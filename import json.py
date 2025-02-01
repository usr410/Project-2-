import json
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

# Bedrijfsgegevens
bedrijfsgegevens = {
    "naam": "NovaTech Solutions B.V.",
    "adres": "Innovatieplein 12",
    "postcode": "1012 AB",
    "stad": "Amsterdam",
    "KVK": "87654321",
    "BTW": "NL003456789B01",
    "IBAN": "NL91ABNA0417164300",
    "telefoon": "+31 20 123 4567",
    "email": "info@novatechsolutions.nl",
    "website": "www.novatechsolutions.nl"
}

factuur_dir = "Project-2-\\JSON_INVOICE"

for filename in os.listdir(factuur_dir):
    if filename.endswith(".json"):
        factuur = os.path.join(factuur_dir, filename)
        with open(factuur) as fax:
            factuur_data = json.load(fax)
# Functie om JSON-bestand in te laden
def laad_json_bestand(bestandsnaam):
    with open(bestandsnaam, 'r') as file:
        return json.load(file)

# Laad de factuurgegevens uit het JSON-bestand
bestandsnaam = "2000-096.json"  # Vervang dit door het pad naar je JSON-bestand
factuur = laad_json_bestand(bestandsnaam)

# Bereken de totaalbedragen
subtotaal = sum(product["aantal"] * product["prijs_per_stuk_excl_btw"] for product in factuur["order"]["producten"])
btw_bedrag = sum(product["aantal"] * product["prijs_per_stuk_excl_btw"] * (product["btw_percentage"] / 100) for product in factuur["order"]["producten"])
totaal_incl_btw = subtotaal + btw_bedrag

# Voeg de totaalbedragen toe aan de factuurgegevens
factuur["totaalbedragen"] = {
    "subtotaal": subtotaal,
    "btw_bedrag": btw_bedrag,
    "totaal_incl_btw": totaal_incl_btw
}

# Maak de map PDF_INVOICE als deze niet bestaat
output_dir = "PDF_INVOICE"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Map '{output_dir}' is aangemaakt.")
else:
    print(f"Map '{output_dir}' bestaat al.")

# Genereer de PDF-bestandsnaam
pdf_filename = os.path.join(output_dir, f"{factuur['order']['ordernummer']}.pdf")
print(f"PDF-bestand wordt aangemaakt: {pdf_filename}")

