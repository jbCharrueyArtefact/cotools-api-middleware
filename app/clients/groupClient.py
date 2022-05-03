from typing import Dict, List
from requests import session
from app import config
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2 import service_account
import json
from googleapiclient.discovery import build
from time import sleep
from googleapiclient.errors import HttpError

from app.lib.utils.custom_error_handling import CustomGroupClientException


class GroupClient:
    def __init__(self, credentials_creation, credentials):

        creds = service_account.IDTokenCredentials.from_service_account_info(
            credentials_creation,
            target_audience=config.GROUP_CREATION_CLIENT_ID,
        )

        creds.refresh(GoogleRequest())
        token = creds.token
        self._service = build("admin", "directory_v1", credentials=credentials)
        self._create_session = session()
        self._create_session.headers.update(
            {
                "Authorization": "Bearer {}".format(token),
                "accept": "application/json",
                "Content-Type": "application/json",
            }
        )

    def create_group(
        self, manager: str, name: str, description: str, mail: str
    ):
        params = {"manager": manager}
        data = {"mail": mail, "description": description, "name": name}
        resp = self._create_session.put(
            url=f"{config.URL_GROUP_CREATION}/createGroup/test",
            params=params,
            data=json.dumps(data),
        )
        return resp.json()

    def list_groups(self, user=None) -> List[str]:
        try:
            page_token = None
            groups_list = []
            while True:
                results = (
                    self._service.groups()
                    .list(
                        domain=config.DOMAIN,
                        maxResults=500,
                        orderBy="email",
                        userKey=user,
                        pageToken=page_token,
                    )
                    .execute()
                )
                groups = results.get("groups", [])
                groups_list.extend(groups)
                page_token = results.get("nextPageToken")
                if not page_token:
                    break
                sleep(0.1)
            return [group["email"] for group in groups_list]
        except HttpError as e:
            raise CustomGroupClientException(e.error_details, e.status_code)

    def get_details_group(self, group: str) -> List[Dict[str, str]]:
        try:
            page_token = None
            group_members = []
            while True:
                group_details = (
                    self._service.members()
                    .list(
                        includeDerivedMembership=True,
                        maxResults=100,
                        groupKey=group,
                        pageToken=page_token,
                    )
                    .execute()
                )
                group_members.extend(group_details.get("members", []))
                page_token = group_details.get("nextPageToken")
                if not page_token:
                    break
            return self.__format_group_members(group_members)
        except HttpError as e:
            raise CustomGroupClientException(e.error_details, e.status_code)

    def __format_group_members(
        self, group_members: List[Dict[str, str]]
    ) -> List[Dict[str, str]]:
        members = [
            {
                "user_email": member["email"],
                "role": member["role"].lower(),
                "type": member["type"].lower(),
                "id": member["id"],
                "kind": member["kind"],
            }
            for member in group_members
        ]
        return members
