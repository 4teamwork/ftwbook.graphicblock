from ftw.builder import builder_registry
from ftw.builder.dexterity import DexterityBuilder
from plone.namedfile.file import NamedBlobFile
import os.path


class GraphicBlockBuilder(DexterityBuilder):
    portal_type = 'ftwbook.graphicblock.GraphicBlock'

    def with_file(self, name='diagram.pdf'):
        path = os.path.join(__file__, '..', 'assets', name)
        path = os.path.abspath(path)
        with open(path, 'rb') as fio:
            self.arguments['file'] = NamedBlobFile(
                data=fio.read(), filename=name.decode())
        return self


builder_registry.register('graphicblock', GraphicBlockBuilder)
