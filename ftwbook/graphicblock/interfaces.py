# pylint: disable=E0211, E0213
# E0211: Method has no argument
# E0213: Method should have "self" as first argument


from ftw.book.interfaces import IBookContentType
from zope.interface import Interface


class IGraphicBlock(IBookContentType):
    """Graphic Block for embedding PDF files into Books"""


class IGraphicConverter(Interface):
    """ Marker interface for graphics converter
    """

    def __init__(context, graphic):
        """
        """

    def __call__():
        """ Convert graphic
        """


class ITypeSpecificConverter(Interface):
    """adapter interface for contenttype specific graphic converters.
    The name of the multi adapter is the normalized
    contenttype (e.g. application-pdf)
    """

    def __init__(context, graphic):
        """
        """

    def __call__():
        """ Convert graphic
        """
