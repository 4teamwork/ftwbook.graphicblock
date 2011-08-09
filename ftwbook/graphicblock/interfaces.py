from zope.interface import Interface


class IGraphicBlock(Interface):
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
