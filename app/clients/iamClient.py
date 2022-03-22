from google.oauth2 import service_account
from googleapiclient import discovery
from fastapi import Response, status

from app.lib.utils.googleRestApi import GoogleRestApi


class IamClient(GoogleRestApi):
    def __init__(self, sa_info):
        credentials = service_account.Credentials.from_service_account_info(
            sa_info,
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )
        self.service = discovery.build(
            "cloudresourcemanager", "v1", credentials=credentials
        )

    def set_project_iam_rights(self, policy, project_id: str):
        try:
            body = {"policy": policy}
            self.service.projects().setIamPolicy(
                resource=project_id, body=body
            ).execute(num_retries=5)
            return {"message": "success"}
        except Exception:
            raise Exception

    def get_project_iam_rights(self, project_id: str, response: Response):

        try:
            return_value = (
                self.service.projects()
                .getIamPolicy(resource=project_id, body={})
                .execute(num_retries=5)
            )
            return return_value
        except Exception:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {}
