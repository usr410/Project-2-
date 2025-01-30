import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

output_dir = "PDF_INVOICE"

# Unieke naam generator
def generate_unique_filename(output_dir, base_name):
    i = 1
    while True:
        output_path = os.path.join(output_dir, f"{base_name}{i}.pdf")
        if not os.path.exists(output_path):
            return output_path
        i += 1  

# Pad naar de PDF
output_path = generate_unique_filename(output_dir, "lege_factuur")

# pdf aan maken
def create_invoice(pdf_path):
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    # Titel
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 50, "FACTUUR")

    # Bedrijfsgegevens
    c.setFont("Helvetica", 10)
    company_info = [
        "NovaTech Solutions B.V.", "Innovatieplein 12", "1012 AB Amsterdam",
        "KVK: 87654321", "BTW: NL003456789B01",
        "IBAN: NL91ABNA0417164300", "Telefoon: +31 20 123 4567",
        "E-mail: info@novatechsolutions.nl", "Website: www.novatechsolutions.nl"
    ]
    y = height - 80
    for line in company_info:
        c.drawString(50, y, line)
        y -= 15

    c.line(50, y, width - 50, y)
    y -= 20

    # Factuurgegevens
    invoice_info = [
        "Factuurnummer: NT-20240101", "Factuurdatum: 29 januari 2025",
        "Vervaldatum: 12 februari 2025"
    ]
    for line in invoice_info:
        c.drawString(50, y, line)
        y -= 15

    # Klantgegevens
    c.drawString(50, y - 10, "Factuur aan:")
    y -= 25
    client_info = ["[Naam Klant]", "[Bedrijfsnaam Klant]", "[Adres Klant]", "[Postcode & Plaats]", "[BTW-nummer Klant]"]
    for line in client_info:
        c.drawString(50, y, line)
        y -= 15

    c.line(50, y, width - 50, y)
    y -= 20

    # Factuurregels
    c.drawString(50, y, "Omschrijving van de diensten/producten:")
    y -= 20
    headers = ["Aantal", "Omschrijving", "Prijs per stuk", "Totaal"]
    x_positions = [50, 120, 350, 450]
    for i, header in enumerate(headers):
        c.drawString(x_positions[i], y, header)
    y -= 10
    c.line(50, y, width - 50, y)
    y -= 20

    for _ in range(3):
        values = ["0", "", "€ 0", "€ 0"]
        for i, value in enumerate(values):
            c.drawString(x_positions[i], y, value)
        y -= 15

    y -= 20
    totals = ["Subtotaal: € 0", "BTW (21%): € 0", "Totaalbedrag: € 0"]
    for line in totals:
        c.drawString(50, y, line)
        y -= 15

    c.line(50, y, width - 50, y)
    y -= 20

    # Betalingsgegevens
    c.drawString(50, y, "Betalingsgegevens:")
    y -= 20
    payment_info = [
        "Gelieve het totaalbedrag van € 0 over te maken naar onderstaand rekeningnummer onder vermelding van het factuurnummer.",
        "IBAN: NL91ABNA0417164300", "BIC: ABNANL2A", "Ten name van: NovaTech Solutions B.V."
    ]
    for line in payment_info:
        c.drawString(50, y, line)
        y -= 15

    c.line(50, y, width - 50, y)
    y -= 20

    # Opmerkingen
    c.drawString(50, y, "Opmerkingen:")
    y -= 20
    notes = [
        "• Bij vragen over deze factuur kunt u contact met ons opnemen via info@novatechsolutions.nl of +31 20 123 4567.",
        "• Betaling dient binnen 14 dagen na factuurdatum te geschieden.",
        "• Na de vervaldatum kunnen incassokosten in rekening worden gebracht.",
        "Bedankt voor uw samenwerking!"
    ]
    for line in notes:
        c.drawString(50, y, line)
        y -= 15

    # opslaan pfd
    c.save()
    print(f"Factuur gegenereerd: {pdf_path}")

create_invoice(output_path)
