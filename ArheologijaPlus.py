# -*- coding: utf-8 -*-
import os
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction
from .ArheologijaPlus_dialog import ArheologijaPlusDialog
from .export_pdf import export_to_pdf   # << Import your PDF export function here

class ArheologijaPlus:
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.actions = []
        self.menu = u"&ArheologijaPlus"
        self.toolbar = self.iface.addToolBar(u'ArheologijaPlus')
        self.toolbar.setObjectName(u'ArheologijaPlus')
        self.dlg = None



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
        for action in self.actions:
            self.iface.removePluginMenu(u'&ArheologijaPlus', action)
            self.iface.removeToolBarIcon(action)
        del self.toolbar

    def run(self):
        if self.dlg is None:
            self.dlg = ArheologijaPlusDialog()
            # Connect button to export PDF using external function
            if hasattr(self.dlg, 'pushButtonExport'):
                self.dlg.pushButtonExport.clicked.connect(self.exportToPdf)
            # ... Connect other buttons as before ...
        self.dlg.fill_with_example_data()
        self.dlg.show()
        self.dlg.exec_()

    def exportToPdf(self):
        export_to_pdf(self.dlg, self.iface)


