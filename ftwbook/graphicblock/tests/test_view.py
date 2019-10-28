from ftw.testbrowser import browsing
from ftwbook.graphicblock.tests import FunctionalTestCase
import transaction


class TestView(FunctionalTestCase):

    @browsing
    def test_show_title(self, browser):
        self.graphicblock.show_title = True
        transaction.commit()
        browser.login().open(self.graphicblock)
        self.assertEqual(['Graphicblock'],
                         browser.css('.graphicblock-label').text)

        self.graphicblock.show_title = False
        transaction.commit()
        browser.reload()
        self.assertEqual([], browser.css('.graphicblock-label').text)
