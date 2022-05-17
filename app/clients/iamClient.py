from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from googleapiclient import discovery

from app.lib.utils.custom_error_handling import (
    CustomIamManagementException,
    CustomIamManagementError,
)
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
        except ConnectionError as e:
            raise CustomIamManagementException(e.args[0])
        except HttpError as e:
            raise CustomIamManagementError(e.error_details, e.status_code)
        except Exception as e:
            raise CustomIamManagementException(e.args[0])

    def get_project_iam_rights(self, project_id: str):
        try:
            response = (
                self.service.projects()
                .getIamPolicy(resource=project_id, body={})
                .execute(num_retries=5)
            )
            return response
        except HttpError as e:
            raise CustomIamManagementError(e.error_details, e.status_code)
        except Exception as e:
            raise CustomIamManagementException(e.args[0])
