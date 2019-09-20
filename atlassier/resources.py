CURRENT_SPEC_VERSION = "0.1"


class Resource:
    def __init__(self):
        self.name = None
        self.uid = None

    def as_dict(self):
        return {
            "version": CURRENT_SPEC_VERSION,
            "kind": "repository",
            "metadata": {"name": self.name, "uid": self.uid},
        }

    def as_atlassian_object(self):
        return {"name": self.name, "uuid": self.uid}

    def load_from_atlassian_object(self, data):
        for k in vars(data):
            v = getattr(data, k)
            t = type(v)
            print(f"{k} -> {t}")
        print(dir(data))
        self.name = data["name"]
        self.uid = data.get("uuid")

        return self


class Repository(Resource):
    def __init__(self):
        super().__init__()

        self.scm = "git"
        self.main_branch = "master"
        self.project = None
        self.description = None
        self.is_private = False

    def load_from_atlassian_object(self, data):
        super().load_from_atlassian_object(data)

        self.scm = data["scm"]
        self.main_branch = data.get("mainbranch", {}).get("name", "master")
        self.project = data["project"]
        self.description = data.get("description")
        self.is_private = data.get("is_private", False)

        return self

    def as_dict(self):
        result = super().as_dict()
        result["spec"] = {
            "scm": self.scm,
            "project": self.project,
            "description": self.description,
            "is_private": self.is_private,
            "main_branch": self.main_branch,
        }
        return result

    def as_atlassian_object(self):
        result = super().as_atlassian_object()
        result["scm"] = self.scm
        result["project"] = self.project
        result["description"] = self.description
        result["is_private"] = self.is_private
        result["main_branch"] = {"name": self.main_branch, "type": "branch"}

        return result
