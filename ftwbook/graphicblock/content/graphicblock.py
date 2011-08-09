"""Definition of the GraphicBlock content type
"""

from zope.interface import implements
from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from ftwbook.graphicblock.interfaces import IGraphicBlock
from ftwbook.graphicblock.config import PROJECTNAME
from ftwbook.bibliothek.content import latexmixin


GraphicBlockSchema = (schemata.ATContentTypeSchema.copy() + \
                          latexmixin.LatexMixinSchema + \
                          atapi.Schema((

            atapi.BooleanField(
                name='showTitle',
                storage=atapi.AnnotationStorage(),
                schemata='default',
                default=False,
                widget=atapi.BooleanWidget(
                    label='Show title',
                    label_msgid='ftwbook_label_showtitle',
                    description='',
                    description_msgid='ftwbook_help_showtitle',
                    i18n_domain='ftwbook',
                    ),
                ),

            atapi.FileField(
                name = 'graphic',
                storage = atapi.AnnotationStorage(),
                widget = atapi.FileWidget(
                    label = 'Graphic (PDF)',
                    label_msgid = 'ftwbook_label_graphic',
                    description = '',
                    description_msgid = '',
                    i18n_domain = 'ftwbook.graphicblock',
                    visible = {
                        'edit' : 'visible',
                        'view' : 'invisible',
                        },
                    ),
                ),

            atapi.ImageField(
                name = 'graphic_preview',
                storage = atapi.AnnotationStorage(),
                widget = atapi.ImageWidget(
                    label = 'Graphic Preview',
                    label_msgid = 'ftwbook_label_graphic_preview',
                    description = '',
                    description_msgid = '',
                    i18n_domain = 'ftwbook.graphicblock',
                    visible = {
                        'edit' : 'invisible',
                        'view' : 'visible',
                        }
                    ),
                ),

            atapi.IntegerField(
                name = 'width',
                storage = atapi.AnnotationStorage(),
                required = True,
                searchable = False,
                default = 100,
                widget = atapi.IntegerWidget(
                    label = 'Graphic Width',
                    label_msgid = 'ftwbook_label_graphic_width',
                    description = '',
                    description_msgid = '',
                    i18n_domain = 'ftwbook.graphicblock',
                    ),
                ),

            atapi.IntegerField(
                name = 'trim_top',
                storage = atapi.AnnotationStorage(),
                required = False,
                searchable = False,
                default = 0,
                widget = atapi.IntegerWidget(
                    label = 'Trim top (mm)',
                    label_msgid = 'ftwbook_label_trim_top',
                    description = '',
                    description_msgid = '',
                    i18n_domain = 'ftwbook.graphicblock',
                    ),
                ),

            atapi.IntegerField(
                name = 'trim_right',
                storage = atapi.AnnotationStorage(),
                required = False,
                searchable = False,
                default = 0,
                widget = atapi.IntegerWidget(
                    label = 'Trim right (mm)',
                    label_msgid = 'ftwbook_label_trim_right',
                    description = '',
                    description_msgid = '',
                    i18n_domain = 'ftwbook.graphicblock',
                    ),
                ),

            atapi.IntegerField(
                name = 'trim_bottom',
                storage = atapi.AnnotationStorage(),
                required = False,
                searchable = False,
                default = 0,
                widget = atapi.IntegerWidget(
                    label = 'Trim bottom (mm)',
                    label_msgid = 'ftwbook_label_trim_bottom',
                    description = '',
                    description_msgid = '',
                    i18n_domain = 'ftwbook.graphicblock',
                    ),
                ),

            atapi.IntegerField(
                name = 'trim_left',
                storage = atapi.AnnotationStorage(),
                required = False,
                searchable = False,
                default = 0,
                widget = atapi.IntegerWidget(
                    label = 'Trim left (mm)',
                    label_msgid = 'ftwbook_label_trim_left',
                    description = '',
                    description_msgid = '',
                    i18n_domain = 'ftwbook.graphicblock',
                    ),
                ),


            # -*- Your Archetypes field definitions here ... -*-

            )))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

GraphicBlockSchema['title'].storage = atapi.AnnotationStorage()
GraphicBlockSchema['title'].required = False
GraphicBlockSchema['title'].searchable = False

GraphicBlockSchema['description'].storage = atapi.AnnotationStorage()
GraphicBlockSchema['description'].widget.visible = {'edit': 0, 'view': 0}

GraphicBlockSchema['excludeFromNav'].default = True

schemata.finalizeATCTSchema(GraphicBlockSchema, moveDiscussion=False)

class GraphicBlock(base.ATCTContent, latexmixin.LatexMixin):
    """Graphic Block for embedding PDF files into Books"""
    implements(IGraphicBlock)

    portal_type = "GraphicBlock"
    schema = GraphicBlockSchema

    _sl_viewlet = 'ftwbook.graphicblock'

    # ATFolder
    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # GraphicBlock
    showTitle = atapi.ATFieldProperty('showTitle')
    graphic = atapi.ATFieldProperty('graphic')
    graphic_preview = atapi.ATFieldProperty('graphic_preview')
    width = atapi.ATFieldProperty('width')
    trim_top = atapi.ATFieldProperty('trim_top')
    trim_right = atapi.ATFieldProperty('trim_right')
    trim_bottom = atapi.ATFieldProperty('trim_bottom')
    trim_left = atapi.ATFieldProperty('trim_left')

atapi.registerType(GraphicBlock, PROJECTNAME)
