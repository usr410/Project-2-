from reportlab.pdfgen import canvas

def hallo(c):
    tekst = input("Voer een stuk tekst in. ")
    c.drawString(100, 700, tekst)

c = canvas.Canvas("Eerste PDF.pdf")
hallo(c)
c.showPage()
c.save()