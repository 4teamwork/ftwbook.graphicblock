"""Definition of the GraphicBlock content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from izug.graphicblock import graphicblockMessageFactory as _
from izug.graphicblock.interfaces import IGraphicBlock
from izug.graphicblock.config import PROJECTNAME

GraphicBlockSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

GraphicBlockSchema['title'].storage = atapi.AnnotationStorage()
GraphicBlockSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(GraphicBlockSchema, moveDiscussion=False)

class GraphicBlock(base.ATCTContent):
    """Graphic Block for embedding PDF files into Books"""
    implements(IGraphicBlock)

    portal_type = "GraphicBlock"
    schema = GraphicBlockSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

atapi.registerType(GraphicBlock, PROJECTNAME)
