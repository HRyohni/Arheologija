# -*- coding: utf-8 -*-

import os
from PyQt5 import uic
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QDialog

# Load the UI file dynamically from the same directory as this file.
# Ensure 'ArheologijaPlus_dialog_base.ui' name matches your saved UI file
FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'ArheologijaPlus_dialog_base.ui'))


class ArheologijaPlusDialog(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """
        Constructor.
        Loads the user interface from the .ui file.
        """
        super(ArheologijaPlusDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        self.setupUi(self)

        # Ako ste premjestili povezivanje signala ovdje (kako je preporučeno ranije),
        # trebali biste ukloniti veze za pushButtonDigitize i pushButtonColorPicker.
        # Npr. ako ste imali:
        # self.pushButtonDigitize.clicked.connect(self.digitize_feature)
        # Ovu liniju biste obrisali.

    def fill_with_example_data(self):
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
        self.lineEditSJAbove.setText("100")
        self.lineEditSJBelow.setText("102")
        self.lineEditCuts.setText("103")
        self.lineEditCutBy.setText("104")
        self.lineEditFilledWith.setText("105")
        self.lineEditFills.setText("106")
        self.lineEditComponent.setText("107")
        self.lineEditConnectedWith.setText("108")
        self.lineEditAdjacentTo.setText("109")
        self.lineEditSimilarTo.setText("110")
        self.comboBoxCeramics.setCurrentText("D")
        self.lineEditCeramicsNotes.setText("Fragmenata keramike, rimska razdoblja")
        self.comboBoxBrick.setCurrentText("N")
        self.lineEditBrickNotes.setText("Bez vidljivih opeka")
        self.comboBoxClay.setCurrentText("D")
        self.lineEditClayNotes.setText("Mali komadići gline")
        self.comboBoxGlass.setCurrentText("-")
        self.lineEditGlassNotes.setText("")
        self.comboBoxMetal.setCurrentText("D")
        self.lineEditMetalNotes.setText("Gvozdeni čavao")
        self.comboBoxWood.setCurrentText("U")
        self.lineEditWoodNotes.setText("Tragovi ugljena")
        self.comboBoxCharcoal.setCurrentText("D")
        self.lineEditCharcoalNotes.setText("Rasprostranjeno")
        self.comboBoxBones.setCurrentText("N")
        self.lineEditBonesNotes.setText("")
        self.lineEditOtherFindings.setText("Sjemenke, školjke")
        self.lineEditSpecialFindings.setText("Nakit")
        self.lineEditSamples.setText("1 uzorak zemlje")
        self.spinBoxDiaryPage.setValue(7)
        self.lineEditPhotoNumber.setText("P-2024-015")
        self.lineEditArchaeologist.setText("Ivan Horvat")
        self.lineEditPhotographer.setText("Ana Kovač")
        self.textEditNotes.setPlainText("Napomena: Mokro vrijeme, otežano uzorkovanje.")