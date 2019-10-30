from ftwbook.graphicblock.interfaces import IGraphicConverter
from plone.namedfile.file import NamedBlobImage
from zope.component import getMultiAdapter
import os


def create_preview(obj, event):
    if not obj.file:
        return

    if os.environ.get('GRAPHICBLOCK_SKIP_GENERATING_PREVIEW', '').lower() == 'true':
        return

    converter = getMultiAdapter((obj, obj.file), IGraphicConverter)
    preview_image = converter()
    obj.preview = NamedBlobImage(preview_image.read(),
                                 filename=u'preview.png')
