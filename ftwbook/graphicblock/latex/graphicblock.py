from plonegov.pdflatex.browser.converter import LatexCTConverter


class GraphicBlockLatexConverter(LatexCTConverter):

    def __call__(self, context, view):
        self.context = context
        self.view = view

        return '\n'.join(self.get_latex())

    def get_latex(self):
        self.view.conditionalRegisterPackage('graphicx')
        self.view.conditionalRegisterPackage('wrapfig')

        graphicname = self.register_image()

        yield r'\begin{center}'
        yield self.get_includegraphics_cmd(graphicname)

        if self.context.getShowTitle():
            yield r'\caption{%s}' % self.context.Title()

        yield r'\end{center}'

    def register_image(self):
        """register the graphic file. returns the graphic name
        """

        graphicname = '%s_graphic' % self.context.UID()
        self.view.addImage(uid=graphicname,
                           image=self.context.getFile())
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
            val = r'%f\columnwidth' % (
                self.context.getWidth() / float(100))

        return [r'width=%s' % val]
