#!/usr/bin/python
# -*- coding: utf-8 -*-

appName = "txt2pdf (version 1.0)"

import argparse

import reportlab.lib.pagesizes
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def readDocument(infile, nChars):
    with open(infile, 'r') as f:
        nbr = 0
        for l0 in f:
            l = l0.decode("utf-8")
            nbr += 1
            l = l[:-1] # remove trailing newspace \n character
            if len(l) > nChars:
                print("Warning: wrapping line "+str(nbr) + " in " + infile)
                while len(l) > nChars:
                    yield l[:nChars]
                    l = l[nChars:]
            yield l

def newpage(c, font, fontsize, top, mleft, leading0, kerning):
    textobject = c.beginText()
    textobject.setFont(font, fontsize, leading=leading0)
    textobject.setTextOrigin(mleft, top)
    textobject.setCharSpace( kerning )
    return textobject

def document(data, outfile, font, fontsize, top, mleft, lpp, leading, kerning):
    p,l = 1, 0
    t = newpage(c, font, fontsize, top, mleft, leading, kerning)
    for line in data:
        t.textLine(line)
        l += 1
        if l == lpp:
            c.drawText(t)
            c.showPage()
            l = 0
            p += 1
            t = newpage(c, font, fontsize, top, mleft, leading, kerning)
    if l > 0:
        c.drawText(t)
    else:
        p -= 1
    c.save()
    print("PDF document: "+str(p)+" pages")


parser = argparse.ArgumentParser()
parser.add_argument('filename')
parser.add_argument('--font', '-f', nargs=1,
                    help='Select a font (True Type format) by its full path')
parser.add_argument('--size', '-s', nargs=1,
                    help='Size of the font')
parser.add_argument('--extra-vertical-space', '-v', nargs=1,
                    help='Extra vertical space between lines')
parser.add_argument('--kerning', '-k', nargs=1,
                    help='Extra horizontal space between characters')
parser.add_argument('--media', '-m', nargs=1,
                    help='Select the size of the page (A4, A3, etc.)')
parser.add_argument('--landscape', '-ls', action="store_true", default=False,
                    help='Select landscape mode')
parser.add_argument('--margin-left', '-l', nargs=1,
                    help='Left margin (in cm unit)')
parser.add_argument('--margin-right', '-r', nargs=1,
                    help='Right margin (in cm unit)')
parser.add_argument('--margin-top', '-t', nargs=1,
                    help='Top margin (in cm unit)')
parser.add_argument('--margin-bottom', '-b', nargs=1,
                    help='Bottom margin (in cm unit)')
parser.add_argument('--output', '-o', nargs=1,
                    help='Output file')
parser.add_argument('--author', nargs=1,
                    help='Author of the PDF document')
parser.add_argument('--title', nargs=1,
                    help='Title of the PDF document')

args = parser.parse_args()

if args.media:
    myPageSize = eval("reportlab.lib.pagesizes." + args.media[0])
else:
    myPageSize = reportlab.lib.pagesizes.A4

if args.landscape:
    myPageSize = reportlab.lib.pagesizes.landscape(myPageSize)

if args.margin_left:
    mLeft = float(args.margin_left[0])*cm
else:
    mLeft = 2*cm
if args.margin_right:
    mRight = float(args.margin_right[0])*cm
else:
    mRight = 2*cm
if args.margin_top:
    mTop = float(args.margin_top[0])*cm
else:
    mTop = 2*cm
if args.margin_bottom:
    mBottom = float(args.margin_bottom[0])*cm
else:
    mBottom = 2*cm

if args.output:
    outFile = args.output[0]
else:
    outFile = "output.pdf"

if args.author:
    author = args.author[0]
else:
    author = None
if args.title:
    title = args.title[0]
else:
    title = None

if args.size:
    fs = float(args.size[0])
else:
    fs = 10

if args.extra_vertical_space:
    leading = float(args.extra_vertical_space[0]) + 1.2*fs
else:
    leading = None

if args.kerning:
    kerning = float(args.kerning[0])
else:
    kerning = 0

if args.font:
    fn = 'myFont'
    pdfmetrics.registerFont(TTFont('myFont', args.font[0]))
else:
    fn = 'Courier'

c = canvas.Canvas(outFile, pagesize=myPageSize)
c.setCreator(appName)

if author:
    c.setAuthor(author)
if title:
    c.setTitle(title)

width = myPageSize[0] - mLeft - mRight
w = c.stringWidth(".", fontName=fn, fontSize=fs)
nChars = int( ( width + kerning ) / ( w + kerning ) )

top = myPageSize[1] - mTop - fs
if leading:
    nLines = int ( ( leading + myPageSize[1] - mTop - mBottom - fs ) / (leading) )
else:
    nLines = int ( ( 1.2*fs + myPageSize[1] - mTop - mBottom - fs ) / (1.2*fs) )

data = readDocument(args.filename, nChars)

print("Printing '"+args.filename+"' with "+str(nChars)+" characters per line"
      + " and "+str(nLines)+" lines per page...")
document(data, outFile, fn, fs, top, mLeft, nLines, leading, kerning)
