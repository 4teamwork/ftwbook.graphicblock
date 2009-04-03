
from zope.component import getUtility
from zope.app.event.interfaces import IObjectModifiedEvent
from Products.CMFPlone.utils import normalizeString
from zope.component.exceptions import ComponentLookupError
from StringIO import StringIO
import traceback
from PIL import Image, ImageDraw, ImageFont

from interfaces import IGraphicConverter

def convertFileUpponImageCreation(obj, event):
    if obj.REQUEST.get('graphic_delete')=='delete':
        # delete preview, if graphic file was delete
        obj.getField('graphic_preview').set(obj, "DELETE_IMAGE")
        return
    if IObjectModifiedEvent.providedBy(event) and not obj.REQUEST.get('graphic_file'):
        # do nothing, if no new graphic was uploaded
        return

    file = obj.getGraphic()

    if file:
        image = file
        converter = None
        try:
            converter = getUtility(IGraphicConverter,
                                name = normalizeString(image.content_type, context=obj))
        except ComponentLookupError:
            try:
                converter = getUtility(ISkriptoriumImageConverter, 'base-converter')
            except ComponentLookupError, e:
                image = createErrorImage(e)

        if converter:
            image = converter.convert(image)

        if not obj.Title():
            obj.setTitle(file.filename)

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


