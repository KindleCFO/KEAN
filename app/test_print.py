from __future__ import print_function

import csv

pagedata = []

with open('data/Lightstone_Daily.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')

    for row in reader:
        pagedata.append(row)

#print(str(pagedata[0][0]))


reportwidth = 0
row2 = pagedata[0]
for col2 in row2:
    reportwidth +=  int(col2)

#print(str(reportwidth))


#Landscape letter should be 792 x 612

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors

c = canvas.Canvas("Lightstone Daily P&L.pdf", pagesize=landscape(letter))

topmargin = 10
bottommargin = 10
leftmargin = 10
rightmargin = 10
pagewidth = 792
pageheight = 612

scalingfactorwidth = (pagewidth - leftmargin - rightmargin) / reportwidth

title = 'Lightstone Daily P&L Report'
c.setFont("Helvetica",12)

c.drawString(leftmargin, pageheight-topmargin-12, title)

#c.setFont("Helvetica",7)
#c.drawString(leftmargin, (pageheight-topmargin-24), "Hello")

#someday calc appropriate font size to use based on rows


c.setFont("Helvetica",5)
rowheight = 7
sectionrow = 0
titlespacer = 23
sectionstart = pageheight - topmargin -titlespacer

#yellow highlights
c.setFillColorRGB(1,1,0)
c.rect(leftmargin, sectionstart-rowheight-1, pagewidth-leftmargin-rightmargin,7, fill=1)
c.rect(leftmargin, sectionstart-31*rowheight-1, pagewidth-leftmargin-rightmargin,7, fill=1)
c.rect(leftmargin, sectionstart-44*rowheight-1, pagewidth-leftmargin-rightmargin,7, fill=1)
c.rect(leftmargin, sectionstart-60*rowheight-1, pagewidth-leftmargin-rightmargin,7, fill=1)
c.rect(leftmargin, sectionstart-64*rowheight-1, pagewidth-leftmargin-rightmargin,7, fill=1)

#navy blue hightlights
c.setFillColorRGB(0,0,128/255)
c.rect(leftmargin, sectionstart-rowheight-2, pagewidth-leftmargin-rightmargin,7, fill=1)
c.rect(leftmargin, sectionstart-9*rowheight-1, pagewidth-leftmargin-rightmargin,7, fill=1)
c.rect(leftmargin, sectionstart-13*rowheight-1, pagewidth-leftmargin-rightmargin,7, fill=1)
c.rect(leftmargin, sectionstart-20*rowheight-1, pagewidth-leftmargin-rightmargin,7, fill=1)
c.rect(leftmargin, sectionstart-24*rowheight-1, pagewidth-leftmargin-rightmargin,7, fill=1)
c.rect(leftmargin, sectionstart-29*rowheight-1, pagewidth-leftmargin-rightmargin,7, fill=1)
c.rect(leftmargin, sectionstart-32*rowheight-1, pagewidth-leftmargin-rightmargin,7, fill=1)
c.rect(leftmargin, sectionstart-35*rowheight-1, pagewidth-leftmargin-rightmargin,7, fill=1)
c.rect(leftmargin, sectionstart-39*rowheight-1, pagewidth-leftmargin-rightmargin,7, fill=1)
c.rect(leftmargin, sectionstart-41*rowheight-1, pagewidth-leftmargin-rightmargin,7, fill=1)
c.rect(leftmargin, sectionstart-71*rowheight-1, pagewidth-leftmargin-rightmargin,7, fill=1)
c.rect(leftmargin, sectionstart-73*rowheight-1, pagewidth-leftmargin-rightmargin,7, fill=1)
c.rect(leftmargin, sectionstart-76*rowheight-1, pagewidth-leftmargin-rightmargin,7, fill=1)

#green
c.setFillColorRGB(47/255,211/255,76/255)
c.rect(leftmargin, sectionstart-78*rowheight-2, pagewidth-leftmargin-rightmargin,7, fill=1)



c.setFillColor(colors.black)

for reportrow in pagedata[1:]:
    c.drawString(leftmargin, (sectionstart-sectionrow*rowheight), reportrow[0])
    #add next columns - need to use the columnwidth data to determine where to start cols
    sectionrow += 1



c.save()
