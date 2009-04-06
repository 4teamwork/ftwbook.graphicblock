
from izug.bibliothek.latex.ctconverter import ZugCTConverter, LatexMixinConverter

class GraphicBlockLatexConverter(ZugCTConverter, LatexMixinConverter):
    
    def __call__(self, context, view):
        super(GraphicBlockLatexConverter, self).__call__(context, view)
        latex = []
        write = lambda *a:[latex.append(x) for x in a]
        # latex mixin
        write(self.renderPreLatex(context, view))
        graphic = context.getGraphic()
        # parse arguments
        if self.context.width==100:
            command = 'figure'
            width = r'\columnwidth'
        else:
            command = 'wrapfigure'
            width = r'%f\columnwidth' % (self.context.width / float(100))
        # includegraphics options
        include_options = [
                r'width=%s' % width,
        ]
        trim = {
            'left' : self.context.trim_left,
            'right' : self.context.trim_right,
            'top' : self.context.trim_top,
            'bottom' : self.context.trim_bottom,
        }
        if len(filter(lambda x:x>0, trim.values()))>0:
            # at least one side must be trimmed, we have to specify
            # each side and add "clip" option
            include_options.append('clip')
            include_options.append('trim=%s' %
                    ' '.join(['%smm' % str(trim[k]) for k in [
                            'left',
                            'bottom',
                            'right',
                            'top',
                    ]])
            )
        # register image
        uid = '%s_image' % context.UID()
        view.addImage(uid=uid, image=graphic)
        # generate latex
        if command=='figure':
            write(r'\begin{figure}[htbp]')
        elif command=='wrapfigure':
            write(r'\begin{wrapfigure}{hl}{%s}' % width)
        write(r'\begin{center}')
        write(r'\includegraphics[%s]{%s}' % (','.join(include_options), uid))
        write(r'\end{center}')
        write(r'\end{%s}' % command)
        # latex mixin
        write(self.renderPostLatex(context, view))
        # register additional packages
        view.conditionalRegisterPackage('graphicx')
        view.conditionalRegisterPackage('wrapfig')
        return '\n'.join(latex)

