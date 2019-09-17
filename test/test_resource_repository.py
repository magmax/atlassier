import datetime
from unittest import TestCase

from atlassier.resources import Repository
from dateutil.tz import tzutc

BITBUCKET_GDCR14_REPOSITORY = {
    "created_on": datetime.datetime(2014, 11, 14, 9, 1, 14, 102407, tzinfo=tzutc()),
    "description": "Global Day of Code Retreat 2014 Ciudad Real",
    "fork_policy": "allow_forks",
    "full_name": "magmax/gdcr14",
    "has_issues": False,
    "has_wiki": False,
    "is_private": False,
    "language": "",
    "links": {
        "_self": {
            "href": "https://api.bitbucket.org/2.0/repositories/magmax/gdcr14",
            "name": None,
        }
    },
    "mainbranch": {"name": "master", "type": "branch"},
    "name": "gdcr14",
    "owner": {
        "account_status": None,
        "created_on": None,
        "display_name": "Miguel Angel García",
        "has_2fa_enabled": None,
        "links": {},
        "nickname": "Miguel García",
        "username": None,
        "uuid": "{d454e901-6c1b-49a7-ad8e-0b5cb95d8e8a}",
        "website": None,
    },
    "parent": None,
    "project": None,
    "scm": "git",
    "size": 411235,
    "updated_on": datetime.datetime(2016, 9, 30, 6, 4, 18, 250075, tzinfo=tzutc()),
    "uuid": "{dd848870-5738-4f46-bd9a-cdc6b5a9667a}",
}


class RepositoryTest(TestCase):
    def setUp(self):
        self.repository = Repository()

    def test_default_dict(self):
        assert self.repository.as_dict() == {
            "kind": "repository",
            "metadata": {"name": None, "uid": None},
            "spec": {
                "description": None,
                "is_private": False,
                "main_branch": "master",
                "project": None,
                "scm": "git",
            },
            "version": "0.1",
        }

    def test_default_atlassian_object(self):
        assert self.repository.as_atlassian_object() == {
            "description": None,
            "is_private": False,
            "main_branch": {"name": "master", "type": "branch"},
            "name": None,
            "project": None,
            "scm": "git",
            "uuid": None,
        }

    def test_load_resource(self):
        self.repository.load_from_atlassian_object(BITBUCKET_GDCR14_REPOSITORY)

        assert self.repository.as_dict() == {
            "kind": "repository",
            "metadata": {
                "name": "gdcr14",
                "uid": "{dd848870-5738-4f46-bd9a-cdc6b5a9667a}",
            },
            "spec": {
                "description": "Global Day of Code Retreat 2014 Ciudad Real",
                "is_private": False,
                "main_branch": "master",
                "project": None,
                "scm": "git",
            },
            "version": "0.1",
        }
