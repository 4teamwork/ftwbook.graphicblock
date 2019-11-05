from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata


SCHEMA = atapi.Schema((

        atapi.BooleanField(
            name='showTitle',
            default=False,
            searchable=False,
            widget=atapi.BooleanWidget()),

        atapi.FileField(
            name='file',
            storage=atapi.AnnotationStorage(),
            required=True,
            searchable=True,
            widget=atapi.FileWidget()),

        atapi.ImageField(
            name='preview',
            storage=atapi.AnnotationStorage(),
            required=False,
            searchable=False,
            widget=atapi.ImageWidget()),

        atapi.IntegerField(
            name='width',
            required=True,
            default=100,
            searchable=False,
            widget=atapi.IntegerWidget()),

        atapi.IntegerField(
            name='trim_top',
            required=False,
            searchable=False,
            default=0,
            widget=atapi.IntegerWidget()),

        atapi.IntegerField(
            name='trim_right',
            required=False,
            searchable=False,
            default=0,
            widget=atapi.IntegerWidget()),

        atapi.IntegerField(
            name='trim_bottom',
            required=False,
            searchable=False,
            default=0,
            widget=atapi.IntegerWidget()),

        atapi.IntegerField(
            name='trim_left',
            required=False,
            searchable=False,
            default=0,
            widget=atapi.IntegerWidget())))


GraphicBlockSchema = schemata.ATContentTypeSchema.copy() + SCHEMA
schemata.finalizeATCTSchema(GraphicBlockSchema, moveDiscussion=False)


class GraphicBlock(base.ATCTContent):
    schema = GraphicBlockSchema
