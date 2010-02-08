
from zope.component import getUtility
from zope.app.event.interfaces import IObjectModifiedEvent
from Products.CMFPlone.utils import normalizeString
from zope.component.exceptions import ComponentLookupError
from StringIO import StringIO
import traceback
from PIL import Image, ImageDraw, ImageFont

from izug.graphicblock import config
from interfaces import IGraphicConverter

def convertFileUpponImageCreation(obj, event):
    if obj.REQUEST.get('graphic_delete')=='delete':
        # delete preview, if graphic file was delete
        obj.getField('graphic_preview').set(obj, "DELETE_IMAGE")
        return

    file_ = obj.getGraphic()

    if file_:
        image = file_
        converter = None
        try:
            converter = getUtility(IGraphicConverter,
                                name = normalizeString(image.content_type, context=obj))
        except ComponentLookupError:
            try:
                converter = getUtility(IGraphicConverter, 'base-converter')
            except ComponentLookupError, e:
                image = createErrorImage(e)

        if converter:
            image = converter.convert(image)

        if not obj.Title():
            obj.setTitle(file_.filename)

        # resize
        try:
            ori_im = Image.open(image)
        except IOError:
            pass
        else:
            ori_im = ori_im.convert('RGB')
            if ori_im.size[0]>config.PREVIEW_MAX_WIDTH:
                pv_size = (config.PREVIEW_MAX_WIDTH,
                           ori_im.size[1] * config.PREVIEW_MAX_WIDTH / ori_im.size[0])
                pv_im = ori_im.resize(pv_size, Image.ANTIALIAS)
                pv_file = StringIO()
                pv_im.save(pv_file, 'PNG')
                image = pv_file

            obj.schema['graphic_preview'].set(obj, image)
            image.close()

def createErrorImage(e=None, msg=''):    
    if e is not None:
        erms = StringIO()
        traceback.print_exc(file=erms)
        msg = erms.getvalue()
    msgs = msg.split('\n')
    ml = ''
    for m in msgs:
        ml = len(m)>len(ml) and m or ml 
    height = (len(msgs)*12)+(2*10)
    width = ImageFont.load_default().getsize(ml)[0]+2*10
    tmpimg = Image.new("RGB", (width,height))
    draw = ImageDraw.Draw(tmpimg)
    for i in range(0,len(msgs)):
        draw.text((10,i*15), msgs[i])
    out = StringIO()
    tmpimg.save(out, 'png')
    return out


