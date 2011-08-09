Introduction
============


This package is a addon for the `ftw.book` package. It provides an
additional simplelayout-based block for uploading PDF documents, which
will then be included in the book PDF.

The block is intended to be used for including vector based data such
as charts. The uploaded PDF is included in the exported PDF of the whole
book directly as PDF, so that there is no quality loss.

Features:

* resizing the PDF
* cropping the PDF
* automatic generation of PNG preview for the displaying in the browser
  (based on ghostscript)
* including PDF like an picture (intended for charts etc)
* including PDF as sub-document (multiple pages)


Installation
============

Operatic system dependencies:

* Ghostscript (http://www.ghostscript.com/)
