from interfaces import IGraphicConverter
from zope.component import getMultiAdapter


def create_preview(obj, event):
    """(re-) create preview after modifying object.
    """

    if obj.REQUEST.get('file_delete') == 'delete':
        # delete preview, if graphic file was delete
        obj.getField('preview').set(obj, 'DELETE_IMAGE')
        return

    graphic = obj.getFile()

    if not graphic:
        return

    converter = getMultiAdapter(IGraphicConverter,
                                (obj, graphic))

    preview_image = converter()
    # XXX scaling needed (obj.width %)?

    obj.getField('preview').set(obj, preview_image)
