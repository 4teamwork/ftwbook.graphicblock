from ftw.pdfgenerator.html2latex.utils import generate_manual_caption
from ftw.pdfgenerator.view import MakoLaTeXView
from ftwbook.graphicblock.interfaces import IGraphicBlock
from zope.component import adapter
from zope.interface import Interface


@adapter(IGraphicBlock, Interface, Interface)
class GraphicBlockLaTeXView(MakoLaTeXView):

    def render(self):
        self.layout.use_package('graphicx')
        self.layout.use_package('wrapfig')
        return '\n'.join(self.get_latex())

    def get_latex(self):
        graphicname = self.register_image()

        yield r'\begin{center}'
        yield self.get_includegraphics_cmd(graphicname)

        if self.context.show_title:
            yield generate_manual_caption(
                self.convert(self.context.Title()), 'figure').strip()

        yield r'\end{center}'

    def register_image(self):
        name = '%s_graphic.pdf' % self.context.UID()
        with self.context.file.open('r') as fio:
            self.layout.get_builder().add_file(name, fio)
        return name

    def get_includegraphics_cmd(self, name):
        options = []
        options.extend(self.get_width_option())
        options.extend(self.get_trim_options())
        return r'\includegraphics[%s]{%s}' % (','.join(options), name)

    def get_trim_options(self):
        """returns a list containing clip / trim options for the
        \includegraphics command, if there is trimming configured.
        otherwise returns an empty list
        """

        # trim must be in order left, bottom, right, top
        trim_config = (self.context.trim_left or 0,
                       self.context.trim_bottom or 0,
                       self.context.trim_right or 0,
                       self.context.trim_top or 0)

        # trim / clip only if at least one side should be trimmed
        if sum(trim_config) > 0:
            trimopt = ' '.join(['%smm' % trim for trim in trim_config])
            return ['clip', 'trim=%s' % trimopt]
        else:
            return []

    def get_width_option(self):
        """returns a list containing the width option for
        \includegraphics command
        """

        if not self.context.width or self.context.width == 100:
            val = r'\columnwidth'
        else:
            val = r'%s\columnwidth' % str(self.context.width / 100.0)
        return [r'width=%s' % val]
