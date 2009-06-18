
from PIL import Image
import time
import os
from subprocess import Popen, PIPE, call
from zope.interface import implements
from Products.ATContentTypes.lib.imagetransform import ATCTImageTransform
from StringIO import StringIO
import logging


from interfaces import IGraphicConverter
from events import createErrorImage
from izug.graphicblock import config

logger = logging.getLogger('izug.graphicblock')

class BaseGraphicConverter(object):
    implements(IGraphicConverter)
    
    def getImageAsFile(self, image):
        tmp = ''
        transformer = ATCTImageTransform()
        img = transformer.getImageAsFile(img=image )
        if img is not None:
             tmp = img.read()
        elif hasattr(image, 'data'):
             tmp = image.data
        elif hasattr(image, '_data'):
             tmp = image._data
        return StringIO(tmp)
    
    def convert(self, image):
        return self.getImageAsFile(image)
    

class PDFConverter(BaseGraphicConverter):

    GS_CMD = 'gs -q -dSAFER -dBATCH -dNOPAUSE -sDEVICE=jpeg -dTextAlphaBits=4 -dGraphicsAlphaBits=4 -r105'
    def convert(self, image):
        """convert pdf files to jpeg"""
        data  = self.getImageAsFile(image)
        try:
            opath, cpath = self.getTempfiles()
        
            logger.info('original file: %s' % opath)
            logger.info('converted file: %s' % cpath)

            ofile = open(opath, 'wb')
            ofile.write(data.read())
            ofile.close()
            
            cmd = "%s -sOutputFile=%s %s" % (PDFConverter.GS_CMD, cpath, opath)
            logger.info('calling: %s' % cmd)
            retcode = call(cmd.split(' '))
            os.remove(opath)
                            
            if retcode == 0:
                cfile = open(cpath, 'rb')
                converted = cfile.read()
                cfile.close()
                os.remove(cpath)
                width = int(float(image.width) / 100 * config.PREVIEW_MAX_WIDTH)
                return self.rescale_image(StringIO(converted), width)
            else:
                raise IOError, 'Program terminated with error code %s' % (retcode)
        except Exception, e:
            return createErrorImage(e)

    def rescale_image(self, stream, width):
        """
        stream: image stream (e.g. open('pic.jpg'))
        width: width
        return: resized stream
        """
        original = Image.open(stream)
        width = int(width)
        height = int(width * float(original.size[1]) / original.size[0])
        resized = original.resize((width, height))
        iostring = StringIO()
        resized.save(iostring, 'jpeg')
        return iostring

    def getTempfiles(self):
        name = time.strftime("%Y%m%d%H%M%S_image")
        
        filebase = name
        i = 0
        while os.path.exists(filebase + '.pdf'):
            i += 1
            filebase = name + str(i)
        name = filebase

        return name + '.pdf', name + '.jpg'


