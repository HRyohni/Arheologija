import os
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QDockWidget
from PyQt5.QtCore import Qt, QVariant
from qgis.core import (
    QgsProject, QgsVectorLayer, QgsField, QgsFields,
    QgsVectorFileWriter, QgsWkbTypes, QgsFeature
)
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
        self.target_layer = None

    def add_action(self, icon_path, text, callback, parent=None):
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        self.iface.addPluginToMenu(self.menu, action)
        self.toolbar.addAction(action)
        self.actions.append(action)
        return action

    def initGui(self):
        icon_path = os.path.join(self.plugin_dir, 'icon.png')
        self.add_action(icon_path, u'ArheologijaPlus', self.run, self.iface.mainWindow())

    def unload(self):
        if self.target_layer:
            try:
                self.target_layer.selectionChanged.disconnect(self.populate_form_from_selection)
            except (TypeError, RuntimeError):
                pass
        if self.dock_widget:
            self.iface.removeDockWidget(self.dock_widget)
        for action in self.actions:
            self.iface.removePluginMenu(u'&ArheologijaPlus', action)
            self.iface.removeToolBarIcon(action)
        del self.toolbar

    def run(self):
        self.target_layer = self.setup_database_layer()
        if not self.target_layer:
            return

        if not self.dock_widget:
            self.dialog = ArheologijaPlusDialog()
            self.dock_widget = QDockWidget("Arheologija Plus", self.iface.mainWindow())
            self.dock_widget.setWidget(self.dialog)
            if hasattr(self.dialog, 'pushButtonExport'):
                self.dialog.pushButtonExport.clicked.connect(self.exportToPdf)
            if hasattr(self.dialog, 'pushButtonSave'):
                self.dialog.pushButtonSave.clicked.connect(self.save_data_to_layer)

        try:
            self.target_layer.selectionChanged.disconnect(self.populate_form_from_selection)
        except (TypeError, RuntimeError):
            pass
        self.target_layer.selectionChanged.connect(self.populate_form_from_selection)

        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)
        self.dock_widget.show()

    def populate_form_from_selection(self):
        if not self.target_layer: return
        selected_features = self.target_layer.selectedFeatures()
        if len(selected_features) == 1:
            feature = selected_features[0]
            data = {field.name(): feature.attribute(field.name()) for field in self.target_layer.fields()}
            if self.dialog:
                self.dialog.set_data(data)
        else:
            pass

    def save_data_to_layer(self):
        if not self.target_layer:
            self.iface.messageBar().pushMessage("Greška", "Ciljni sloj nije postavljen.", level=3)
            return

        active_layer = self.iface.activeLayer()
        if not active_layer or not isinstance(active_layer, QgsVectorLayer):
            self.iface.messageBar().pushMessage("Upozorenje", "Molimo, odaberite sloj s poligonima.", level=2)
            return

        selected_features = active_layer.selectedFeatures()
        if len(selected_features) != 1:
            self.iface.messageBar().pushMessage("Upozorenje", "Odaberite točno jedan poligon kao predložak geometrije.",
                                                level=2)
            return

        source_geometry = selected_features[0].geometry()
        data = self.dialog.get_data()

        self.target_layer.startEditing()
        feature = QgsFeature(self.target_layer.fields())
        feature.setGeometry(source_geometry)

        for field_name, value in data.items():
            field_index = self.target_layer.fields().lookupField(field_name)
            if field_index != -1:
                feature.setAttribute(field_index, value)

        if self.target_layer.addFeature(feature):
            self.target_layer.commitChanges()
            self.iface.messageBar().pushMessage("Uspjeh", "Novi unos je spremljen.", duration=5)
        else:
            self.target_layer.rollBack()
            self.iface.messageBar().pushMessage("Greška", "Podaci nisu spremljeni.", level=3)

    def exportToPdf(self):
        if self.dialog:
            export_to_pdf(self.dialog, self.iface)

    def setup_database_layer(self):
        layer_name = 'Stratigrafske_Jedinice'
        layers = QgsProject.instance().mapLayersByName(layer_name)
        if layers:
            return layers[0]

        project_path = QgsProject.instance().homePath()
        if not project_path:
            self.iface.messageBar().pushMessage("Upozorenje", "Molimo, prvo spremite vaš QGIS projekt.", level=2,
                                                duration=5)
            return None
        gpkg_path = os.path.join(project_path, 'ArheologijaDB.gpkg')

        if os.path.exists(gpkg_path):
            layer = QgsVectorLayer(f"{gpkg_path}|layername={layer_name}", layer_name, "ogr")
            if layer.isValid():
                QgsProject.instance().addMapLayer(layer)
                return layer

        self.iface.messageBar().pushMessage("Info", "Kreiram novu bazu i sloj...", duration=3)

        fields_list = [
            QgsField('SJ_br', QVariant.Int), QgsField('SJ_vrsta', QVariant.String),
            QgsField('lokalitet', QVariant.String), QgsField('datum', QVariant.Date),
            QgsField('sonda', QVariant.Int), QgsField('sektor', QVariant.String),
            QgsField('kvadrat', QVariant.String), QgsField('aps_visina', QVariant.Double),
            QgsField('najniza_tocka', QVariant.Double), QgsField('najvisa_tocka', QVariant.Double),
            QgsField('oblik', QVariant.String), QgsField('duzina', QVariant.Double),
            QgsField('sirina', QVariant.Double), QgsField('promjer', QVariant.Double),
            QgsField('sastav', QVariant.String), QgsField('konzistencija', QVariant.String),
            QgsField('boja_munsell', QVariant.String), QgsField('opis', QVariant.String),
            QgsField('odnosi_iznad', QVariant.String), QgsField('odnosi_ispod', QVariant.String),
            QgsField('sjece', QVariant.String), QgsField('presjeceno_od', QVariant.String),
            QgsField('zapunjena_sa', QVariant.String), QgsField('zapunjava', QVariant.String),
            QgsField('sastavni_dio', QVariant.String), QgsField('povezana_sa', QVariant.String),
            QgsField('uz', QVariant.String), QgsField('slicna_s', QVariant.String),
            QgsField('keramika', QVariant.Bool), QgsField('keramika_opis', QVariant.String),
            QgsField('opeka', QVariant.Bool), QgsField('opeka_opis', QVariant.String),
            QgsField('ljep', QVariant.Bool), QgsField('ljep_opis', QVariant.String),
            QgsField('staklo', QVariant.Bool), QgsField('staklo_opis', QVariant.String),
            QgsField('metal', QVariant.Bool), QgsField('metal_opis', QVariant.String),
            QgsField('drvo', QVariant.Bool), QgsField('drvo_opis', QVariant.String),
            QgsField('ugljen', QVariant.Bool), QgsField('ugljen_opis', QVariant.String),
            QgsField('kosti', QVariant.Bool), QgsField('kosti_opis', QVariant.String),
            QgsField('ostali_nalazi', QVariant.String), QgsField('posebni_nalazi', QVariant.String),
            QgsField('uzorci', QVariant.String), QgsField('dnevnik_str', QVariant.Int),
            QgsField('foto_br', QVariant.String), QgsField('arheolog', QVariant.String),
            QgsField('snimio', QVariant.String), QgsField('napomene', QVariant.String),
        ]

        qgs_fields = QgsFields()
        for field in fields_list:
            qgs_fields.append(field)

        options = QgsVectorFileWriter.SaveVectorOptions()
        options.driverName = "GPKG"
        options.layerName = layer_name

        writer = QgsVectorFileWriter.create(
            gpkg_path, qgs_fields, QgsWkbTypes.Polygon,
            QgsProject.instance().crs(), QgsProject.instance().transformContext(), options
        )

        if writer is None:
            self.iface.messageBar().pushMessage("Greška pri kreiranju GeoPackage-a.", level=3)
            return None
        del writer

        layer = QgsVectorLayer(f"{gpkg_path}|layername={layer_name}", layer_name, "ogr")
        if layer.isValid():
            QgsProject.instance().addMapLayer(layer)
            self.iface.messageBar().pushMessage("Uspjeh", "Nova baza i sloj su kreirani.", duration=5)
            return layer
        else:
            self.iface.messageBar().pushMessage("Greška", "Nije moguće učitati novokreirani sloj.", level=3)
            return None