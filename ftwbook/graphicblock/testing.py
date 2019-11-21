from datetime import datetime
from ftw.book.testing import clear_transmogrifier_registry
from ftw.builder import Builder
from ftw.builder import session
from ftw.builder import ticking_creator
from ftw.builder.testing import functional_session_factory
from ftw.testing import freeze
from ftw.testing.layer import COMPONENT_REGISTRY_ISOLATION
from plone.app.testing import FunctionalTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.testing import z2
from zope.configuration import xmlconfig
import ftw.book.tests.builders  # noqa
import ftwbook.graphicblock.tests.builders  # noqa


class GraphicblockLayer(PloneSandboxLayer):
    defaultBases = (COMPONENT_REGISTRY_ISOLATION,)

    def setUp(self):
        clear_transmogrifier_registry()
        session.current_session = functional_session_factory()
        super(GraphicblockLayer, self).setUp()

    def tearDown(self):
        session.current_session = None
        super(GraphicblockLayer, self).tearDown()
        clear_transmogrifier_registry()

    def setUpZope(self, app, configurationContext):
        xmlconfig.string(
            '<configure xmlns="http://namespaces.zope.org/zope">'
            '  <include package="z3c.autoinclude" file="meta.zcml" />'
            '  <includePlugins package="plone" />'
            '  <includePluginsOverrides package="plone" />'
            '</configure>',
            context=configurationContext)

        z2.installProduct(app, 'ftw.simplelayout')
        z2.installProduct(app, 'ftw.book')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ftwbook.graphicblock:default')
        self['book_path'] = '/'.join(
            self.create_example_book().getPhysicalPath())

    def create_example_book(self):
        with freeze(datetime(2016, 10, 31, 9, 52, 34),
                    ignore_modules=('ZODB.utils')) as clock:
            create = ticking_creator(clock, hours=1)

            book = create(
                Builder('book')
                .titled(u'The Example Book'))

            introduction = create(Builder('chapter').within(book)
                                  .titled(u'Introduction'))

            create(Builder('chapter').within(book)
                   .titled(u'Empty Chapter'))

            create(Builder('graphicblock')
                   .within(introduction)
                   .titled(u'Graphicblock')
                   .having(show_title=True)
                   .with_file())

        return book


GRAPHICBLOCK_FIXTURE = GraphicblockLayer()
GRAPHICBLOCK_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(GRAPHICBLOCK_FIXTURE, ),
    name='ftwbook.graphicblock:functional')
