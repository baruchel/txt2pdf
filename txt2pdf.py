#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

import reportlab.lib.pagesizes
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib import units
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


class Margins(object):
    def __init__(self, right, left, top, bottom):
        self._right = right
        self._left = left
        self._top = top
        self._bottom = bottom

    @property
    def right(self):
        return self._right * units.cm

    @property
    def left(self):
        return self._left * units.cm

    @property
    def top(self):
        return self._top * units.cm

    @property
    def bottom(self):
        return self._bottom * units.cm


class PDFCreator(object):
    appName = "txt2pdf (version 1.0)"

    def __init__(self, args, margins):
        pageWidth, pageHeight = reportlab.lib.pagesizes.__dict__[args.media]
        if args.landscape:
            pageWidth, pageHeight = reportlab.lib.pagesizes.landscape(
                (pageWidth, pageHeight))
        self.author = args.author
        self.title = args.title
        self.canvas = Canvas(args.output, pagesize=(pageWidth, pageHeight))
        self.canvas.setCreator(self.appName)
        if len(args.author) > 0:
            self.canvas.setAuthor(args.author)
        if len(args.title) > 0:
            self.canvas.setTitle(args.title)
        self.fontSize = args.font_size
        if args.font not in ('Courier'):
            self.font = 'myFont'
            pdfmetrics.registerFont(TTFont('myFont', args.font))
        else:
            self.font = args.font
        self.kerning = args.kerning
        self.margins = margins

        width = pageWidth - margins.left - margins.right
        w = self.canvas.stringWidth(
            ".", fontName=self.font, fontSize=self.fontSize)
        charsPerLine = int((width + self.kerning) / (w + self.kerning))
        self.leading = self._leading(args.extra_vertical_space)

        top = pageHeight - margins.top - self.fontSize
        if self.leading:
            linesPerPage = int(
                (self.leading + pageHeight - margins.top - margins.bottom - self.fontSize) / leading)
        else:
            linesPerPage = int(
                (1.2*self.fontSize + pageHeight - margins.top - margins.bottom - self.fontSize) / (1.2*self.fontSize))

        print(
            "Printing '%s' with %d characters per line and %d lines per page..." %
            (args.filename, charsPerLine, linesPerPage)
        )

        self.document(
            self.readDocument(args.filename, charsPerLine), top, linesPerPage)

    def _leading(self, extraVerticalSpace):
        if extraVerticalSpace:
            return (float(args.extra_vertical_space) + 1.2) * self.fontSize
        return None

    def readDocument(self, infile, maxCharsPerLine):
        with open(infile, 'r') as data:
            lineno = 0
            for line in data:
                line = line.decode('utf8').rstrip('\r\n')
                lineno += 1
                if len(line) > maxCharsPerLine:
                    print("Warning: wrapping line %d in %s" % (lineno, infile))
                    while len(line) > maxCharsPerLine:
                        yield line[:maxCharsPerLine]
                        line = line[maxCharsPerLine:]
                yield line

    def newpage(self, top):
        textobject = self.canvas.beginText()
        textobject.setFont(self.font, self.fontSize, leading=self.leading)
        textobject.setTextOrigin(self.margins.left, top)
        textobject.setCharSpace(self.kerning)
        return textobject

    def document(self, data, top, lpp):
        page, l = 1, 0
        t = self.newpage(top)
        for line in data:
            t.textLine(line)
            l += 1
            if l == lpp:
                self.canvas.drawText(t)
                self.canvas.showPage()
                l = 0
                page += 1
                t = self.newpage(top)
        if l > 0:
            self.canvas.drawText(t)
        else:
            page -= 1
        self.canvas.save()
        print("PDF document: " + str(page) + " pages")


parser = argparse.ArgumentParser()
parser.add_argument('filename')
parser.add_argument('--font', '-f', default='Courier',
                    help='Select a font (True Type format) by its full path')
parser.add_argument('--font-size', '-s', type=float, default=10.0,
                    help='Size of the font')
parser.add_argument('--extra-vertical-space', '-v',
                    help='Extra vertical space between lines')
parser.add_argument('--kerning', '-k', type=float, default=0.0,
                    help='Extra horizontal space between characters')
parser.add_argument('--media', '-m', default='A4',
                    help='Select the size of the page (A4, A3, etc.)')
parser.add_argument('--landscape', '-ls', action="store_true", default=False,
                    help='Select landscape mode')
parser.add_argument('--margin-left', '-l', type=float, default=2.0,
                    help='Left margin (in cm unit)')
parser.add_argument('--margin-right', '-r', type=float, default=2.0,
                    help='Right margin (in cm unit)')
parser.add_argument('--margin-top', '-t', type=float, default=2.0,
                    help='Top margin (in cm unit)')
parser.add_argument('--margin-bottom', '-b', type=float, default=2.0,
                    help='Bottom margin (in cm unit)')
parser.add_argument('--output', '-o', default='output.pdf',
                    help='Output file')
parser.add_argument('--author', default='',
                    help='Author of the PDF document')
parser.add_argument('--title', default='',
                    help='Title of the PDF document')

args = parser.parse_args()

PDFCreator(args, Margins(
    args.margin_right,
    args.margin_left,
    args.margin_top,
    args.margin_bottom))
