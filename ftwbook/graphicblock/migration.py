from ftw.upgrade.migration import InplaceMigrator
from zope.annotation.interfaces import IAnnotations

try:

    from ftw.upgrade.migration import DUBLIN_CORE_IGNORES
    import ftwbook.graphicblock.content.graphicblock  # noqa

except ImportError, IMPORT_ERROR:
    pass
else:
    IMPORT_ERROR = None


class GraphicBlockMigrator(InplaceMigrator):

    def __init__(self, ignore_fields=(), additional_steps=(), **kwargs):
        if IMPORT_ERROR:
            raise IMPORT_ERROR

        super(GraphicBlockMigrator, self).__init__(
            new_portal_type='ftwbook.graphicblock.GraphicBlock',
            ignore_fields=(
                DUBLIN_CORE_IGNORES
                + ignore_fields + (
                    'description',
                    'effectiveDate',
                    'excludeFromNav',
                    'expirationDate',
                    'lastModifier',
                    'searchwords',
                    'showinsearch',
                    'subject',
                )
            ),
            field_mapping={
                'showTitle': 'show_title',
            },
            additional_steps=(
                self.migrate_last_modifier,
            ) + additional_steps,
            **kwargs)

    def query(self):
        return {'portal_type': 'GraphicBlock'}

    def migrate_last_modifier(self, old_object, new_object):
        value = getattr(old_object, 'lastModifier', None)
        if value:
            IAnnotations(new_object)['collective.lastmodifier'] = value