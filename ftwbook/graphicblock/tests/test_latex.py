from ftwbook.graphicblock.tests import FunctionalTestCase


class TestLatex(FunctionalTestCase):

    def test_default_latex(self):
        self.assert_latex_code(
            self.graphicblock, r'''
        \label{path:/plone/the-example-book/introduction/graphicblock}
        \begin{center}
        \includegraphics[width=\columnwidth]{XBlockUUIDX_graphic.pdf}
        \begin{center}
        \addtocounter{figure}{1}
        \addcontentsline{lof}{figure}{\protect\numberline {\thechapter.\arabic{figure}}{\ignorespaces Graphicblock}}
        Figure \thechapter.\arabic{figure}: Graphicblock
        \end{center}
        \end{center}
            ''')

    def test_hide_title(self):
        self.graphicblock.show_title = True
        with self.assert_latex_diff(
                self.graphicblock,
                r'''
        --- before.tex
        +++ after.tex
        @@ -1,9 +1,4 @@
         \label{path:/plone/the-example-book/introduction/graphicblock}
         \begin{center}
         \includegraphics[width=\columnwidth]{XBlockUUIDX_graphic.pdf}
        -\begin{center}
        -\addtocounter{figure}{1}
        -\addcontentsline{lof}{figure}{\protect\numberline {\thechapter.\arabic{figure}}{\ignorespaces Graphicblock}}
        -Figure \thechapter.\arabic{figure}: Graphicblock
         \end{center}
        -\end{center}
                '''):
            self.graphicblock.show_title = False

    def test_configure_width(self):
        self.graphicblock.width = 100
        with self.assert_latex_diff(
                self.graphicblock,
                r'''
        --- before.tex
        +++ after.tex
        @@ -1,6 +1,6 @@
         \label{path:/plone/the-example-book/introduction/graphicblock}
         \begin{center}
        -\includegraphics[width=\columnwidth]{XBlockUUIDX_graphic.pdf}
        +\includegraphics[width=0.7\columnwidth]{XBlockUUIDX_graphic.pdf}
         \begin{center}
         \addtocounter{figure}{1}
         \addcontentsline{lof}{figure}{\protect\numberline {\thechapter.\arabic{figure}}{\ignorespaces Graphicblock}}
                '''):
            self.graphicblock.width = 70

    def test_configure_cropping(self):
        self.graphicblock.top = 1
        self.graphicblock.right = 2
        self.graphicblock.bottom = 3
        self.graphicblock.left = 4
        with self.assert_latex_diff(
                self.graphicblock,
                r'''
        --- before.tex
        +++ after.tex
        @@ -1,6 +1,6 @@
         \label{path:/plone/the-example-book/introduction/graphicblock}
         \begin{center}
        -\includegraphics[width=\columnwidth]{XBlockUUIDX_graphic.pdf}
        +\includegraphics[width=0.7\columnwidth]{XBlockUUIDX_graphic.pdf}
         \begin{center}
         \addtocounter{figure}{1}
         \addcontentsline{lof}{figure}{\protect\numberline {\thechapter.\arabic{figure}}{\ignorespaces Graphicblock}}
                '''):
            self.graphicblock.width = 70
