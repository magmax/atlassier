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
    def __init__(self, credentials, api=bitbucket):
        config = api.Configuration()
        config.username = credentials.get("username")
        config.password = credentials.get("password")
        if "host" in credentials:
            config.host = credentials.get("host")

        self._client = api.ApiClient(config)
        self._username = config.username

    def fetch_repository(self, repository_name):
        logger.debug(f"Fetching repository {repository_name} from BitBucket")
        api = bitbucket.RepositoriesApi(self._client)
        data = api.get_repositories_by_username_by_repo_slug(
            self._username, repository_name
        )
        return {
            "name": data["name"],
            "scm": data["scm"],
            "project": data["project"],
            "description": data["description"],
            "is_private": data["is_private"],
            "main_branch": data["mainbranch"]["name"],
        }
