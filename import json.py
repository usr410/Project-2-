import json
import os
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

# Voorbeeld factuur JSON (uit de vorige stap)
factuur_json = '''
{
    "factuurnummer": "FACT-2000-096",
    "factuurdatum": "14-10-2023",
    "vervaldatum": "13-06-2020",
    "klant": {
        "naam": "PC Sputnik B.V.",
        "adres": "Schoolstraat 169",
        "postcode": "1128 AA",
        "stad": "Amsterdam",
        "KVK-nummer": "64293189"
    },
    "order": {
        "ordernummer": "2000-096",
        "orderdatum": "14-05-2020"
    },
    "producten": [
        {
            "productnaam": "Google Cloud Platform",
            "aantal": 3,
            "prijs_per_stuk_excl_btw": 494.88,
            "btw_percentage": 6
        }
    ],
    "totaalbedragen": {
        "totaal_excl_btw": 1484.64,
        "btw_bedrag": 89.08,
        "totaal_incl_btw": 1573.72
    }
}
'''

# Laad de factuur JSON
factuur = json.loads(factuur_json)

# Maak de map PDF_INVOICE als deze niet bestaat
output_dir = "PDF_INVOICE"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Map '{output_dir}' is aangemaakt.")
else:
    print(f"Map '{output_dir}' bestaat al.")

# Genereer de PDF-bestandsnaam
pdf_filename = os.path.join(output_dir, f"{factuur['factuurnummer']}.pdf")
print(f"PDF-bestand wordt aangemaakt: {pdf_filename}")

# Maak een PDF-bestand
try:
    doc = SimpleDocTemplate(pdf_filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Titel
    story.append(Paragraph("Factuur", styles['Title']))
    story.append(Spacer(1, 12))

    # Factuurgegevens
    factuur_gegevens = [
        ["Factuurnummer:", factuur["factuurnummer"]],
        ["Factuurdatum:", factuur["factuurdatum"]],
        ["Vervaldatum:", factuur["vervaldatum"]]
    ]
    story.append(Table(factuur_gegevens, colWidths=[100, 200]))
    story.append(Spacer(1, 12))

    # Klantgegevens
    klant_gegevens = [
        ["Klantnaam:", factuur["klant"]["naam"]],
        ["Adres:", factuur["klant"]["adres"]],
        ["Postcode:", factuur["klant"]["postcode"]],
        ["Stad:", factuur["klant"]["stad"]],
        ["KVK-nummer:", factuur["klant"]["KVK-nummer"]]
    ]
    story.append(Table(klant_gegevens, colWidths=[100, 200]))
    story.append(Spacer(1, 12))

    # Ordergegevens
    order_gegevens = [
        ["Ordernummer:", factuur["order"]["ordernummer"]],
        ["Orderdatum:", factuur["order"]["orderdatum"]]
    ]
    story.append(Table(order_gegevens, colWidths=[100, 200]))
    story.append(Spacer(1, 12))

    # Producttabel
    product_headers = ["Productnaam", "Aantal", "Prijs per stuk (excl. BTW)", "BTW Percentage", "Totaal (excl. BTW)"]
    product_data = [product_headers]

    for product in factuur["producten"]:
        totaal_excl_btw = product["aantal"] * product["prijs_per_stuk_excl_btw"]
        product_data.append([
            product["productnaam"],
            str(product["aantal"]),
            f"€{product['prijs_per_stuk_excl_btw']:.2f}",
            f"{product['btw_percentage']}%",
            f"€{totaal_excl_btw:.2f}"
        ])

    product_table = Table(product_data, colWidths=[120, 60, 120, 80, 100])
    product_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(product_table)
    story.append(Spacer(1, 12))

    # Totaalbedragen
    totaal_gegevens = [
        ["Totaalbedrag (excl. BTW):", f"€{factuur['totaalbedragen']['totaal_excl_btw']:.2f}"],
        ["BTW-bedrag:", f"€{factuur['totaalbedragen']['btw_bedrag']:.2f}"],
        ["Totaalbedrag (incl. BTW):", f"€{factuur['totaalbedragen']['totaal_incl_btw']:.2f}"]
    ]
    story.append(Table(totaal_gegevens, colWidths=[150, 100]))
    story.append(Spacer(1, 12))

    # Bouw de PDF
    doc.build(story)
    print(f"Factuur PDF is succesvol aangemaakt: {pdf_filename}")

except Exception as e:
    print(f"Fout tijdens het aanmaken van de PDF: {e}")