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
    Izvozi podatke o arheološkoj stratigrafskoj jedinici u PDF dokument,
    kombinirajući dinamičko dohvaćanje podataka s točnim vizualnim rasporedom.
    """
    # --- DOHVATI SVE PODATKE IZ DIJALOGA ---
    data = dlg.get_data()

    fileName, _ = QFileDialog.getSaveFileName(
        dlg, "Export to PDF", "", "PDF Files (*.pdf)"
    )
    if not fileName:
        return
    if not fileName.endswith('.pdf'):
        fileName += '.pdf'

    # --- REGISTRACIJA FONTOVA ---
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

    # --- STILOVI ---
    styleN = ParagraphStyle('Normal', fontName='DejaVu-Sans', fontSize=9, leading=11)
    styleWrap = ParagraphStyle('Wrap', parent=styleN, alignment=0)
    styleSmall = ParagraphStyle('Small', parent=styleN, fontSize=8, leading=9)

    elements = []

    # --- GORNJI DESNI SJ BOX ---
    sj_box_data = [
        [Paragraph(f"<b>SJ</b><br/>{data.get('SJ_br', '')}", styleN)],
        [Paragraph(f"List br.<br/>{data.get('dnevnik_str', '')}", styleN)]
    ]
    sj_box_table = Table(sj_box_data, colWidths=[20 * mm], rowHeights=[8 * mm, 8 * mm])
    sj_box_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    # --- ZAGLAVLJE SA SJ BOXOM ---
    header_data = [
        [Paragraph(f"STRATIGRAFSKA JEDINICA br. ____{data.get('SJ_br', '')}____",
                   ParagraphStyle('H1', fontName='DejaVu-Sans-Bold', fontSize=11)),
         sj_box_table]
    ]
    header_table = Table(header_data, colWidths=[160 * mm, 20 * mm])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (0, 0), 'BOTTOM'),
        ('VALIGN', (1, 0), (1, 0), 'TOP'),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 3 * mm))

    # --- RED: LOKALITET, VRSTA SJ, DATUM ---
    datum_za_pdf = data.get('datum').toString("d. M. yyyy.") if data.get('datum') else ''
    top_row_data = [
        [Paragraph(f"<b>LOKALITET:</b><br/>{data.get('lokalitet', '')}", styleWrap),
         Paragraph(f"<b>Vrsta SJ:</b><br/>{data.get('SJ_vrsta', '')}", styleWrap),
         Paragraph(f"<b>Datum:</b><br/>{datum_za_pdf}", styleWrap)]
    ]
    top_row_table = Table(top_row_data, colWidths=[90 * mm, 50 * mm, 40 * mm], rowHeights=[12 * mm])
    top_row_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3)
    ]))
    elements.append(top_row_table)

    # --- RED: SONDA, SEKTOR, KVADRAT, VISINA ---
    location_text = (f"Apsolutna visina najviše točke: {data.get('najvisa_tocka', '')}<br/>"
                     f"Visina: {data.get('aps_visina', '')}<br/>"
                     f"Apsolutna visina najniže točke: {data.get('najniza_tocka', '')}")
    location_data = [
        [Paragraph(f"Sonda<br/>{data.get('sonda', '')}", styleWrap),
         Paragraph(f"Sektor<br/>{data.get('sektor', '')}", styleWrap),
         Paragraph(f"Kvadrat<br/>{data.get('kvadrat', '')}", styleWrap),
         Paragraph(location_text, styleWrap)]
    ]
    location_table = Table(location_data, colWidths=[30 * mm, 30 * mm, 30 * mm, 90 * mm], rowHeights=[25 * mm])
    location_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3)
    ]))
    elements.append(location_table)

    # --- TABLICA KARAKTERISTIKA ---
    char_top_data = [
        [Paragraph(f"Sastav: {data.get('sastav', '')}", styleWrap)],
        [Paragraph(f"Konzistencija: {data.get('konzistencija', '')}", styleWrap),
         Paragraph(f"Boja(Munsell):<br/>{data.get('boja_munsell', '')}", styleWrap)],
    ]
    char_top_table = Table(char_top_data, colWidths=[90 * mm, 90 * mm], rowHeights=[10 * mm, 10 * mm])
    char_top_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black), ('SPAN', (0, 0), (1, 0)),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3)
    ]))

    char_bottom_data = [
        [Paragraph(f"Oblik<br/>{data.get('oblik', '')}", styleWrap),
         Paragraph(f"Dužina<br/>{data.get('duzina', '')} m", styleWrap),
         Paragraph(f"Širina<br/>{data.get('sirina', '')} m", styleWrap),
         Paragraph(f"Promjer<br/>{data.get('promjer', '')} m", styleWrap)]
    ]
    char_bottom_table = Table(char_bottom_data, colWidths=[45 * mm, 45 * mm, 45 * mm, 45 * mm], rowHeights=[15 * mm])
    char_bottom_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3)
    ]))

    elements.append(char_top_table)
    elements.append(char_bottom_table)

    # --- SEKCIJA OPIS ---
    opis_data = [[Paragraph(f"<b>OPIS</b><br/>{data.get('opis', '')}", styleWrap)]]
    opis_table = Table(opis_data, colWidths=[180 * mm], rowHeights=[25 * mm])
    opis_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3)
    ]))
    elements.append(opis_table)

    # --- STRATIGRAFSKI ODNOSI ---
    strat_data = [
        [Paragraph("<b>STRATIGRAFSKI ODNOSI</b>", styleN), "", ""],
        [Paragraph("SJ iznad", styleN), Paragraph(data.get('odnosi_iznad', ''), styleN), ""],
        [Paragraph("SJ ispod", styleN), Paragraph(data.get('odnosi_ispod', ''), styleN), ""],
        [Paragraph("Sječe", styleN), Paragraph(data.get('sjece', ''), styleN), ""],
        [Paragraph("Presječeno od", styleN), Paragraph(data.get('presjeceno_od', ''), styleN), ""],
        [Paragraph("Zapunjena sa SJ", styleN), Paragraph(data.get('zapunjena_sa', ''), styleN), ""],
        [Paragraph("Zapunjava SJ", styleN), Paragraph(data.get('zapunjava', ''), styleN), ""],
        [Paragraph("Sastavni dio", styleN), Paragraph(data.get('sastavni_dio', ''), styleN), ""],
        [Paragraph("Povezana sa SJ", styleN), Paragraph(data.get('povezana_sa', ''), styleN), ""],
        [Paragraph("Uz", styleN), Paragraph(data.get('uz', ''), styleN), ""],
        [Paragraph("Slična s SJ", styleN), Paragraph(data.get('slicna_s', ''), styleN), ""]
    ]
    strat_table = Table(strat_data, colWidths=[60 * mm, 60 * mm, 60 * mm], rowHeights=[8 * mm] * 11)
    strat_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('SPAN', (0, 0), (2, 0)),
        ('ALIGN', (0, 0), (2, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 3)
    ]))
    elements.append(strat_table)

    # --- TABLICA NALAZA ---
    def get_finding_text(name, check_key, notes_key):
        checked_char = "X" if data.get(check_key) else "–"
        notes = data.get(notes_key, '')
        return Paragraph(f"{name} [{checked_char}]<br/><i>{notes}</i>", styleWrap)

    nalazi_data = [
        [get_finding_text('Keramika', 'keramika', 'keramika_opis'),
         Paragraph(f"<b>Ostali nalazi:</b><br/>{data.get('ostali_nalazi', '')}", styleWrap)],
        [get_finding_text('Opeka', 'opeka', 'opeka_opis'), ""],
        [get_finding_text('Ljep', 'ljep', 'ljep_opis'),
         Paragraph(f"<b>Posebni nalazi:</b><br/>{data.get('posebni_nalazi', '')}", styleWrap)],
        [get_finding_text('Staklo', 'staklo', 'staklo_opis'), ""],
        [get_finding_text('Metal', 'metal', 'metal_opis'),
         Paragraph(f"<b>Uzorci:</b><br/>{data.get('uzorci', '')}", styleWrap)],
        [get_finding_text('Drvo', 'drvo', 'drvo_opis'), ""],
        [get_finding_text('Ugljen', 'ugljen', 'ugljen_opis'),
         Paragraph(f"<b>Napomene:</b><br/>{data.get('napomene', '')}", styleWrap)],
        [get_finding_text('Kosti', 'kosti', 'kosti_opis'), ""]
    ]

    nalazi_main_table = Table(nalazi_data, colWidths=[90 * mm, 90 * mm], rowHeights=[12 * mm] * 8)
    nalazi_main_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 3), ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('SPAN', (1, 0), (1, 1)), ('SPAN', (1, 2), (1, 3)),
        ('SPAN', (1, 4), (1, 5)), ('SPAN', (1, 6), (1, 7)),
    ]))

    elements.append(nalazi_main_table)

    # --- SEKCIJA DOKUMENTACIJA ---
    doc_data = [
        [Paragraph(f"Stranica dnevnika<br/>{data.get('dnevnik_str', '')}", styleWrap),
         Paragraph(f"Arheolog:<br/>{data.get('arheolog', '')}", styleWrap)],
        [Paragraph(f"Foto: br.<br/>{data.get('foto_br', '')}", styleWrap),
         Paragraph(f"Snimio:<br/>{data.get('snimio', '')}", styleWrap)]
    ]
    doc_table = Table(doc_data, colWidths=[90 * mm, 90 * mm], rowHeights=[15 * mm, 15 * mm])
    doc_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3)
    ]))
    elements.append(doc_table)

    elements.append(Spacer(1, 5 * mm))

    # --- FOOTER ---
    footer_text = "Ministarstvo kulture, Uprava za zaštitu kulturne baštine, Odjel za arheološku baštinu"
    elements.append(Paragraph(footer_text, styleSmall))

    # --- PRIJELOM STRANICE ZA SKICE ---
    elements.append(PageBreak())

    # --- STRANICA 2: SKICE ---
    sj_val = data.get('SJ_br', '')
    elements.append(Table([[f"SJ\n{sj_val}"]], colWidths=[20 * mm], rowHeights=[15 * mm],
                          style=[('GRID', (0, 0), (-1, -1), 1, colors.black),
                                 ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                 ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                 ('FONTNAME', (0, 0), (-1, -1), 'DejaVu-Sans-Bold')]))
    elements.append(Spacer(1, 2 * mm))

    sketch1_data = [[Paragraph("SKICA STRATIGRAFSKE JEDINICE", styleN)]]
    sketch1_table = Table(sketch1_data, colWidths=[180 * mm], rowHeights=[100 * mm])
    sketch1_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 3), ('TOPPADDING', (0, 0), (-1, -1), 3)
    ]))
    elements.append(sketch1_table)
    elements.append(Spacer(1, 5 * mm))

    sketch2_data = [[Paragraph("SKICA POLOŽAJA STRATIGRAFSKE JEDINICE U SONDI / KVADRANTU", styleN)]]
    sketch2_header = Table(sketch2_data, colWidths=[180 * mm], rowHeights=[8 * mm])
    sketch2_header.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 3)
    ]))
    elements.append(sketch2_header)

    grid_data = [["" for _ in range(6)] for _ in range(4)]
    grid_table = Table(grid_data, colWidths=[30 * mm] * 6, rowHeights=[20 * mm] * 4)
    grid_table.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    elements.append(grid_table)
    elements.append(Spacer(1, 5 * mm))

    elements.append(Paragraph(footer_text, styleSmall))

    # --- BUILD DOKUMENTA ---
    try:
        doc.build(elements)
        iface.messageBar().pushMessage("Uspjeh", f"PDF spremljen: {fileName}", level=0, duration=4)
    except Exception as e:
        iface.messageBar().pushMessage("Greška", f"Greška kod izvoza PDF-a: {e}", level=3, duration=7)