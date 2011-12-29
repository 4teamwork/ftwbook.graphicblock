from plone.testing import Layer
from plone.testing import zca
from zope.configuration import xmlconfig


class BasicZCMLLayer(Layer):
    """A basic layer which only sets up the zcml, but does not start a zope
    instance.
    """

    defaultBases = (zca.ZCML_DIRECTIVES,)

    def setUp(self):
        self['configurationContext'] = zca.stackConfigurationContext(
            self.get('configurationContext'))

        import ftwbook.graphicblock.tests
        xmlconfig.file('tests.zcml', ftwbook.graphicblock.tests,
                       context=self['configurationContext'])

    def tearDown(self):
        del self['configurationContext']


BASIC_ZCML_LAYER = BasicZCMLLayer()
