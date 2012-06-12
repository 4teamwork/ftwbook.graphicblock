from ftw.pdfgenerator.interfaces import ILaTeXView
from ftw.testing import MockTestCase
from ftwbook.graphicblock.interfaces import IGraphicBlock
from ftwbook.graphicblock.latex.graphicblock import GraphicBlockLaTeXView
from ftwbook.graphicblock.testing import BASIC_ZCML_LAYER
from plone.mocktestcase.dummy import Dummy
from zope.app.component.hooks import setSite
from zope.component import getGlobalSiteManager
from zope.component import getMultiAdapter
from zope.i18n.interfaces import IUserPreferredLanguages
from zope.interface import alsoProvides


class TestGraphicBlockLaTeXView_component(MockTestCase):

    layer = BASIC_ZCML_LAYER

    def test_component_registered(self):
        context = self.providing_stub([IGraphicBlock])
        request = self.create_dummy()
        layer = self.create_dummy()

        self.replay()

        view = getMultiAdapter((context, request, layer), ILaTeXView)

        self.assertTrue(isinstance(view, GraphicBlockLaTeXView))


class TestGraphicBlockLaTeXView_UnitTests(MockTestCase):

    def setUp(self):
        setSite(self._create_site_with_request())

    def tearDown(self):
        setSite(None)

    def _create_site_with_request(self):
        request = Dummy(getPreferredLanguages=lambda: [])
        alsoProvides(request, IUserPreferredLanguages)
        site = Dummy(REQUEST=request,
                     getSiteManager=getGlobalSiteManager)

        return site

    def test_render(self):
        context = self.stub()
        request = self.create_dummy()
        layout = self.mocker.mock()

        # title
        self.expect(context.getShowTitle()).result(True)
        self.expect(context.Title()).result('My graph')

        # file / UID
        self.expect(context.UID()).result('789')

        file_data = 'FILE DATA'
        file_ = self.create_dummy(data=file_data)
        self.expect(context.getFile()).result(file_)
        self.expect(layout.get_builder().add_file(
                '789_graphic.pdf', file_data))

        # width / trim
        self.expect(context.getWidth()).result(25)  # 25 %
        self.expect(context.getTrim_left()).result(10)
        self.expect(context.getTrim_bottom()).result(20)
        self.expect(context.getTrim_right()).result(30)
        self.expect(context.getTrim_top()).result(40)

        # package registration
        self.expect(layout.use_package('graphicx'))
        self.expect(layout.use_package('wrapfig'))

        # caption conversion
        self.expect(layout.get_converter().convert('My graph')).result(
            'My Graph Caption')

        self.replay()

        view = GraphicBlockLaTeXView(context, request, layout)
        latex = view.render()

        expected_latex = '\n'.join((
                r'\begin{center}',
                r'\includegraphics[width=0.25\columnwidth,clip,' + \
                    r'trim=10mm 20mm 30mm 40mm]{789_graphic.pdf}',

                r'\begin{center}',
                r'\addtocounter{figure}{1}',
                r'\addcontentsline{lof}{figure}{' + \
                    r'\protect\numberline ' + \
                    r'{\thechapter.\arabic{figure}}' + \
                    r'{\ignorespaces My Graph Caption}' + \
                    r'}',
                r'Figure \thechapter.\arabic{figure}: My Graph Caption',
                r'\end{center}',

                r'\end{center}'))

        self.assertEqual(latex, expected_latex)

    def test_register_image(self):
        file_data = 'FILE DATA'
        file_ = self.create_dummy(data=file_data)

        context = self.stub()
        self.expect(context.UID()).result('1234')
        self.expect(context.getFile()).result(file_)

        layout = self.mocker.mock()
        self.expect(layout.get_builder().add_file(
                '1234_graphic.pdf', file_data))

        request = self.create_dummy()

        self.replay()

        view = GraphicBlockLaTeXView(context, request, layout)

        self.assertEqual(view.register_image(), '1234_graphic.pdf')

    def test_get_includegraphics_cmd__all_options(self):
        context = self.stub()
        self.expect(context.getWidth()).result(75)
        self.expect(context.getTrim_left()).result(3)
        self.expect(context.getTrim_bottom()).result(4)
        self.expect(context.getTrim_right()).result(5)
        self.expect(context.getTrim_top()).result(6)

        request = self.create_dummy()
        layout = self.create_dummy()

        self.replay()

        view = GraphicBlockLaTeXView(context, request, layout)

        options = 'width=0.75\columnwidth,clip,trim=3mm 4mm 5mm 6mm'
        self.assertEqual(
            view.get_includegraphics_cmd('my_graphic.pdf'),
            r'\includegraphics[%s]{my_graphic.pdf}' % options)

    def test_get_includegraphics_cmd__no_options(self):
        context = self.stub()
        self.expect(context.getWidth()).result(100)
        self.expect(context.getTrim_left()).result(0)
        self.expect(context.getTrim_bottom()).result(0)
        self.expect(context.getTrim_right()).result(0)
        self.expect(context.getTrim_top()).result(0)

        request = self.create_dummy()
        layout = self.create_dummy()

        self.replay()

        view = GraphicBlockLaTeXView(context, request, layout)

        options = 'width=\columnwidth'
        self.assertEqual(
            view.get_includegraphics_cmd('my_graphic.pdf'),
            r'\includegraphics[%s]{my_graphic.pdf}' % options)

    def test_trim_options_without_trim(self):
        context = self.stub()
        self.expect(context.getTrim_left()).result(0)
        self.expect(context.getTrim_right()).result(0)
        self.expect(context.getTrim_top()).result(0)
        self.expect(context.getTrim_bottom()).result(0)

        request = self.create_dummy()
        layout = self.create_dummy()

        self.replay()

        view = GraphicBlockLaTeXView(context, request, layout)

        self.assertEqual(view.get_trim_options(), [])

    def test_trim_options_left_right(self):
        context = self.stub()
        self.expect(context.getTrim_left()).result(10)
        self.expect(context.getTrim_right()).result(20)
        self.expect(context.getTrim_top()).result(0)
        self.expect(context.getTrim_bottom()).result(0)

        request = self.create_dummy()
        layout = self.create_dummy()

        self.replay()

        view = GraphicBlockLaTeXView(context, request, layout)

        self.assertEqual(view.get_trim_options(), [
                'clip',
                'trim=10mm 0mm 20mm 0mm'])

    def test_trim_options_top_bottom(self):
        context = self.stub()
        self.expect(context.getTrim_left()).result(0)
        self.expect(context.getTrim_right()).result(0)
        self.expect(context.getTrim_top()).result(15)
        self.expect(context.getTrim_bottom()).result(35)

        request = self.create_dummy()
        layout = self.create_dummy()

        self.replay()

        view = GraphicBlockLaTeXView(context, request, layout)

        self.assertEqual(view.get_trim_options(), [
                'clip',
                'trim=0mm 35mm 0mm 15mm'])

    def test_get_width_option_full_width(self):
        context = self.stub()
        self.expect(context.getWidth()).result(100)

        request = self.create_dummy()
        layout = self.create_dummy()

        self.replay()

        view = GraphicBlockLaTeXView(context, request, layout)

        self.assertEqual(view.get_width_option(), [r'width=\columnwidth'])

    def test_get_width_option_half_width(self):
        context = self.stub()
        self.expect(context.getWidth()).result(50)

        request = self.create_dummy()
        layout = self.create_dummy()

        self.replay()

        view = GraphicBlockLaTeXView(context, request, layout)

        self.assertEqual(view.get_width_option(), [r'width=0.5\columnwidth'])
