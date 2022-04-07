from googleapiclient.errors import HttpError
from googleapiclient import discovery
from google.oauth2 import service_account

from app.lib.utils.googleRestApi import GoogleRestApi
from app.lib.utils.custom_error_handling import CustomProjectCreationException


class ProjectClient(GoogleRestApi):
    def __init__(self, sa_info):

        credentials = service_account.Credentials.from_service_account_info(
            sa_info,
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )
        self.service = discovery.build(
            "cloudresourcemanager", "v3", credentials=credentials
        )

    def create_project(self, name, parent, tags):
        try:
            self.service.projects().create(
                body={
                    "project_id": name,
                    "displayName": name,
                    "parent": parent,
                    "labels": tags,
                }
            ).execute()
        except HttpError as e:
            raise CustomProjectCreationException(
                e.error_details, e.status_code
            )
