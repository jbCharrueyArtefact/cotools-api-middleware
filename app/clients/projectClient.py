from app.lib.utils.googleRestApi import GoogleRestApi, httpErrorHandler
import json


class ProjectClient(GoogleRestApi):
    def __init__(self, sa_info):

        super().__init__(
            sa_info, "https://cloudresourcemanager.googleapis.com/v3/"
        )

    @httpErrorHandler
    def create_project(self, name, parent, tags):
        data = {
            "parent": parent,
            "projectId": name,
            "displayName": name,
            "labels": tags,
        }
        response = self.session.post(url="projects", data=json.dumps(data))
        return response.status_code, response.json()
