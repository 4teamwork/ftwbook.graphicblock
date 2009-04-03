from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from izug.graphicblock import graphicblockMessageFactory as _

# -*- extra stuff goes here -*-

class IGraphicBlock(Interface):
    """Graphic Block for embedding PDF files into Books"""
