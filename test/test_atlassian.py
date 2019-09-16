import datetime
from unittest import TestCase
from unittest.mock import patch

from atlassier.atlassian import BitBucket
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
        "links": {
            "_self": {
                "href": "https://api.bitbucket.org/2.0/users/%7Bd454e901-6c1b-49a7-ad8e-0b5cb95d8e8a%7D",
                "name": None,
            },
            "avatar": {"href": "https://secure.gravatar.com/whatever", "name": None},
            "followers": None,
            "following": None,
            "html": {
                "href": "https://bitbucket.org/%7Bd454e901-6c1b-49a7-ad8e-0b5cb95d8e8a%7D/",
                "name": None,
            },
            "repositories": None,
        },
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


class BitbucketTest(TestCase):
    @patch("bitbucketopenapi.RepositoriesApi.get_repositories_by_username_by_repo_slug")
    def test_fetch_gdcr14(self, method):
        method.return_value = BITBUCKET_GDCR14_REPOSITORY
        bb = BitBucket({"username": "foo"})
        result = bb.fetch_repository("gdcr14")
        assert result == {
            "description": "Global Day of Code Retreat 2014 Ciudad Real",
            "is_private": False,
            "main_branch": "master",
            "name": "gdcr14",
            "project": None,
            "scm": "git",
        }
