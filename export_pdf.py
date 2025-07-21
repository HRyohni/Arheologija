import os
from PyQt5.QtWidgets import QFileDialog
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def export_to_pdf(dlg, iface):
    """
    Exports the archaeological stratigraphic unit data to a PDF document,
    matching the layout of the provided standard form exactly.
    """
    fileName, _ = QFileDialog.getSaveFileName(
        dlg, "Export to PDF", "", "PDF Files (*.pdf)"
    )
    if not fileName:
        return
    if not fileName.endswith('.pdf'):
        fileName += '.pdf'

    # --- FONT REGISTRATION ---
    plugin_dir = os.path.dirname(__file__)
    font_path_regular = os.path.join(plugin_dir, 'DejaVuSans.ttf')
    font_path_bold = os.path.join(plugin_dir, 'DejaVuSans-Bold.ttf')

    if not os.path.exists(font_path_regular) or not os.path.exists(font_path_bold):
        iface.messageBar().pushMessage("Greška", "Font 'DejaVuSans.ttf' i/ili 'DejaVuSans-Bold.ttf' nije pronađen.",
                                       level=3, duration=7)
        return

    pdfmetrics.registerFont(TTFont('DejaVu-Sans', font_path_regular))
    pdfmetrics.registerFont(TTFont('DejaVu-Sans-Bold', font_path_bold))

    doc = SimpleDocTemplate(fileName, pagesize=A4, rightMargin=15 * mm, leftMargin=15 * mm, topMargin=15 * mm,
                            bottomMargin=10 * mm)

    # --- STYLES ---
    styleN = ParagraphStyle('Normal', fontName='DejaVu-Sans', fontSize=9, leading=11)
    styleB = ParagraphStyle('Bold', parent=styleN, fontName='DejaVu-Sans-Bold')
    styleSmall = ParagraphStyle('Small', parent=styleN, fontSize=8, leading=9)

    elements = []

    # --- TOP RIGHT SJ BOX ---
    sj_box_data = [["SJ"], [f"List br."]]
    sj_box_table = Table(sj_box_data, colWidths=[20 * mm], rowHeights=[8 * mm, 8 * mm])
    sj_box_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVu-Sans-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8)
    ]))

    # --- HEADER WITH SJ BOX ---
    header_data = [
        [f"STRATIGRAFSKA JEDINICA br. ____{dlg.spinBoxSJNumber.value()}____", sj_box_table]
    ]
    header_table = Table(header_data, colWidths=[160 * mm, 20 * mm])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (0, 0), 'BOTTOM'),
        ('VALIGN', (1, 0), (1, 0), 'TOP'),
        ('FONTNAME', (0, 0), (0, 0), 'DejaVu-Sans-Bold'),
        ('FONTSIZE', (0, 0), (0, 0), 11)
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 3 * mm))

    # --- LOKALITET, VRSTA SJ, DATUM ROW ---
    top_row_data = [
        [f"LOKALITET:\n{dlg.lineEditLocalitet.text()}", "Vrsta SJ sloj",
         f"Datum:\n{dlg.dateEdit.date().toString('d. M. yyyy.')}"]
    ]
    top_row_table = Table(top_row_data, colWidths=[90 * mm, 50 * mm, 40 * mm], rowHeights=[12 * mm])
    top_row_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (0, 0), 'DejaVu-Sans-Bold'),
        ('FONTNAME', (1, 0), (1, 0), 'DejaVu-Sans'),
        ('FONTNAME', (2, 0), (2, 0), 'DejaVu-Sans-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3)
    ]))
    elements.append(top_row_table)

    # --- SONDA, SEKTOR, KVADRAT, VISINA ROW ---
    location_data = [
        ["Sonda\n2", "Sektor", "Kvadrat", "Apsolutna visina najviše točke\n\nVisina\n\nApsolutna visina najniže točke"]
    ]
    location_table = Table(location_data, colWidths=[30 * mm, 30 * mm, 30 * mm, 90 * mm], rowHeights=[25 * mm])
    location_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVu-Sans'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3)
    ]))
    elements.append(location_table)

    # --- CHARACTERISTICS TABLE ---
    char_data = [
        [f"Sastav: {dlg.lineEditComposition.text()}", f"Boja(Munsell)\n{dlg.lineEditColor.text()}"],
        [f"Konzistencija: {dlg.lineEditConsistency.text()}", ""],
        ["Oblik\nnepravilni", "Dužina\n2.4 m", "Širina\n1.7 m", "Promjer"]
    ]
    char_table = Table(char_data, colWidths=[90 * mm, 90 * mm, 0, 0])
    char_table.setStyle(TableStyle([
        ('GRID', (0, 0), (1, 2), 1, colors.black),
        ('SPAN', (0, 0), (1, 0)),
        ('SPAN', (0, 1), (1, 1)),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVu-Sans'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3)
    ]))

    # Separate table for the bottom row with 4 columns
    char_bottom_data = [["Oblik\nnepravilni", "Dužina\n2.4 m", "Širina\n1.7 m", "Promjer"]]
    char_bottom_table = Table(char_bottom_data, colWidths=[45 * mm, 45 * mm, 45 * mm, 45 * mm], rowHeights=[15 * mm])
    char_bottom_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVu-Sans'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3)
    ]))

    # First part of characteristics
    char_top_data = [
        [f"Sastav: {dlg.lineEditComposition.text()}", f"Boja(Munsell)\n{dlg.lineEditColor.text()}"],
        [f"Konzistencija: {dlg.lineEditConsistency.text()}", ""]
    ]
    char_top_table = Table(char_top_data, colWidths=[90 * mm, 90 * mm], rowHeights=[10 * mm, 10 * mm])
    char_top_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVu-Sans'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3)
    ]))

    elements.append(char_top_table)
    elements.append(char_bottom_table)

    # --- OPIS SECTION ---
    opis_data = [[f"OPIS\n{dlg.textEditDescription.toPlainText()}"]]
    opis_table = Table(opis_data, colWidths=[180 * mm], rowHeights=[25 * mm])
    opis_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVu-Sans'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3)
    ]))
    elements.append(opis_table)

    # --- STRATIGRAFSKI ODNOSI ---
    strat_data = [
        ["STRATIGRAFSKI ODNOSI", "", ""],
        ["SJ iznad", "000", ""],
        ["SJ ispod", "020", ""],
        ["Sječe", "", ""],
        ["Presječeno od", "", ""],
        ["Zapunjena sa SJ", "", ""],
        ["Zapunjava SJ", "", ""],
        ["Sastavni dio", "", ""],
        ["Povezana sa SJ", "002", ""],
        ["Uz", "001", ""],
        ["Slična s SJ", "", ""]
    ]
    strat_table = Table(strat_data, colWidths=[60 * mm, 60 * mm, 60 * mm], rowHeights=[8 * mm] * 11)
    strat_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('SPAN', (0, 0), (2, 0)),  # Header spans all columns
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVu-Sans'),
        ('FONTNAME', (0, 0), (2, 0), 'DejaVu-Sans-Bold'),  # Header bold
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('LEFTPADDING', (0, 0), (-1, -1), 3)
    ]))
    elements.append(strat_table)

    # --- NALAZI TABLE ---
    nalazi_data = [
        ["Keramika N -", "5, 17, 48", "Ostali nalazi:"],
        ["Opeka    N -", "", ""],
        ["Ljep     N -", "", "Posebni nalazi:"],
        ["Staklo   N -", "", "PN -"],
        ["Metal    N -", "", "Uzorci:"],
        ["Drvo     U -", "", ""],
        ["Ugljen   U-", "3", "Napomene:"],
        ["Kosti    N-", "2, 19, 35", ""]
    ]

    # Create NALAZI as a vertical label
    nalazi_label_data = [
        ["N"], ["A"], ["L"], ["A"], ["Z"], ["I"]
    ]
    nalazi_label_table = Table(nalazi_label_data, colWidths=[10 * mm], rowHeights=[8 * mm] * 6)
    nalazi_label_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVu-Sans-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9)
    ]))

    # Main nalazi table
    nalazi_main_table = Table(nalazi_data, colWidths=[40 * mm, 40 * mm, 90 * mm], rowHeights=[6 * mm] * 8)
    nalazi_main_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVu-Sans'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('SPAN', (2, 0), (2, 1)),  # Ostali nalazi spans 2 rows
        ('SPAN', (2, 2), (2, 3)),  # Posebni nalazi spans 2 rows
        ('SPAN', (2, 4), (2, 5)),  # Uzorci spans 2 rows
        ('SPAN', (2, 6), (2, 7))  # Napomene spans 2 rows
    ]))

    # Combine label and main table
    combined_nalazi_data = [
        [nalazi_label_table, nalazi_main_table]
    ]
    combined_nalazi_table = Table(combined_nalazi_data, colWidths=[10 * mm, 170 * mm])
    combined_nalazi_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ]))
    elements.append(combined_nalazi_table)

    # --- DOCUMENTATION SECTION ---
    doc_data = [
        ["", "Stranica dnevnika\n14", "Arheolog:\nKG"],
        ["Foto: br.", "Snimio:", ""]
    ]
    doc_table = Table(doc_data, colWidths=[60 * mm, 60 * mm, 60 * mm], rowHeights=[15 * mm, 10 * mm])
    doc_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVu-Sans'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3)
    ]))
    elements.append(doc_table)

    elements.append(Spacer(1, 10 * mm))

    # --- FOOTER ---
    footer_text = "Ministarstvo kulture, Uprava za zaštitu kulturne baštine, Odjel za arheološku baštinu"
    footer_para = Paragraph(footer_text, styleSmall)
    elements.append(footer_para)

    # --- PAGE BREAK FOR SKETCHES ---
    elements.append(PageBreak())

    # --- PAGE 2: SKETCHES ---
    # SJ box on second page
    elements.append(Table([["SJ"]], colWidths=[20 * mm], rowHeights=[15 * mm],
                          style=[('GRID', (0, 0), (-1, -1), 1, colors.black),
                                 ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                 ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                 ('FONTNAME', (0, 0), (-1, -1), 'DejaVu-Sans-Bold')]))

    # First sketch section
    sketch1_data = [["SKICA STRATIGRAFSKE JEDINICE"]]
    sketch1_table = Table(sketch1_data, colWidths=[180 * mm], rowHeights=[100 * mm])
    sketch1_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVu-Sans-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3)
    ]))
    elements.append(sketch1_table)

    elements.append(Spacer(1, 5 * mm))

    # Second sketch section with grid
    sketch2_data = [["SKICA POLOŽAJA STRATIGRAFSKE JEDINICE U SONDI / KVADRANTU"]]
    sketch2_header = Table(sketch2_data, colWidths=[180 * mm], rowHeights=[8 * mm])
    sketch2_header.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVu-Sans-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('LEFTPADDING', (0, 0), (-1, -1), 3)
    ]))
    elements.append(sketch2_header)

    # Grid for the sketch (6x4 grid as shown in image)
    grid_data = [["" for _ in range(6)] for _ in range(4)]
    grid_table = Table(grid_data, colWidths=[30 * mm] * 6, rowHeights=[20 * mm] * 4)
    grid_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(grid_table)

    elements.append(Spacer(1, 10 * mm))

    # Footer on second page
    elements.append(Paragraph(footer_text, styleSmall))

    # Build the PDF
    try:
        doc.build(elements)
        iface.messageBar().pushMessage("Uspjeh", f"PDF spremljen: {fileName}", level=0, duration=4)
    except Exception as e:
        iface.messageBar().pushMessage("Greška", f"Greška kod izvoza PDF-a: {e}", level=3, duration=7)