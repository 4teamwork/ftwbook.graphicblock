import os

try:

    from ftw.book.migration import BookTypeMigratorBase
    from ftw.upgrade.migration import DUBLIN_CORE_IGNORES
    import ftwbook.graphicblock.content.graphicblock  # noqa

except ImportError, IMPORT_ERROR:
    pass
else:
    IMPORT_ERROR = None


class GraphicBlockMigrator(BookTypeMigratorBase):

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
                    'hideFromTOC',
                )
            ),
            field_mapping={
                'showTitle': 'show_title',
            },
            additional_steps=(
                self.migrate_last_modifier,
            ) + additional_steps,
            **kwargs)

    def migrate_object(self, old_object):
        os.environ['GRAPHICBLOCK_SKIP_GENERATING_PREVIEW'] = 'true'
        try:
            return super(GraphicBlockMigrator, self).migrate_object(old_object)
        finally:
            os.environ.pop('GRAPHICBLOCK_SKIP_GENERATING_PREVIEW', None)

    def query(self):
        return {'portal_type': 'GraphicBlock'}
