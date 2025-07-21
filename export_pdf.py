from PyQt5.QtWidgets import QFileDialog
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Frame
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas


def export_to_pdf(dlg, iface):
    """
    Exports the archaeological stratigraphic unit data from the Qt dialog
    to a PDF document, formatted to match the provided PDF standard.

    Args:
        dlg: The PyQt5 dialog object containing the input fields.
        iface: The QGIS interface object for displaying messages.
    """
    fileName, _ = QFileDialog.getSaveFileName(
        dlg, "Export to PDF", "", "PDF Files (*.pdf)"
    )
    if not fileName:
        return
    if not fileName.endswith('.pdf'):
        fileName += '.pdf'

    # Set up the document with A4 page size and custom margins
    doc = SimpleDocTemplate(fileName, pagesize=A4, rightMargin=20 * mm, leftMargin=20 * mm, topMargin=15 * mm,
                            bottomMargin=12 * mm)

    # Get standard styles and define a bold style
    styles = getSampleStyleSheet()
    styleN = styles["Normal"]
    styleB = ParagraphStyle('Bold', parent=styleN, fontName='Helvetica-Bold')
    styleSmall = ParagraphStyle('Small', parent=styleN, fontSize=8)  # Smaller font for some elements if needed

    elements = []

    # --- HEADER SECTION ---
    # "STRATIGRAFSKA JEDINICA br."
    elements.append(Paragraph(f"STRATIGRAFSKA JEDINICA br. <b>{dlg.spinBoxSJNumber.value()}</b>", styleB))
    elements.append(Spacer(1, 4 * mm))

    # "LOKALITET:" and its value
    elements.append(Paragraph("LOKALITET:", styleN))
    elements.append(Paragraph(f"<b>{dlg.lineEditLocalitet.text()}</b>", styleN))  # Value in bold
    elements.append(Spacer(1, 2 * mm))

    # "Vrsta SJ sloj" and "Datum:" with their values
    vrsta = dlg.comboBoxSJType.currentText()
    datum = dlg.dateEdit.date().toString("d. M.yyyy.")  # Ensure year is 4 digits

    # Create a table for "Vrsta SJ" and "Datum" to align them side-by-side
    date_type_data = [
        ["Vrsta SJ sloj", "Datum:"],
        [f"<b>{vrsta}</b>", f"<b>{datum}</b>"]
    ]
    t_date_type = Table(date_type_data, colWidths=[60 * mm, 60 * mm])
    t_date_type.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
    ]))
    elements.append(t_date_type)
    elements.append(Spacer(1, 3 * mm))

    # --- FIRST BLOCK: Location, Sonda, Sektor, Kvadrat, Heights ---
    # This section is complex in the PDF, combining labels and values in a non-standard table.
    # We will use a table to approximate the visual layout.
    loc_data = [
        ["Sonda", "Sektor", "Kvadrat"],
        [str(dlg.spinBoxSonda.value()), dlg.lineEditSektor.text(), dlg.lineEditKvadrat.text()],
        ["Apsolutna visina najviše točke", "Visina", ""],  # "Visina" spans two cells
        [str(dlg.doubleSpinBoxHighestPoint.value()), "Apsolutna visina najniže točke", ""],
        ["", str(dlg.doubleSpinBoxLowestPoint.value()), ""],
    ]
    t_loc = Table(loc_data, colWidths=[50 * mm, 50 * mm, 50 * mm])  # Adjusted widths for better fit
    t_loc.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        # Span "Visina" across two cells
        ('SPAN', (1, 2), (2, 2)),
        # Add a light grey background to the first row of labels for visual distinction if desired
        # ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
    ]))
    elements.append(t_loc)
    elements.append(Spacer(1, 2 * mm))

    # "3" and "SJ List br." as separate paragraphs to match PDF's isolated placement
    elements.append(Paragraph("3", styleN))
    elements.append(
        Paragraph(f"SJ List br. {dlg.spinBoxSJNumber.value()}", styleN))  # Assuming SJ number is the list number
    elements.append(Spacer(1, 2 * mm))

    # --- SECOND BLOCK: Composition, Color, Consistency, Shape, Dimensions ---
    char_data = [
        ["Sastav:", dlg.lineEditComposition.text()],
        ["Konzistencija:", dlg.lineEditConsistency.text()],
        ["Oblik:", dlg.comboBoxShape.currentText()],
        ["Dužina:", f"{dlg.doubleSpinBoxLength.value()} m"],
        ["Širina:", f"{dlg.doubleSpinBoxWidth.value()} m"],
        ["Promjer:", f"{dlg.doubleSpinBoxDiameter.value()} m"],  # Promjer on its own line as in PDF
        ["Boja(Munsell):", dlg.lineEditColor.text()]  # Color at the end as in PDF
    ]
    # Adjusting column widths to make it visually similar to the PDF's two-column layout
    t_char = Table(char_data, colWidths=[40 * mm, 80 * mm])  # Adjusted widths
    t_char.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elements.append(t_char)
    elements.append(Spacer(1, 2 * mm))

    # --- OPIS (DESCRIPTION) ---
    elements.append(Paragraph("<b>OPIS</b>", styleB))
    opis = dlg.textEditDescription.toPlainText()
    elements.append(Paragraph(opis, styleN))
    elements.append(Spacer(1, 2 * mm))

    # --- STRATIGRAFSKI ODNOSI (STRATIGRAPHIC RELATIONS) ---
    strat_data = [
        ["SJ iznad", dlg.lineEditSJAbove.text(), "SJ ispod", dlg.lineEditSJBelow.text()],
        ["Sječe", dlg.lineEditCuts.text(), "Presječeno od", dlg.lineEditCutBy.text()],
        ["Zapunjena sa SJ", dlg.lineEditFilledWith.text(), "Zapunjava SJ", dlg.lineEditFills.text()],
        ["Sastavni dio", dlg.lineEditComponent.text(), "Povezana sa SJ", dlg.lineEditConnectedWith.text()],
        ["Uz", dlg.lineEditAdjacentTo.text(), "Slična s SJ", dlg.lineEditSimilarTo.text()]
    ]
    t_strat = Table(strat_data, colWidths=[30 * mm, 45 * mm, 30 * mm, 45 * mm])  # Adjusted widths
    t_strat.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elements.append(Paragraph("<b>STRATIGRAFSKI ODNOSI</b>", styleB))
    elements.append(t_strat)
    elements.append(Spacer(1, 2 * mm))

    # --- NALAZI (FINDINGS) ---
    # This section is also complex in the PDF with specific "N-" and "U-" prefixes
    # and a mixed 3-column then 2-column layout.
    nal_data = [
        [f"Keramika N- {dlg.comboBoxCeramics.currentText()}", "", "Ostali nalazi:", dlg.lineEditOtherFindings.text()],
        [f"Opeka N- {dlg.comboBoxBrick.currentText()}", "", "Ljep N- {dlg.comboBoxClay.currentText()}", ""],
        # Ljep moved to second column
        ["Posebni nalazi:", dlg.lineEditSpecialFindings.text(), "Staklo N- {dlg.comboBoxGlass.currentText()}", ""],
        # Staklo moved
        [f"Metal N- {dlg.comboBoxMetal.currentText()}", "", "PN -", ""],  # PN - label
        ["Uzorci:", dlg.lineEditSamples.text(), f"Drvo U- {dlg.comboBoxWood.currentText()}", ""],  # Drvo moved
        [f"Ugljen U- {dlg.comboBoxCharcoal.currentText()}", "", "Napomene:", dlg.textEditNotes.toPlainText()],
        [f"Kosti N- {dlg.comboBoxBones.currentText()}", "", "", ""]
    ]
    # Adjust colWidths to match the PDF's visual grouping and spacing
    t_nal = Table(nal_data, colWidths=[40 * mm, 30 * mm, 40 * mm, 40 * mm])  # Adjusted to approximate PDF layout
    t_nal.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        # Spanning for "Ostali nalazi", "Posebni nalazi", "Uzorci", "Napomene"
        ('SPAN', (2, 0), (3, 0)),  # Ostali nalazi
        ('SPAN', (0, 2), (1, 2)),  # Posebni nalazi
        ('SPAN', (2, 2), (3, 2)),  # Staklo
        ('SPAN', (0, 4), (1, 4)),  # Uzorci
        ('SPAN', (2, 5), (3, 5)),  # Napomene
    ]))
    elements.append(Paragraph("<b>NALAZI</b>", styleB))
    elements.append(t_nal)
    elements.append(Spacer(1, 2 * mm))

    # --- MEDIA SECTION: Diary Page, Archaeologist, Photo Number, Photographer ---
    media_data = [
        ["Stranica dnevnika", str(dlg.spinBoxDiaryPage.value()), "Arheolog:", dlg.lineEditArchaeologist.text()],
        ["Foto br.", dlg.lineEditPhotoNumber.text(), "Snimio:", dlg.lineEditPhotographer.text()],
    ]
    t_media = Table(media_data, colWidths=[35 * mm, 35 * mm, 30 * mm, 40 * mm])  # Adjusted widths
    t_media.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elements.append(t_media)
    elements.append(Spacer(1, 2 * mm))

    # --- PLACEHOLDERS FOR SKETCHES ---
    elements.append(Spacer(1, 10 * mm))
    elements.append(Paragraph("SJ SKICA STRATIGRAFSKE JEDINICE", styleB))
    elements.append(Spacer(1, 25 * mm))  # Increased space for sketch

    # "Z" in the middle of the second sketch placeholder
    elements.append(Paragraph("SKICA POLOŽAJA STRATIGRAFSKE JEDINICE U SONDI / KVADRANTU", styleB))
    elements.append(Paragraph("Z", ParagraphStyle('CenteredBold', parent=styleB, alignment=1)))  # Centered "Z"
    elements.append(Spacer(1, 25 * mm))  # Increased space for sketch

    # --- FOOTER ---
    footer = "Ministarstvo kulture, Uprava za zaštitu kulturne baštine, Odjel za arheološku baštinu"
    elements.append(Spacer(1, 8 * mm))
    elements.append(Paragraph(footer, styleN))

    # Build the PDF document
    try:
        doc.build(elements)
        iface.messageBar().pushMessage("Uspjeh", f"PDF spremljen: {fileName}", level=0, duration=4)
        print(f"PDF export successful: {fileName}")
    except Exception as e:
        iface.messageBar().pushMessage("Greška", f"Greška kod izvoza PDF-a: {e}", level=3, duration=7)
        print(f"Error exporting PDF: {e}")
