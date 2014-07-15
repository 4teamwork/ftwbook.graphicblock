from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browsing
from ftw.testbrowser.pages import factoriesmenu
from ftwbook.graphicblock.testing import GRAPHICBLOCK_FUNCTIONAL_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from unittest2 import TestCase
import os.path


def asset(name, mode='rb'):
    return open(os.path.join(os.path.dirname(__file__), 'assets', name), mode)


class TestGraphicblock(TestCase):
    layer = GRAPHICBLOCK_FUNCTIONAL_TESTING

    def setUp(self):
        setRoles(self.layer['portal'], TEST_USER_ID, ['Contributor'])

    @browsing
    def test_creating_a_new_graphicblock(self, browser):
        book = create(Builder('book').titled('The book'))
        chapter = create(Builder('chapter').titled('The chapter').within(book))

        browser.login().open(chapter)
        factoriesmenu.add('Graphic Block')

        with asset('diagram.pdf') as diagram:
            browser.fill({'Title': 'The Graphicblock',
                          'PDF document': diagram}).save()

        self.assertEquals(chapter, browser.context,
                          'Expected redirect to chapter view after savin')

        image = browser.css('.BlockOverallWrapper.graphicblock'
                            ' .simplelayout-block-wrapper img').first

        self.assertDictContainsSubset(
            {'height': '1228',
             'width': '868'},
            image.attrib)

        browser.open(image.attrib['src'])
        self.assertEquals('image/jpeg',
                          browser.headers.get('Content-Type'))
