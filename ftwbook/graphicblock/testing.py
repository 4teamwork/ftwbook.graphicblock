from ftw.builder.testing import BUILDER_LAYER
from ftw.builder.testing import functional_session_factory
from ftw.builder.testing import set_builder_session_factory
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import Layer
from plone.testing import z2
from plone.testing import zca
from zope.configuration import xmlconfig
import ftw.book.tests.builders


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



class GraphicblockLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        xmlconfig.string(
            '<configure xmlns="http://namespaces.zope.org/zope">'
            '  <include package="z3c.autoinclude" file="meta.zcml" />'
            '  <includePlugins package="plone" />'
            '  <includePluginsOverrides package="plone" />'
            '</configure>',
            context=configurationContext)

        z2.installProduct(app, 'simplelayout.base')
        z2.installProduct(app, 'ftw.contentpage')
        z2.installProduct(app, 'ftw.book')
        z2.installProduct(app, 'ftwbook.graphicblock')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ftw.book:default')
        applyProfile(portal, 'ftwbook.graphicblock:default')


GRAPHICBLOCK_FIXTURE = GraphicblockLayer()
GRAPHICBLOCK_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(GRAPHICBLOCK_FIXTURE,
           set_builder_session_factory(functional_session_factory)
           ), name="functional")
