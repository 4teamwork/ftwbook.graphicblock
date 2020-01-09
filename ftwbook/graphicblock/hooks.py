from plone.registry.interfaces import IRegistry
from zope.component import getUtility
import pkg_resources


IS_PLONE_5 = pkg_resources.get_distribution('Products.CMFPlone').version >= '5'


def uninstalled(site):
    if IS_PLONE_5:
        clean_plone5_registry(site)


def clean_plone5_registry(site):
    registry = getUtility(IRegistry)
    types_not_searched = list(registry['plone.types_not_searched'])
    types_not_searched.remove('ftwbook.graphicblock.GraphicBlock')
    registry['plone.types_not_searched'] = tuple(types_not_searched)
