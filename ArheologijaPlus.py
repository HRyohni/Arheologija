# -*- coding: utf-8 -*-
import os
import json  # <--- Import the json library
from qgis.core import QgsProject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QDockWidget
from PyQt5.QtCore import Qt
from .ArheologijaPlus_dialog import ArheologijaPlusDialog
from .export_pdf import export_to_pdf


class ArheologijaPlus:
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.actions = []
        self.menu = u"&ArheologijaPlus"
        self.toolbar = self.iface.addToolBar(u'ArheologijaPlus')
        self.toolbar.setObjectName(u'ArheologijaPlus')
        self.dock_widget = None
        self.dialog = None

        # Connect to the project read signal
        QgsProject.instance().readProject.connect(self.load_data_from_project)

    # ... (add_action and initGui methods are unchanged) ...
    def add_action(
            self, icon_path, text, callback,
            enabled_flag=True, add_to_menu=True, add_to_toolbar=True,
            status_tip=None, whats_this=None, parent=None
    ):
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)
        if status_tip is not None:
            action.setStatusTip(status_tip)
        if whats_this is not None:
            action.setWhatsThis(whats_this)
        if add_to_toolbar:
            self.toolbar.addAction(action)
        if add_to_menu:
            self.iface.addPluginToMenu(self.menu, action)
        self.actions.append(action)
        return action

    def initGui(self):
        icon_path = os.path.join(self.plugin_dir, 'icon.png')
        self.add_action(
            icon_path,
            text=u'Archaeological Documentation',
            callback=self.run,
            parent=self.iface.mainWindow()
        )

    def unload(self):
        # Disconnect from the project read signal
        QgsProject.instance().readProject.disconnect(self.load_data_from_project)

        if self.dock_widget:
            self.iface.removeDockWidget(self.dock_widget)

        for action in self.actions:
            self.iface.removePluginMenu(u'&ArheologijaPlus', action)
            self.iface.removeToolBarIcon(action)
        del self.toolbar

    def run(self):
        if not self.dock_widget:
            self.dialog = ArheologijaPlusDialog()
            self.dock_widget = QDockWidget("Arheologija Plus", self.iface.mainWindow())
            self.dock_widget.setWidget(self.dialog)

            # Connect the buttons
            if hasattr(self.dialog, 'pushButtonExport'):
                self.dialog.pushButtonExport.clicked.connect(self.exportToPdf)
            if hasattr(self.dialog, 'pushButtonSave'):
                self.dialog.pushButtonSave.clicked.connect(self.save_data_to_project)
            if hasattr(self.dialog, 'pushButtonLoad'):
                self.dialog.pushButtonLoad.clicked.connect(self.load_data_from_project)

        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)
        self.dock_widget.show()

        # Attempt to load data when the plugin is run
        self.load_data_from_project()

    def save_data_to_project(self):
        """Saves the current data from the dialog to the QGIS project."""
        if self.dialog:
            data = self.dialog.get_data()
            # Convert dictionary to a JSON string before saving
            data_string = json.dumps(data)
            QgsProject.instance().writeEntry("ArheologijaPlus", "data", data_string)
            self.iface.messageBar().pushMessage("Uspjeh", "Podaci su spremljeni u projekt.", level=0, duration=3)

    def load_data_from_project(self):
        """Loads data from the QGIS project into the dialog."""
        if not self.dialog:
            self.run()
            return

        # The third argument should be a default string, not a dictionary
        data_string, success = QgsProject.instance().readEntry("ArheologijaPlus", "data", "")
        if success and data_string:
            # Convert the string back to a dictionary
            data = json.loads(data_string)
            self.dialog.set_data(data)
            self.iface.messageBar().pushMessage("Info", "Podaci su učitani iz projekta.", level=0, duration=3)
        else:
            self.iface.messageBar().pushMessage("Info", "Nema spremljenih podataka u ovom projektu.", level=0,
                                                duration=3)

    def exportToPdf(self):
        if self.dialog:
            export_to_pdf(self.dialog, self.iface)
