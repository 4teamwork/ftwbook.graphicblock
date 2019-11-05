from ftw.book.tests import FunctionalTestCase as BookFunctionalTestCase
from ftwbook.graphicblock.testing import GRAPHICBLOCK_FUNCTIONAL_TESTING
import os.path


class FunctionalTestCase(BookFunctionalTestCase):
    layer = GRAPHICBLOCK_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.book = self.portal.restrictedTraverse(
            self.layer['book_path'])
        self.chapter = self.book.restrictedTraverse(
            'introduction')
        self.empty_chapter = self.book.restrictedTraverse(
            'empty-chapter')
        self.graphicblock = self.book.unrestrictedTraverse(
            'introduction/graphicblock')

    def asset(self, name, mode='rb'):
        tests_dir = os.path.join(os.path.dirname(__file__))
        file_path = os.path.join(tests_dir, 'assets', name)
        return open(file_path, mode)
