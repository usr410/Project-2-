import json
import os
import shutil
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

# Mappen
factuur_dir = r"C:\school\code\projecten\Project-2-\\JSON_INVOICE" 
pdf_dir = r"C:\school\code\projecten\Project-2-\\PDF_INVOICE"     
error_dir = r"C:\school\code\projecten\Project-2-\\JSON_ORDER_ERROR" 


os.makedirs(pdf_dir, exist_ok=True)
os.makedirs(error_dir, exist_ok=True)

#JSON-bestand laden
def laad_json_bestand(bestandsnaam):
    with open(bestandsnaam, 'r') as file:
        return json.load(file)

#PDF genereren
def genereer_pdf(factuur_data, pdf_filename):
    try:
        doc = SimpleDocTemplate(pdf_filename, pagesize=A4)
        styles = getSampleStyleSheet()

        left_align_style = ParagraphStyle(
            name='LeftAlign',
            parent=styles['Normal'],
            alignment=0,
            fontSize=10,
            spaceAfter=12
        )

        story = []

        # Bedrijfsgegevens
        bedrijfsgegevens = factuur_data.get("Bedrijfsgegevens", {})
        bedrijfs_info = [
            [Paragraph(bedrijfsgegevens.get("Bedrijfsnaam", "NovaTech Solutions B.V."), styles['Heading1'])],
            [Paragraph(bedrijfsgegevens.get("Bedrijfsadres", "Innovatieplein 12"), left_align_style)],
            [Paragraph(bedrijfsgegevens.get("Postcode & Plaats", "1012 AB Amsterdam"), left_align_style)],
            [Paragraph(f"KVK: {bedrijfsgegevens.get('KVK nummer', 'KVK87654321')}", left_align_style)],
            [Paragraph(f"BTW: {bedrijfsgegevens.get('BTW nummer', 'NL003456789B01')}", left_align_style)],
            [Paragraph(f"IBAN: {bedrijfsgegevens.get('IBAN', 'NL91ABNA0417164300')}", left_align_style)],
            [Paragraph(f"Telefoon: {bedrijfsgegevens.get('Telefoonnummer', '+31 20 123 4567')}", left_align_style)],
            [Paragraph(f"E-mail: {bedrijfsgegevens.get('E-mail', 'info@novatechsolutions.nl')}", left_align_style)],
            [Paragraph(f"Website: {bedrijfsgegevens.get('Website', 'www.novatechsolutions.nl')}", left_align_style)]
        ]
        story.append(Table(bedrijfs_info, colWidths=[400]))
        story.append(Spacer(1, 24))

        # Factuurgegevens
        factuur_gegevens = [
            [Paragraph("Factuurnummer:", left_align_style), Paragraph(factuur_data["order"]["ordernummer"], left_align_style)],
            [Paragraph("Orderdatum:", left_align_style), Paragraph(factuur_data["order"]["orderdatum"], left_align_style)],
            [Paragraph("Betaaltermijn:", left_align_style), Paragraph(factuur_data["order"]["betaaltermijn"], left_align_style)]
        ]
        story.append(Table(factuur_gegevens, colWidths=[100, 300]))
        story.append(Spacer(1, 24))

        # Klantgegevens
        klant_gegevens = [
            [Paragraph("Factuur aan:", left_align_style)],
            [Paragraph(factuur_data["order"]["klant"]["naam"], left_align_style)],
            [Paragraph(factuur_data["order"]["klant"]["adres"], left_align_style)],
            [Paragraph(factuur_data["order"]["klant"]["postcode"], left_align_style)],
            [Paragraph(factuur_data["order"]["klant"]["stad"], left_align_style)],
            [Paragraph(f"KVK-nummer: {factuur_data['order']['klant']['KVK-nummer']}", left_align_style)]
        ]
        story.append(Table(klant_gegevens, colWidths=[400]))
        story.append(Spacer(1, 24))

        # Producttabel
        product_headers = ["Aantal", "Omschrijving", "Prijs per stuk", "Totaal"]
        product_data = [product_headers]

        for product in factuur_data["order"]["producten"]:
            totaal = product["aantal"] * product["prijs_per_stuk_excl_btw"]
            product_data.append([
                str(product["aantal"]),
                product["productnaam"],
                f"€{product['prijs_per_stuk_excl_btw']:.2f}",
                f"€{totaal:.2f}"
            ])

        product_table = Table(product_data, colWidths=[60, 200, 100, 100])
        product_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  
            ('GRID', (0, 0), (-1, -1), 1, colors.black)  
        ]))
        story.append(product_table)
        story.append(Spacer(1, 24))

        # Totaalbedragen
        totaal_gegevens = [
            [Paragraph("Subtotaal:", left_align_style), Paragraph(f"€{factuur_data['order']['subtotaal']:.2f}", left_align_style)],
            [Paragraph(f"BTW ({factuur_data['order']['producten'][0]['btw_percentage']}%):", left_align_style), Paragraph(f"€{factuur_data['order']['btw(21.0%)']:.2f}", left_align_style)],
            [Paragraph("Totaalbedrag:", left_align_style), Paragraph(f"€{factuur_data['order']['totaalbedrag']:.2f}", left_align_style)]
        ]
        story.append(Table(totaal_gegevens, colWidths=[100, 100]))
        story.append(Spacer(1, 24))

        # Betalingsgegevens
        betalings_info = [
            [Paragraph("Betalingsgegevens:", left_align_style)],
            [Paragraph("Gelieve het totaalbedrag over te maken naar:", left_align_style)],
            [Paragraph(f"IBAN: {bedrijfsgegevens.get('IBAN', 'NL91ABNA0417164300')}", left_align_style)],
            [Paragraph("Ten name van: NovaTech Solutions B.V.", left_align_style)]
        ]
        story.append(Table(betalings_info, colWidths=[400]))
        story.append(Spacer(1, 24))


        opmerkingen = [
            [Paragraph("Opmerkingen:", left_align_style)],
            [Paragraph("- Bij vragen over deze factuur kunt u contact met ons opnemen via info@novatechsolutions.nl of +31 20 123 4567.", left_align_style)],
            [Paragraph(f"- Betaling dient binnen {factuur_data['order']['betaaltermijn']} na factuurdatum te geschieden.", left_align_style)],
            [Paragraph("- Na de vervaldatum kunnen incassokosten in rekening worden gebracht.", left_align_style)]
        ]
        story.append(Table(opmerkingen, colWidths=[400]))
        story.append(Spacer(1, 24))

        story.append(Paragraph("Bedankt voor uw samenwerking!", styles['Title']))

        doc.build(story)
        print(f"PDF succesvol aangemaakt: {pdf_filename}")

    except Exception as e:
        print(f"Fout tijdens het aanmaken van de PDF {pdf_filename}: {e}")
        raise

# Verwerk alle JSON-bestanden in de map
for filename in os.listdir(factuur_dir):
    if filename.endswith(".json"):
        factuur_path = os.path.join(factuur_dir, filename)
        try:
            # Laad de JSON-data
            factuur_data = laad_json_bestand(factuur_path)

            # Genereer de PDF-bestandsnaam
            pdf_filename = os.path.join(pdf_dir, f"{factuur_data['order']['ordernummer']}.pdf")

            # Genereer de PDF
            genereer_pdf(factuur_data, pdf_filename)

        except Exception as e:
            print(f"Fout bij het verwerken van {filename}: {e}")
            # Verplaats het foutieve bestand naar de error-map
            error_path = os.path.join(error_dir, filename)
            shutil.move(factuur_path, error_path)
            print(f"Bestand verplaatst naar: {error_path}")