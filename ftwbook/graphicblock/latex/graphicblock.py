from ftw.pdfgenerator.html2latex.utils import generate_manual_caption
from ftw.pdfgenerator.view import MakoLaTeXView
from ftwbook.graphicblock.interfaces import IGraphicBlock
from zope.component import adapts
from zope.interface import Interface


class GraphicBlockLaTeXView(MakoLaTeXView):
    adapts(IGraphicBlock, Interface, Interface)

    def render(self):
        self.layout.use_package('graphicx')
        self.layout.use_package('wrapfig')

        return '\n'.join(self.get_latex())

    def get_latex(self):
        graphicname = self.register_image()

        yield r'\begin{center}'
        yield self.get_includegraphics_cmd(graphicname)

        if self.context.getShowTitle():

            yield generate_manual_caption(
                self.convert(self.context.Title()), 'figure').strip()

        yield r'\end{center}'

    def register_image(self):
        """register the graphic file. returns the graphic name
        """

        graphicname = '%s_graphic.pdf' % self.context.UID()
        self.layout.get_builder().add_file(
            graphicname, str(self.context.getFile().data))

        return graphicname

    def get_includegraphics_cmd(self, graphicname):
        """return the \includegraphics command with arguments
        """

        options = []

        options.extend(self.get_width_option())
        options.extend(self.get_trim_options())

        return r'\includegraphics[%s]{%s}' % (
            ','.join(options),
            graphicname)

    def get_trim_options(self):
        """returns a list containing clip / trim options for the
        \includegraphics command, if there is trimming configured.
        otherwise returns an empty list
        """

        # trim must be in order left, bottom, right, top
        trim_config = (self.context.getTrim_left(),
                       self.context.getTrim_bottom(),
                       self.context.getTrim_right(),
                       self.context.getTrim_top())

        # trim / clip only if at least one side should be trimmed
        if sum(trim_config) > 0:

            trimopt = ' '.join(['%smm' % trim
                                for trim in trim_config])

            return ['clip',
                    'trim=%s' % trimopt,
                    ]

        else:
            return []

    def get_width_option(self):
        """returns a list containing the width option for
        \includegraphics command
        """

        if self.context.getWidth() == 100:
            val = r'\columnwidth'
        else:
            val = r'%s\columnwidth' % str(
                self.context.getWidth() / float(100))

        return [r'width=%s' % val]
