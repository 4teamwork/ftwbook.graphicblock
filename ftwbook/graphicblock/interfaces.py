from zope.interface import Interface
from zope.viewlet.interfaces import IViewletManager


class IGraphicBlock(Interface):
    """Graphic Block for embedding PDF files into Books"""


class ISimpleViewletGraphicBlockProvider(IViewletManager):
    """ ViewletManager marker interface"""


class IGraphicConverter(Interface):
    """ Marker interface for graphics converter
    """
    def convert(graphic):
        """ Convert graphic
        """
