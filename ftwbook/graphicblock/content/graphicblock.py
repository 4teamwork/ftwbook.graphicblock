"""Definition of the GraphicBlock content type
"""

from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.Archetypes import atapi
from ftwbook.graphicblock import _
from ftwbook.graphicblock.config import PROJECTNAME
from ftwbook.graphicblock.interfaces import IGraphicBlock
from simplelayout.base.interfaces import ISimpleLayoutBlock
from zope.interface import implements


SCHEMA = atapi.Schema((

        atapi.BooleanField(
            name='showTitle',
            default=False,
            searchable=False,
            widget=atapi.BooleanWidget(
                label=_(u'label_showtitle',
                        default=u'Show title'),
                description=_(u'help_showtitle', default=u''))),

        atapi.FileField(
            name='file',
            storage=atapi.AnnotationStorage(),
            required=True,
            searchable=True,
            widget=atapi.FileWidget(
                label=_(u'label_file',
                        u'PDF file'),
                description=_(u'help_file', default=u''),
                visible=dict(edit='visible', view='invisible'))),

        atapi.ImageField(
            name='preview',
            storage=atapi.AnnotationStorage(),
            required=False,
            searchable=False,
            widget=atapi.ImageWidget(
                label=_(u'Preview',
                        default=u'Preview'),
                visible=dict(edit='invisible', view='visible'))),

        atapi.IntegerField(
            name='width',
            required=True,
            default=100,
            searchable=False,
            widget=atapi.IntegerWidget(
                label=_(u'label_width',
                        default=u'Grapic width (%)'),
                description=_(u'help_width', default=u''))),

        atapi.IntegerField(
            name='trim_top',
            required=False,
            searchable=False,
            default=0,
            widget=atapi.IntegerWidget(
                label=_(u'label_trim_top',
                        default=u'Trim top (mm)'),
                help=_(u'help_trim_top', default=u''))),

        atapi.IntegerField(
            name='trim_right',
            required=False,
            searchable=False,
            default=0,
            widget=atapi.IntegerWidget(
                label=_(u'label_trim_right',
                        default=u'Trim right (mm)'),
                help=_(u'help_trim_right', default=u''))),

        atapi.IntegerField(
            name='trim_bottom',
            required=False,
            searchable=False,
            default=0,
            widget=atapi.IntegerWidget(
                label=_(u'label_trim_bottom',
                        default=u'Trim bottom (mm)'),
                help=_(u'help_trim_bottom', default=u''))),

        atapi.IntegerField(
            name='trim_left',
            required=False,
            searchable=False,
            default=0,
            widget=atapi.IntegerWidget(
                label=_(u'label_trim_left',
                        default=u'Trim left (mm)'),
                help=_(u'help_trim_left', default=u''))),


        ))


GraphicBlockSchema = schemata.ATContentTypeSchema.copy() + SCHEMA


GraphicBlockSchema['title'].required = False
GraphicBlockSchema['title'].searchable = False
GraphicBlockSchema['description'].widget.visible = {'edit': 0, 'view': 0}
schemata.finalizeATCTSchema(GraphicBlockSchema, moveDiscussion=False)


class GraphicBlock(base.ATCTContent):
    """Graphic Block for embedding PDF files into Books"""

    implements(IGraphicBlock, ISimpleLayoutBlock)
    schema = GraphicBlockSchema

atapi.registerType(GraphicBlock, PROJECTNAME)
