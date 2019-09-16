import logging

import bitbucketopenapi as bitbucket

logger = logging.getLogger(__name__)


class Atlassian:
    def __init__(self, inventory, dry_run, credentials):
        self.inventory = inventory
        self.dry_run = dry_run
        self.products = [BitBucket(credentials)]
        self.resources = {}

    def fetch(self):
        for p in self.products:
            p.fetch()

    def show(self):
        for p in self.products:
            p.show()

    def run(self):
        for p in self.products:
            p.run()


class BitBucket:
    def __init__(self, credentials):
        config = bitbucket.Configuration()
        config.username = credentials.get("username")
        config.password = credentials.get("password")
        if "host" in credentials:
            config.host = credentials.get("host")

        self._client = bitbucket.ApiClient(config)

    def fetch(self):
        logger.debug("Fetching from BitBucket")
