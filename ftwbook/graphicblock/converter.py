from PIL import Image, ImageDraw, ImageFont
from Products.ATContentTypes.lib.imagetransform import ATCTImageTransform
from Products.CMFPlone.utils import normalizeString
from StringIO import StringIO
from ftwbook.graphicblock import _
from ftwbook.graphicblock.interfaces import IGraphicConverter
from ftwbook.graphicblock.interfaces import ITypeSpecificConverter
from shutil import rmtree
from subprocess import call
from zope.component import adapts
from zope.component import queryMultiAdapter, getMultiAdapter
from zope.interface import implements, Interface
import logging
import os
import tempfile


class GraphicConverter(object):
    """IGraphicConverter adapter for converting a file to a preview image.
    Searches for more specific IGraphicConverter adapters, depending on the
    content-type of the file or falls back to the FallbackGraphicConverter.
    """

    implements(IGraphicConverter)
    adapts(Interface, Interface)

    def __init__(self, context, graphic):
        self.context = context
        self.graphic = graphic

    def __call__(self):
        contenttype = normalizeString(self.graphic.content_type,
                                      context=self.context)

        converter = queryMultiAdapter((self.context, self.graphic),
                                      ITypeSpecificConverter,
                                      name=contenttype)

        if not converter:
            converter = getMultiAdapter((self.context, self.graphic),
                                        ITypeSpecificConverter,
                                        name='fallback-converter')

        return converter()


class BaseGraphicConverter(object):
    """Base graphic converter to super class graphic converter.
    Provides a method get_data returning the file data and a
    method generate_error_image(message).
    """

    implements(ITypeSpecificConverter)
    adapts(Interface, Interface)

    def __init__(self, context, graphic):
        self.context = context
        self.graphic = graphic

    def get_data(self):
        transformer = ATCTImageTransform()
        img = transformer.getImageAsFile(img=self.graphic)

        if img is not None:
            return StringIO(img.read())

        if hasattr(self.graphic, 'data'):
            return StringIO(self.graphic.data)

        if hasattr(self.graphic, '_data'):
            return StringIO(self.graphic._data)

        return None

    def generate_error_image(self, message):
        """Creating an error image containing the error `message`
        as png image. Returns a file stream.
        """

        lines = message.strip().split('\n')

        longest_line = max(lines, key=len)
        width = ImageFont.load_default().getsize(longest_line)[0] + 2 * 10
        height = (len(lines) * 12) + (2 * 10)

        image = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(image)

        for index, line in enumerate(lines):
            draw.text((10, index * 15), line)

        data = StringIO()
        image.save(data, 'png')

        return data


class FallbackGraphicConverter(BaseGraphicConverter):
    """Fallback graphic converter, trying to convert the image with
    ATCTImageTransform
    """

    def __call__(self):
        return self.get_data()


class PDFConverter(BaseGraphicConverter):
    """graphic converter converting PDF documents to preview images.
    """

    # XXX should we use a absolute path?
    GS_CMD = 'gs'

    GS_ARGUMENTS = ('-q',
                    '-dSAFER',
                    '-dBATCH',
                    '-dNOPAUSE',
                    '-sDEVICE=jpeg',
                    '-dTextAlphaBits=4',
                    '-dGraphicsAlphaBits=4',
                    '-r105')

    def __call__(self):
        logger = logging.getLogger('ftwbook.graphicblock pdfconverter')

        tempdir = tempfile.mkdtemp()
        pdf_path = os.path.join(tempdir, 'temp.pdf')
        jpg_path = os.path.join(tempdir, 'temp.jpg')
        logger.debug('tempfiles at %s' % tempdir)

        try:
            # write data to pdf temp file
            pdf_file = open(pdf_path, 'wb')
            pdf_file.write(self.get_data().read())
            pdf_file.close()

            cmd_args = [self.__class__.GS_CMD]
            cmd_args.extend(self.__class__.GS_ARGUMENTS)
            cmd_args.extend(['-sOutputFile=%s' % jpg_path, pdf_path])

            logger.info('calling: %s' % ' '.join(cmd_args))
            retcode = call(cmd_args)

            if retcode != 0:
                logger.error(
                    'ghostscript failed with exitcode %s' % str(retcode))

                return self.generate_error_image(
                    _(u'error_ghostscript_pdf_preview',
                      default=u'ERROR: Could not generate PDF preview ' + \
                          '(Ghostscript error code: ${code})',
                      mapping=dict(code=retcode)))

            return open(jpg_path, 'rb')

        finally:
            rmtree(tempdir)
