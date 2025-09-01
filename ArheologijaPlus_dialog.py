# -*- coding: utf-8 -*-
import os
from PyQt5 import uic
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QWidget

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'ArheologijaPlus_dialog_base.ui'))


class ArheologijaPlusDialog(QWidget, FORM_CLASS):
    def __init__(self, parent=None):
        super(ArheologijaPlusDialog, self).__init__(parent)
        self.setupUi(self)
        self.dateEdit.setDate(QDate.currentDate())


    def get_data(self):
        data = {
            'SJ_br': self.spinBoxSJNumber.value(),
            'SJ_vrsta': self.comboBoxSJType.currentText(),
            'lokalitet': self.lineEditLocalitet.text(),
            'datum': self.dateEdit.date(),
            'sonda': self.spinBoxSonda.value(),
            'sektor': self.lineEditSektor.text(),
            'kvadrat': self.lineEditKvadrat.text(),
            'aps_visina': self.doubleSpinBoxAbsHeight.value(),
            'najniza_tocka': self.doubleSpinBoxLowestPoint.value(),
            'najvisa_tocka': self.doubleSpinBoxHighestPoint.value(),
            'oblik': self.comboBoxShape.currentText(),
            'duzina': self.doubleSpinBoxLength.value(),
            'sirina': self.doubleSpinBoxWidth.value(),
            'promjer': self.doubleSpinBoxDiameter.value(),
            'sastav': self.lineEditComposition.text(),
            'konzistencija': self.lineEditConsistency.text(),
            'boja_munsell': self.lineEditColor.text(),
            'opis': self.textEditDescription.toPlainText(),
            'odnosi_iznad': self.lineEditSJAbove.text(),
            'odnosi_ispod': self.lineEditSJBelow.text(),
            'sjece': self.lineEditCuts.text(),
            'presjeceno_od': self.lineEditCutBy.text(),
            'zapunjena_sa': self.lineEditFilledWith.text(),
            'zapunjava': self.lineEditFills.text(),
            'sastavni_dio': self.lineEditComponent.text(),
            'povezana_sa': self.lineEditConnectedWith.text(),
            'uz': self.lineEditAdjacentTo.text(),
            'slicna_s': self.lineEditSimilarTo.text(),
            'keramika': self.checkBoxCeramics.isChecked(),
            'keramika_opis': self.lineEditCeramicsNotes.text(),
            'opeka': self.checkBoxBrick.isChecked(),
            'opeka_opis': self.lineEditBrickNotes.text(),
            'ljep': self.checkBoxClay.isChecked(),
            'ljep_opis': self.lineEditClayNotes.text(),
            'staklo': self.checkBoxGlass.isChecked(),
            'staklo_opis': self.lineEditGlassNotes.text(),
            'metal': self.checkBoxMetal.isChecked(),
            'metal_opis': self.lineEditMetalNotes.text(),
            'drvo': self.checkBoxWood.isChecked(),
            'drvo_opis': self.lineEditWoodNotes.text(),
            'ugljen': self.checkBoxCharcoal.isChecked(),
            'ugljen_opis': self.lineEditCharcoalNotes.text(),
            'kosti': self.checkBoxBones.isChecked(),
            'kosti_opis': self.lineEditBonesNotes.text(),
            'ostali_nalazi': self.lineEditOtherFindings.text(),
            'posebni_nalazi': self.lineEditSpecialFindings.text(),
            'uzorci': self.lineEditSamples.text(),
            'dnevnik_str': self.spinBoxDiaryPage.value(),
            'foto_br': self.lineEditPhotoNumber.text(),
            'arheolog': self.lineEditArchaeologist.text(),
            'snimio': self.lineEditPhotographer.text(),
            'napomene': self.textEditNotes.toPlainText(),
            'opis_priloga': self.textEditAnnexDescription.toPlainText(),
        }
        return data

    def set_data(self, data):
        """Popunjava UI s podacima iz rječnika (feature atributa)."""
        self.spinBoxSJNumber.setValue(data.get('SJ_br') or 0)
        self.comboBoxSJType.setCurrentText(data.get('SJ_vrsta') or '')
        self.lineEditLocalitet.setText(data.get('lokalitet') or '')

        datum_vrijednost = data.get('datum')
        if datum_vrijednost and isinstance(datum_vrijednost, QDate) and datum_vrijednost.isValid():
            self.dateEdit.setDate(datum_vrijednost)
        else:
            self.dateEdit.setDate(QDate.currentDate())

        self.spinBoxSonda.setValue(data.get('sonda') or 0)
        self.lineEditSektor.setText(data.get('sektor') or '')
        self.lineEditKvadrat.setText(data.get('kvadrat') or '')
        self.doubleSpinBoxAbsHeight.setValue(data.get('aps_visina') or 0.0)
        self.doubleSpinBoxLowestPoint.setValue(data.get('najniza_tocka') or 0.0)
        self.doubleSpinBoxHighestPoint.setValue(data.get('najvisa_tocka') or 0.0)
        self.comboBoxShape.setCurrentText(data.get('oblik') or '')
        self.doubleSpinBoxLength.setValue(data.get('duzina') or 0.0)
        self.doubleSpinBoxWidth.setValue(data.get('sirina') or 0.0)
        self.doubleSpinBoxDiameter.setValue(data.get('promjer') or 0.0)
        self.lineEditComposition.setText(data.get('sastav') or '')
        self.lineEditConsistency.setText(data.get('konzistencija') or '')
        self.lineEditColor.setText(data.get('boja_munsell') or '')
        self.textEditDescription.setPlainText(data.get('opis') or '')
        self.lineEditSJAbove.setText(data.get('odnosi_iznad') or '')
        self.lineEditSJBelow.setText(data.get('odnosi_ispod') or '')
        self.lineEditCuts.setText(data.get('sjece') or '')
        self.lineEditCutBy.setText(data.get('presjeceno_od') or '')
        self.lineEditFilledWith.setText(data.get('zapunjena_sa') or '')
        self.lineEditFills.setText(data.get('zapunjava') or '')
        self.lineEditComponent.setText(data.get('sastavni_dio') or '')
        self.lineEditConnectedWith.setText(data.get('povezana_sa') or '')
        self.lineEditAdjacentTo.setText(data.get('uz') or '')
        self.lineEditSimilarTo.setText(data.get('slicna_s') or '')
        self.checkBoxCeramics.setChecked(data.get('keramika') or False)
        self.lineEditCeramicsNotes.setText(data.get('keramika_opis') or '')
        self.checkBoxBrick.setChecked(data.get('opeka') or False)
        self.lineEditBrickNotes.setText(data.get('opeka_opis') or '')
        self.checkBoxClay.setChecked(data.get('ljep') or False)
        self.lineEditClayNotes.setText(data.get('ljep_opis') or '')
        self.checkBoxGlass.setChecked(data.get('staklo') or False)
        self.lineEditGlassNotes.setText(data.get('staklo_opis') or '')
        self.checkBoxMetal.setChecked(data.get('metal') or False)
        self.lineEditMetalNotes.setText(data.get('metal_opis') or '')
        self.checkBoxWood.setChecked(data.get('drvo') or False)
        self.lineEditWoodNotes.setText(data.get('drvo_opis') or '')
        self.checkBoxCharcoal.setChecked(data.get('ugljen') or False)
        self.lineEditCharcoalNotes.setText(data.get('ugljen_opis') or '')
        self.checkBoxBones.setChecked(data.get('kosti') or False)
        self.lineEditBonesNotes.setText(data.get('kosti_opis') or '')
        self.lineEditOtherFindings.setText(data.get('ostali_nalazi') or '')
        self.lineEditSpecialFindings.setText(data.get('posebni_nalazi') or '')
        self.lineEditSamples.setText(data.get('uzorci') or '')
        self.spinBoxDiaryPage.setValue(data.get('dnevnik_str') or 0)
        self.lineEditPhotoNumber.setText(data.get('foto_br') or '')
        self.lineEditArchaeologist.setText(data.get('arheolog') or '')
        self.lineEditPhotographer.setText(data.get('snimio') or '')
        self.textEditNotes.setPlainText(data.get('napomene') or '')
        self.textEditAnnexDescription.setPlainText(data.get('opis_priloga') or '')

    def clear_data(self):
        """Čisti sve unose u UI-u."""
        self.spinBoxSJNumber.setValue(0)
        self.comboBoxSJType.setCurrentIndex(0)
        self.lineEditLocalitet.setText('')
        self.dateEdit.setDate(QDate.currentDate())
        self.spinBoxSonda.setValue(0)
        self.lineEditSektor.setText('')
        self.lineEditKvadrat.setText('')
        self.doubleSpinBoxAbsHeight.setValue(0.0)
        self.doubleSpinBoxLowestPoint.setValue(0.0)
        self.doubleSpinBoxHighestPoint.setValue(0.0)
        self.comboBoxShape.setCurrentIndex(0)
        self.doubleSpinBoxLength.setValue(0.0)
        self.doubleSpinBoxWidth.setValue(0.0)
        self.doubleSpinBoxDiameter.setValue(0.0)
        self.lineEditComposition.setText('')
        self.lineEditConsistency.setText('')
        self.lineEditColor.setText('')
        self.textEditDescription.setPlainText('')
        self.lineEditSJAbove.setText('')
        self.lineEditSJBelow.setText('')
        self.lineEditCuts.setText('')
        self.lineEditCutBy.setText('')
        self.lineEditFilledWith.setText('')
        self.lineEditFills.setText('')
        self.lineEditComponent.setText('')
        self.lineEditConnectedWith.setText('')
        self.lineEditAdjacentTo.setText('')
        self.lineEditSimilarTo.setText('')
        self.checkBoxCeramics.setChecked(False)
        self.lineEditCeramicsNotes.setText('')
        self.checkBoxBrick.setChecked(False)
        self.lineEditBrickNotes.setText('')
        self.checkBoxClay.setChecked(False)
        self.lineEditClayNotes.setText('')
        self.checkBoxGlass.setChecked(False)
        self.lineEditGlassNotes.setText('')
        self.checkBoxMetal.setChecked(False)
        self.lineEditMetalNotes.setText('')
        self.checkBoxWood.setChecked(False)
        self.lineEditWoodNotes.setText('')
        self.checkBoxCharcoal.setChecked(False)
        self.lineEditCharcoalNotes.setText('')
        self.checkBoxBones.setChecked(False)
        self.lineEditBonesNotes.setText('')
        self.lineEditOtherFindings.setText('')
        self.lineEditSpecialFindings.setText('')
        self.lineEditSamples.setText('')
        self.spinBoxDiaryPage.setValue(0)
        self.lineEditPhotoNumber.setText('')
        self.lineEditArchaeologist.setText('')
        self.lineEditPhotographer.setText('')
        self.textEditNotes.setPlainText('')
        self.textEditAnnexDescription.setPlainText('')