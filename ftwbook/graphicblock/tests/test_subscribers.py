from ftw.testbrowser import browsing
from ftw.testbrowser.pages import factoriesmenu
from ftwbook.graphicblock.tests import FunctionalTestCase


class TestSubscribers(FunctionalTestCase):

    @browsing
    def test_creating_block_generates_preview(self, browser):
        self.grant('Contributor')
        browser.login().open(self.empty_chapter)
        factoriesmenu.add('Graphic Block')

        with self.asset('diagram.pdf') as diagram:
            browser.fill({'Title': 'The Graphicblock',
                          'PDF document': diagram}).save()

        blocks = self.empty_chapter.contentValues()
        self.assertEqual(1, len(blocks), blocks)
        block, = blocks

        self.assertTrue(block.preview,
                        'Creating a graphic block should generate a preview')

    @browsing
    def test_modifying_block_regenerates_preview(self, browser):
        self.graphicblock.preview = None
        self.assertFalse(self.graphicblock.preview)

        browser.login().open(self.graphicblock, view='edit')
        with self.asset('diagram.pdf') as diagram:
            browser.fill({'PDF document': diagram}).save()

        self.assertTrue(self.graphicblock.preview)
