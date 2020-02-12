from ftwbook.graphicblock import _
from ftwbook.graphicblock.interfaces import IGraphicBlock
from plone.autoform.directives import omitted
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.content import Item
from plone.namedfile.field import NamedBlobFile
from plone.namedfile.field import NamedBlobImage
from plone.supermodel.directives import primary
from plone.supermodel.model import Schema
from zope.interface import implementer
from zope.interface import provider
from zope.schema import Bool
from zope.schema import Int
from zope.schema import TextLine


@provider(IFormFieldProvider)
class IGraphicBlockSchema(Schema):

    title = TextLine(
        title=_(u'label_title', default=u'Title'),
        required=False)

    show_title = Bool(
        title=_(u'label_show_title', default=u'Show title as legend'),
        default=False,
        required=False)

    primary('file')
    file = NamedBlobFile(
        title=_(u'label_file', default=u'PDF file'),
        required=True)

    omitted('preview')
    preview = NamedBlobImage(
        title=_(u'Preview', default=u'Preview'),
        required=False)

    width = Int(
        title=_(u'label_width', default=u'Graphic width (%)'),
        required=True,
        default=100)

    trim_top = Int(
        title=_(u'label_trim_top', default=u'Trim top (mm)'),
        default=0,
        required=False)

    trim_right = Int(
        title=_(u'label_trim_right', default=u'Trim right (mm)'),
        default=0,
        required=False)

    trim_bottom = Int(
        title=_(u'label_trim_bottom', default=u'Trim bottom (mm)'),
        default=0,
        required=False)

    trim_left = Int(
        title=_(u'label_trim_left', default=u'Trim left (mm)'),
        default=0,
        required=False)


@implementer(IGraphicBlock)
class GraphicBlock(Item):
    pass
