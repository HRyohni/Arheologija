# -*- coding: utf-8 -*-

import os
from PyQt5 import uic
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QWidget

# Load the UI file
FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'ArheologijaPlus_dialog_base.ui'))

class ArheologijaPlusDialog(QWidget, FORM_CLASS):
    def __init__(self, parent=None):
        super(ArheologijaPlusDialog, self).__init__(parent)
        self.setupUi(self)

    def get_data(self):
        """Returns a dictionary with all the data from the UI."""
        data = {
            'SJNumber': self.spinBoxSJNumber.value(),
            'SJType': self.comboBoxSJType.currentText(),
            'Lokalitet': self.lineEditLocalitet.text(),
            'Datum': self.dateEdit.date().toString("dd-MM-yyyy"),
            'Sonda': self.spinBoxSonda.value(),
            'Sektor': self.lineEditSektor.text(),
            'Kvadrat': self.lineEditKvadrat.text(),
            'AbsHeight': self.doubleSpinBoxAbsHeight.value(),
            'LowestPoint': self.doubleSpinBoxLowestPoint.value(),
            'HighestPoint': self.doubleSpinBoxHighestPoint.value(),
            'Shape': self.comboBoxShape.currentText(),
            'Length': self.doubleSpinBoxLength.value(),
            'Width': self.doubleSpinBoxWidth.value(),
            'Diameter': self.doubleSpinBoxDiameter.value(),
            'Composition': self.lineEditComposition.text(),
            'Consistency': self.lineEditConsistency.text(),
            'Color': self.lineEditColor.text(),
            'Description': self.textEditDescription.toPlainText(),
            'SJAbove': self.lineEditSJAbove.text(),
            'SJBelow': self.lineEditSJBelow.text(),
            'Cuts': self.lineEditCuts.text(),
            'CutBy': self.lineEditCutBy.text(),
            'FilledWith': self.lineEditFilledWith.text(),
            'Fills': self.lineEditFills.text(),
            'Component': self.lineEditComponent.text(),
            'ConnectedWith': self.lineEditConnectedWith.text(),
            'AdjacentTo': self.lineEditAdjacentTo.text(),
            'SimilarTo': self.lineEditSimilarTo.text(),
            'Ceramics': self.comboBoxCeramics.currentText(),
            'CeramicsNotes': self.lineEditCeramicsNotes.text(),
            'Brick': self.comboBoxBrick.currentText(),
            'BrickNotes': self.lineEditBrickNotes.text(),
            'Clay': self.comboBoxClay.currentText(),
            'ClayNotes': self.lineEditClayNotes.text(),
            'Glass': self.comboBoxGlass.currentText(),
            'GlassNotes': self.lineEditGlassNotes.text(),
            'Metal': self.comboBoxMetal.currentText(),
            'MetalNotes': self.lineEditMetalNotes.text(),
            'Wood': self.comboBoxWood.currentText(),
            'WoodNotes': self.lineEditWoodNotes.text(),
            'Charcoal': self.comboBoxCharcoal.currentText(),
            'CharcoalNotes': self.lineEditCharcoalNotes.text(),
            'Bones': self.comboBoxBones.currentText(),
            'BonesNotes': self.lineEditBonesNotes.text(),
            'OtherFindings': self.lineEditOtherFindings.text(),
            'SpecialFindings': self.lineEditSpecialFindings.text(),
            'Samples': self.lineEditSamples.text(),
            'DiaryPage': self.spinBoxDiaryPage.value(),
            'PhotoNumber': self.lineEditPhotoNumber.text(),
            'Archaeologist': self.lineEditArchaeologist.text(),
            'Photographer': self.lineEditPhotographer.text(),
            'Notes': self.textEditNotes.toPlainText(),
        }
        return data

    def set_data(self, data):
        """Populates the UI with data from a dictionary."""
        self.spinBoxSJNumber.setValue(data.get('SJNumber', 0))
        self.comboBoxSJType.setCurrentText(data.get('SJType', ''))
        self.lineEditLocalitet.setText(data.get('Lokalitet', ''))
        self.dateEdit.setDate(QDate.fromString(data.get('Datum', ''), "yyyy-MM-dd"))
        self.spinBoxSonda.setValue(data.get('Sonda', 0))
        # ... (rest of the fields)
        self.lineEditSektor.setText(data.get('Sektor', ''))
        self.lineEditKvadrat.setText(data.get('Kvadrat', ''))
        self.doubleSpinBoxAbsHeight.setValue(data.get('AbsHeight', 0.0))
        self.doubleSpinBoxLowestPoint.setValue(data.get('LowestPoint', 0.0))
        self.doubleSpinBoxHighestPoint.setValue(data.get('HighestPoint', 0.0))
        self.comboBoxShape.setCurrentText(data.get('Shape', ''))
        self.doubleSpinBoxLength.setValue(data.get('Length', 0.0))
        self.doubleSpinBoxWidth.setValue(data.get('Width', 0.0))
        self.doubleSpinBoxDiameter.setValue(data.get('Diameter', 0.0))
        self.lineEditComposition.setText(data.get('Composition', ''))
        self.lineEditConsistency.setText(data.get('Consistency', ''))
        self.lineEditColor.setText(data.get('Color', ''))
        self.textEditDescription.setPlainText(data.get('Description', ''))
        self.lineEditSJAbove.setText(data.get('SJAbove', ''))
        self.lineEditSJBelow.setText(data.get('SJBelow', ''))
        self.lineEditCuts.setText(data.get('Cuts', ''))
        self.lineEditCutBy.setText(data.get('CutBy', ''))
        self.lineEditFilledWith.setText(data.get('FilledWith', ''))
        self.lineEditFills.setText(data.get('Fills', ''))
        self.lineEditComponent.setText(data.get('Component', ''))
        self.lineEditConnectedWith.setText(data.get('ConnectedWith', ''))
        self.lineEditAdjacentTo.setText(data.get('AdjacentTo', ''))
        self.lineEditSimilarTo.setText(data.get('SimilarTo', ''))
        self.comboBoxCeramics.setCurrentText(data.get('Ceramics', ''))
        self.lineEditCeramicsNotes.setText(data.get('CeramicsNotes', ''))
        self.comboBoxBrick.setCurrentText(data.get('Brick', ''))
        self.lineEditBrickNotes.setText(data.get('BrickNotes', ''))
        self.comboBoxClay.setCurrentText(data.get('Clay', ''))
        self.lineEditClayNotes.setText(data.get('ClayNotes', ''))
        self.comboBoxGlass.setCurrentText(data.get('Glass', ''))
        self.lineEditGlassNotes.setText(data.get('GlassNotes', ''))
        self.comboBoxMetal.setCurrentText(data.get('Metal', ''))
        self.lineEditMetalNotes.setText(data.get('MetalNotes', ''))
        self.comboBoxWood.setCurrentText(data.get('Wood', ''))
        self.lineEditWoodNotes.setText(data.get('WoodNotes', ''))
        self.comboBoxCharcoal.setCurrentText(data.get('Charcoal', ''))
        self.lineEditCharcoalNotes.setText(data.get('CharcoalNotes', ''))
        self.comboBoxBones.setCurrentText(data.get('Bones', ''))
        self.lineEditBonesNotes.setText(data.get('BonesNotes', ''))
        self.lineEditOtherFindings.setText(data.get('OtherFindings', ''))
        self.lineEditSpecialFindings.setText(data.get('SpecialFindings', ''))
        self.lineEditSamples.setText(data.get('Samples', ''))
        self.spinBoxDiaryPage.setValue(data.get('DiaryPage', 0))
        self.lineEditPhotoNumber.setText(data.get('PhotoNumber', ''))
        self.lineEditArchaeologist.setText(data.get('Archaeologist', ''))
        self.lineEditPhotographer.setText(data.get('Photographer', ''))
        self.textEditNotes.setPlainText(data.get('Notes', ''))

    def fill_with_example_data(self):
        # ... (This function remains the same)
        self.spinBoxSJNumber.setValue(101)
        self.comboBoxSJType.setCurrentText("sloj")
        self.lineEditLocalitet.setText("Pula - Kaštel")
        self.dateEdit.setDate(QDate(2024, 5, 29))
        self.spinBoxSonda.setValue(3)
        self.lineEditSektor.setText("A1")
        self.lineEditKvadrat.setText("B2")
        self.doubleSpinBoxAbsHeight.setValue(12.345)
        self.doubleSpinBoxLowestPoint.setValue(11.111)
        self.doubleSpinBoxHighestPoint.setValue(13.321)
        self.comboBoxShape.setCurrentText("pravilni")
        self.doubleSpinBoxLength.setValue(2.15)
        self.doubleSpinBoxWidth.setValue(1.1)
        self.doubleSpinBoxDiameter.setValue(0.0)
        self.lineEditComposition.setText("zemlja, pijesak")
        self.lineEditConsistency.setText("kompaktno")
        self.lineEditColor.setText("10YR 5/3")
        self.textEditDescription.setPlainText("Opis primjer: Debeli sloj tamne zemlje s ostacima keramike.")
        # ... etc.