from reportlab.pdfgen import canvas

def hallo(c):
    c.drawString(100, 700, "Hallo dit is mijn eerste PDF.")

c = canvas.Canvas("Eerste PDF")
hallo(c)
c.showPage()
c.save()