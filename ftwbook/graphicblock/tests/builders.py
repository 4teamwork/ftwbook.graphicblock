from ftw.builder.dexterity import DexterityBuilder
from ftw.builder import builder_registry


class GraphicBlockBuilder(DexterityBuilder):
    portal_type = 'ftwbook.graphicblock.GraphicBlock'


builder_registry.register('graphicblock', GraphicBlockBuilder)
