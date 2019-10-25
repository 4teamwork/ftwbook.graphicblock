from ftwbook.graphicblock import _
from ftwbook.graphicblock.interfaces import IGraphicBlock
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.content import Container
from plone.namedfile import field
from plone.supermodel.model import Schema
from zope.interface import implementer
from zope.interface import provider
from zope.schema import Bool
from zope.schema import Int


@provider(IFormFieldProvider)
class IGraphicBlockSchema(Schema):

    showTitle = Bool(
        title=_(u'label_showtitle', default=u'Show title'),
        description=_(u'help_showtitle', default=u''),
    )

    file = field.NamedFile(
        title=_(u'label_file', default=u'PDF file'),
        description=_(u'help_file', default=u''),
        required=True,
    )

    preview = field.NamedImage(
        title=_(u'Preview', default=u'Preview'),
        searchable=False,
    )

    width = Int(
        title=_(u'label_width', default=u'Graphic width (%)'),
        description=_(u'help_width', default=u''),
        required=True,
        default=100,
    )

    trim_top = Int(
        title=_(u'label_trim_top', default=u'Trim top (mm)'),
        description=_(u'help_trim_top', default=u''),
        default=0,
    )

    trim_right = Int(
        title=_(u'label_trim_right', default=u'Trim right (mm)'),
        description=_(u'help_trim_right', default=u''),
        default=0,
    )

    trim_bottom = Int(
        title=_(u'label_trim_bottom', default=u'Trim bottom (mm)'),
        description=_(u'help_trim_bottom', default=u''),
        default=0,
    )

    trim_left = Int(
        title=_(u'label_trim_left', default=u'Trim left (mm)'),
        description=_(u'help_trim_left', default=u''),
        default=0,
    )


@implementer(IGraphicBlock)
class GraphicBlock(Container):
    pass
