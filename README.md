txt2pdf
=======

Text to PDF converter with Unicode support.

This is a Python 2 script using the ReportLab module for generating PDF
documents. It is intended to be used with monospace True Type fonts.
It can be hacked for being used with Type 1 Postscript fonts, but such
fonts contain less characters than TTF ones.

The following fonts have been tested with success:

  * LiberationMono
  * DejaVuSansMono
  * UbuntuMono
  * DroidSansMono
  * FiraMono
  * InputMono (different versions)
  * Envy Code
  * Anonymous Pro
  * APL385
  * APLX Unicode
  * SImPL

The Type 1 font "Courier10PitchBT-Roman" can be used by hacking the code.

The following True Type fonts don't work:

  * Pragmata Pro

No Open Type font work, which includes:

  * Source Code Pro
  * Inconsolata
  * UMTypewriter
