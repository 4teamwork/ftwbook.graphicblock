from plone.namedfile.file import NamedBlobImage
from ftwbook.graphicblock.interfaces import IGraphicConverter
from zope.component import getMultiAdapter


def create_preview(obj, event):
    if not obj.file:
        return

    converter = getMultiAdapter((obj, obj.file), IGraphicConverter)
    preview_image = converter()
    obj.preview = NamedBlobImage(preview_image.read(),
                                 filename=u'preview.png')
