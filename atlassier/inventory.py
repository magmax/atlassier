import os
import logging
import yaml
import bitbucketopenapi as bitbucket

logger = logging.getLogger(__name__)


class Inventory:
    def __init__(self, path):
        self.path = path

    def load(self):
        result = {}
        for root, dirs, files in os.walk(self.path):
            for f in files:
                path = os.path.join(root, f)
                logger.debug(f"Parsing inventory file '{path}'")
                with open(path) as fd:
                    self._extend_dict(result, yaml.load(fd, Loader=yaml.FullLoader))
        return result

    def _extend_dict(self, extend_me, extend_by):
        if isinstance(extend_by, dict):
            for k, v in extend_by.items():
                if k in extend_me:
                    self._extend_dict(extend_me.get(k), v)
                else:
                    extend_me[k] = v
        else:
            extend_me += extend_by

