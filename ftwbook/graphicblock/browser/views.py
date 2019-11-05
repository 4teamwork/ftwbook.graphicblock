from Products.Five.browser import BrowserView


class GraphicblockView(BrowserView):

    def get_preview_tag(self):
        scaler = self.context.restrictedTraverse('@@images')
        scale = scaler.scale('preview', scale='sl_textblock_large')
        return scale.tag()
