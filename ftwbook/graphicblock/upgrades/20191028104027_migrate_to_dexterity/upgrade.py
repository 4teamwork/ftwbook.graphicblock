from ftw.upgrade import UpgradeStep


class MigrateToDexterity(UpgradeStep):
    """Migrate to Dexterity.
    """

    def __call__(self):
        self.install_upgrade_profile()
