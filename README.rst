ftwbook.graphicblock
====================


This package is a addon for the `ftw.book`_ package. It provides an
additional simplelayout-based block for uploading PDF documents, which
will then be included in the book PDF.

The block is intended to be used for including vector based data such
as charts. The uploaded PDF is included in the exported PDF of the whole
book directly as PDF, so that there is no quality loss.

Features
--------

- resizing the PDF
- cropping the PDF
- automatic generation of PNG preview for the displaying in the browser
  (based on ghostscript)
- including PDF like an picture (intended for charts etc)
- including PDF as sub-document (multiple pages)


Installation
------------

- Ghostscript needs to be installed on the server (http://www.ghostscript.com/)
- Add ``ftwbook.graphicblock`` to your buildout configuration::

    [instance]
    eggs +=
        ftwbook.graphicblock

- Install the generic import profile.


Links
-----

- Github: https://github.com/4teamwork/ftwbook.graphicblock
- Issues: https://github.com/4teamwork/ftwbook.graphicblock/issues
- Pypi: http://pypi.python.org/pypi/ftwbook.graphicblock
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftwbook.graphicblock


Copyright
---------

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftwbook.graphicblock`` is licensed under GNU General Public License, version 2.


.. _ftw.book: https://github.com/4teamwork/ftw.book
