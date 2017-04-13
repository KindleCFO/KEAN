#Fourteen fonts come standard with reportlab
#   Helvetica (-Bold, -Oblique, -BoldOblique), Times(-Roman, -Bold,-Italic,-BoldItalic), Courier (-Bold, -Oblique, -BoldOblique), ,



from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.utils import ImageReader

c = canvas.Canvas("hello.pdf", pagesize=landscape(letter))

leftEdge = 10
'''
for i in range(0,1000,50):
    c.setFont("Times-Roman", 14)
    c.drawString(i,300,str(i))
'''

c.setFont("Helvetica",7)
c.drawString(leftEdge, 570, "Market Date")
c.drawString(leftEdge, 563, "Market Spreads")
c.drawString(leftEdge, 556, "Spark Spread Dayton Hub (7.2 HR)")
c.drawString(leftEdge, 549, "   Spark Spread On-Peak")



c.save()
