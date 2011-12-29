from Products.Archetypes.interfaces.base import IBaseObject
from ftw.testing import MockTestCase
from ftwbook.graphicblock.browser.views import GraphicblockView
from ftwbook.graphicblock.interfaces import IGraphicBlock
from ftwbook.graphicblock.testing import BASIC_ZCML_LAYER
from mocker import Mocker, expect, ANY
from simplelayout.base.configlet.interfaces import ISimplelayoutConfiguration
from simplelayout.base.interfaces import ISimpleLayoutBlock
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.component import getMultiAdapter
from zope.component import getSiteManager
from zope.component import queryUtility, provideUtility
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


def mock_tool(mocker, mock, name):
    if getattr(mocker, '_getToolByName_mock', None) is None:
        mocker._getToolByName_mock = mocker.replace(
            'Products.CMFCore.utils.getToolByName')
    return expect(mocker._getToolByName_mock(ANY, name)).result(mock)


class TestGraphicblockView(MockTestCase):

    layer = BASIC_ZCML_LAYER

    def setUp(self):
        self.testcase_mocker = Mocker()

        # stub getToolByName by replacing it
        from Products.CMFCore import utils
        self._ori_getToolByName = utils.getToolByName
        getToolByName = self.testcase_mocker.replace(
            'Products.CMFCore.utils.getToolByName')

        portal_url = self.testcase_mocker.mock(count=False)
        expect(getToolByName(ANY, 'portal_url')).result(
            portal_url).count(0, None)
        expect(portal_url.getPortalObject().absolute_url()).result(
            'http://nohost/plone')

        # XXX simplelayout does not register the ISimplelayoutConfiguration
        # utility, so we mock one.
        assert queryUtility(
            ISimplelayoutConfiguration, name='sl-config') == None
        self.sl_config = self.testcase_mocker.mock(count=False)
        expect(self.sl_config.full_size).result(800)
        provideUtility(provides=ISimplelayoutConfiguration,
                       component=self.sl_config,
                       name='sl-config')

        self.testcase_mocker.replay()

    def tearDown(self):
        self.testcase_mocker.restore()

        # reset getToolByName (mocker does not restore it)
        from Products.CMFCore import utils
        utils.getToolByName = self._ori_getToolByName

        # unregister our simplelayout config utility
        getSiteManager().unregisterUtility(
            self.sl_config, ISimplelayoutConfiguration, name='sl-config')
        assert queryUtility(
            ISimplelayoutConfiguration, name='sl-config') == None

        self.testcase_mocker.verify()

    def _mock_objects(self, context_interfaces=None):
        mocks = self.create_dummy()

        # context
        mocks.context = self.providing_stub(
            [IGraphicBlock, ISimpleLayoutBlock, IBaseObject,
             IAttributeAnnotatable],
            name='context')

        # request
        mocks.request = self.providing_stub(
            [IDefaultBrowserLayer, IAttributeAnnotatable],
            name='request')

        return mocks

    def test_view_registered(self):
        mocks = self._mock_objects()
        self.replay()
        view = getMultiAdapter((mocks.context, mocks.request),
                               name='block_view')
        self.assertTrue(isinstance(view, GraphicblockView))

    def test_get_content_width(self):
        mocks = self._mock_objects()
        self.replay()
        view = getMultiAdapter((mocks.context, mocks.request),
                               name='block_view')

        self.assertEqual(view.get_content_width(), 800)

    def test_get_preview_dimensions(self):
        mocks = self._mock_objects()
        self.expect(mocks.context.getWidth()).result(75)  # 75 %
        preview = self.create_dummy(width=400, height=200)
        self.expect(mocks.context.getField('preview').getRaw(mocks.context)
                    ).result(preview)

        self.replay()
        view = getMultiAdapter((mocks.context, mocks.request),
                               name='block_view')

        self.assertEqual(view.get_preview_dimensions(),
                         {'width': 600,
                          'height': 300})
