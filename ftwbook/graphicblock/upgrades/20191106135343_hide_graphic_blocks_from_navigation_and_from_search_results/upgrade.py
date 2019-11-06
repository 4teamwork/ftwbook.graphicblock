from ftw.upgrade import UpgradeStep


class HideGraphicBlocksFromNavigationAndFromSearchResults(UpgradeStep):
    """Hide graphic blocks from navigation and from search results.
    """

    def __call__(self):
        self.install_upgrade_profile()
