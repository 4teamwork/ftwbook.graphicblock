from zope.interface import Interface


class IGraphicBlock(Interface):
    """Graphic Block for embedding PDF files into Books"""


class IGraphicConverter(Interface):
    """ Marker interface for graphics converter
    """
    def convert(graphic):
        """ Convert graphic
        """
