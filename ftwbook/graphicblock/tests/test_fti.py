from ftw.testbrowser import browsing
from ftw.testbrowser.pages import factoriesmenu
from ftwbook.graphicblock.tests import FunctionalTestCase


class TestFTI(FunctionalTestCase):

    @browsing
    def test_creating_a_new_graphicblock(self, browser):
        self.grant('Contributor')
        browser.login().open(self.empty_chapter)
        factoriesmenu.add('Graphic Block')

        with self.asset('diagram.pdf') as diagram:
            browser.fill({'Title': 'The Graphicblock',
                          'PDF document': diagram}).save()

        self.assertEquals(self.empty_chapter, browser.context,
                          'Expected redirect to chapter view after savin')

        image = browser.css('.graphicblock-image img').first
        self.assertDictContainsSubset(
            {'height': '1228',
             'width': '868'},
            image.attrib)

        browser.open(image.attrib['src'])
        self.assertEquals('image/jpeg',
                          browser.headers.get('Content-Type'))

    @browsing
    def test_preview_field_is_not_visible(self, browser):
        self.grant('Contributor')
        browser.login().open(self.empty_chapter)
        factoriesmenu.add('Graphic Block')
        self.assertTrue(browser.find('Show title as legend'))
        self.assertFalse(browser.find('Preview'))