# Maak een PDF-bestand
try:
    doc = SimpleDocTemplate(pdf_filename, pagesize=A4)
    styles = getSampleStyleSheet()

    # Aangepaste stijl voor links uitgelijnde tekst
    left_align_style = ParagraphStyle(
        name='LeftAlign',
        parent=styles['Normal'],
        alignment=0,  # 0 = links, 1 = gecentreerd, 2 = rechts
        fontSize=10,
        spaceAfter=12
    )

    story = []

    # Bedrijfsgegevens
    bedrijfs_info = [
        [Paragraph(bedrijfsgegevens["naam"], styles['Heading1'])],
        [Paragraph(bedrijfsgegevens["adres"], left_align_style)],
        [Paragraph(f"{bedrijfsgegevens['postcode']} {bedrijfsgegevens['stad']}", left_align_style)],
        [Paragraph(f"KVK: {bedrijfsgegevens['KVK']}", left_align_style)],
        [Paragraph(f"BTW: {bedrijfsgegevens['BTW']}", left_align_style)],
        [Paragraph(f"IBAN: {bedrijfsgegevens['IBAN']}", left_align_style)],
        [Paragraph(f"Telefoon: {bedrijfsgegevens['telefoon']}", left_align_style)],
        [Paragraph(f"E-mail: {bedrijfsgegevens['email']}", left_align_style)],
        [Paragraph(f"Website: {bedrijfsgegevens['website']}", left_align_style)]
    ]
    story.append(Table(bedrijfs_info, colWidths=[400]))
    story.append(Spacer(1, 24))

    # Factuurgegevens
    factuur_gegevens = [
        [Paragraph("Factuurnummer:", left_align_style), Paragraph(factuur["order"]["ordernummer"], left_align_style)],
        [Paragraph("Orderdatum:", left_align_style), Paragraph(factuur["order"]["orderdatum"], left_align_style)],
        [Paragraph("Betaaltermijn:", left_align_style), Paragraph(factuur["order"]["betaaltermijn"], left_align_style)]
    ]
    story.append(Table(factuur_gegevens, colWidths=[100, 300]))
    story.append(Spacer(1, 24))

    # Klantgegevens
    klant_gegevens = [
        [Paragraph("Factuur aan:", left_align_style)],
        [Paragraph(factuur["order"]["klant"]["naam"], left_align_style)],
        [Paragraph(factuur["order"]["klant"]["adres"], left_align_style)],
        [Paragraph(factuur["order"]["klant"]["postcode"], left_align_style)],
        [Paragraph(factuur["order"]["klant"]["stad"], left_align_style)],
        [Paragraph(f"KVK-nummer: {factuur['order']['klant']['KVK-nummer']}", left_align_style)]
    ]
    story.append(Table(klant_gegevens, colWidths=[400]))
    story.append(Spacer(1, 24))

    # Producttabel (zoals in de afbeelding)
    product_headers = ["Aantal", "Omschrijving", "Prijs per stuk", "Totaal"]
    product_data = [product_headers]

    for product in factuur["order"]["producten"]:
        totaal = product["aantal"] * product["prijs_per_stuk_excl_btw"]
        product_data.append([
            str(product["aantal"]),
            product["productnaam"],
            f"€{product['prijs_per_stuk_excl_btw']:.2f}",
            f"€{totaal:.2f}"
        ])

    product_table = Table(product_data, colWidths=[60, 200, 100, 100])
    product_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Links uitlijnen
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header vetgedrukt
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Ruimte onder de header
        ('GRID', (0, 0), (-1, -1), 1, colors.black)  # Zwarte randen
    ]))
    story.append(product_table)
    story.append(Spacer(1, 24))

    # Totaalbedragen (eenvoudige opmaak)
    totaal_gegevens = [
        [Paragraph("Subtotaal:", left_align_style), Paragraph(f"€{factuur['totaalbedragen']['subtotaal']:.2f}", left_align_style)],
        [Paragraph(f"BTW ({factuur['order']['producten'][0]['btw_percentage']}%):", left_align_style), Paragraph(f"€{factuur['totaalbedragen']['btw_bedrag']:.2f}", left_align_style)],
        [Paragraph("Totaalbedrag:", left_align_style), Paragraph(f"€{factuur['totaalbedragen']['totaal_incl_btw']:.2f}", left_align_style)]
    ]
    story.append(Table(totaal_gegevens, colWidths=[100, 100]))
    story.append(Spacer(1, 24))

    # Betalingsgegevens (eenvoudige opmaak)
    betalings_info = [
        [Paragraph("Betalingsgegevens:", left_align_style)],
        [Paragraph("Gelieve het totaalbedrag over te maken naar:", left_align_style)],
        [Paragraph(f"IBAN: {bedrijfsgegevens['IBAN']}", left_align_style)],
        [Paragraph("Ten name van: NovaTech Solutions B.V.", left_align_style)]
    ]
    story.append(Table(betalings_info, colWidths=[400]))
    story.append(Spacer(1, 24))

    # Opmerkingen (eenvoudige opmaak)
    opmerkingen = [
        [Paragraph("Opmerkingen:", left_align_style)],
        [Paragraph("- Bij vragen over deze factuur kunt u contact met ons opnemen via info@novatechsolutions.nl of +31 20 123 4567.", left_align_style)],
        [Paragraph(f"- Betaling dient binnen {factuur['order']['betaaltermijn']} na factuurdatum te geschieden.", left_align_style)],
        [Paragraph("- Na de vervaldatum kunnen incassokosten in rekening worden gebracht.", left_align_style)]
    ]
    story.append(Table(opmerkingen, colWidths=[400]))
    story.append(Spacer(1, 24))

    # Bedankt voor uw samenwerking
    story.append(Paragraph("Bedankt voor uw samenwerking!", styles['Title']))

    # Bouw de PDF
    doc.build(story)
    print(f"Factuur PDF is succesvol aangemaakt: {pdf_filename}")

except Exception as e:
    print(f"Fout tijdens het aanmaken van de PDF: {e}")