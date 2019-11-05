from ftw.upgrade import UpgradeStep
from ftwbook.graphicblock.migration import GraphicBlockMigrator
import os


ENV_VAR_NAME = 'FTWBOOK_GRAPHICBLOCK_SKIP_DEXTERITY_MIGRATION'


class MigrateToDexterity(UpgradeStep):
    """Migrate to Dexterity.
    """

    def __call__(self):
        self.install_upgrade_profile()
        if os.environ.get(ENV_VAR_NAME, '').lower() != 'true':
            self.migrate_to_dexterity()

    def migrate_to_dexterity(self):
        migrator = GraphicBlockMigrator()
        map(migrator.migrate_object,
            self.objects(migrator.query(),
                         'Migrate graphic block to dexterity'))
