from simplelayout.base.config import CONFIGLET_INTERFACE_MAP
from simplelayout.base.utils import SlUtils
from simplelayout.types.common.browser.views import BlockView
from zope.component import queryUtility, queryMultiAdapter


class GraphicblockView(BlockView):
    """Simplelayout view for graphic blocks.
    """

    def get_content_width(self):
        """Returns the max-width of the content, determined
        by evaluating the full_size image scale.
        """

        # scale name depends on layout (two columns etc.)
        # use the scale name of the full_size of the current
        # layout for determining the maximum width of the block
        scale_name = SlUtils().getSizeAttributesByInterface(
            self.context, 'full_size')

        # the size_config contains the width for each scale
        for name, iface in CONFIGLET_INTERFACE_MAP.items():
            size_config = queryUtility(iface, name=name)

            if hasattr(size_config, scale_name):
                return getattr(size_config, scale_name)

        return 0

    def get_preview_dimensions(self):
        """returns the dimensions (width, height) as dict, in which the
        preview should be displayed.
        """

        content_width = self.get_content_width()
        width_scale = float(self.context.getWidth()) / 100  # %

        preview = self.context.getField('preview').getRaw(self.context)

        width = int(content_width * width_scale)
        height = int(
            (float(preview.height) / float(preview.width))
            * width)

        return dict(width=width, height=height)

    def get_preview_tag(self):
        scales = queryMultiAdapter((self.context, self.request),
                                   name='images')

        dimensions = self.get_preview_dimensions()
        if not dimensions['width'] or not dimensions['height']:
            return ''


        title = alt = self.context.getShowTitle() and \
            self.context.Title() or ''

        return scales.scale(
            'preview',
            **dimensions).tag(title=title, alt=alt)
