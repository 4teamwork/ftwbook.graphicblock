from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from zope.viewlet.interfaces import IViewletManager

from ftwbook.graphicblock import graphicblockMessageFactory as _

# -*- extra stuff goes here -*-

class IGraphicBlockLayer(Interface):
    """ Graphic block specific request layer interface
    """

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

