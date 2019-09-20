import logging

import bitbucketopenapi as bitbucket
from atlassier import resources

logger = logging.getLogger(__name__)


class Atlassian:
    def __init__(self, inventory, dry_run, credentials):
        self.inventory = inventory
        self.dry_run = dry_run
        self.products = [BitBucket(credentials)]
        self.resources = {}

    def get_resource(self, kind, name):
        method_name = f"get_{kind}"
        for p in self.products:
            if hasattr(p, method_name):
                method = getattr(p, method_name)
                print(method)
                method(name)

    def get(self):
        for p in self.products:
            p.get()

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

    def get_repository(self, repository_name, owner=None):
        owner = owner or self._username
        logger.debug(f"Fetching repository {owner}/{repository_name} from BitBucket")
        api = bitbucket.RepositoriesApi(self._client)
        data = api.get_repositories_by_username_by_repo_slug(owner, repository_name)
        return resources.Repository().load_from_atlassian_object(data)
