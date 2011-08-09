from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.layout.viewlets import ViewletBase

class SimpleLayoutGraphicBlockViewlet(ViewletBase):
    render = ViewPageTemplateFile('graphicblock_content.pt')

