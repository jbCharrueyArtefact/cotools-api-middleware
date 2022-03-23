from google.oauth2 import service_account
from googleapiclient.discovery import build
from time import sleep
from datetime import datetime
from app.config import DOMAIN


def list_groups(credentials):
    service = build("admin", "directory_v1", credentials=credentials)
    page_token = None
    groups_list = []
    while True:
        results = (
            service.groups()
            .list(
                domain=DOMAIN,
                maxResults=500,
                orderBy="email",
                pageToken=page_token,
            )
            .execute()
        )
        groups = results.get("groups", [])
        groups_list += __extract_group_info(groups)
        page_token = results.get("nextPageToken")
        if not page_token:
            break
        page_token = results.get("nextPageToken")
        sleep(0.1)
    return groups_list


def get_details_groups(groups, credentials):
    service = build("admin", "directory_v1", credentials=credentials)
    formated_group_members = []
    insertion_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    for group in groups:
        page_token = None
        while True:
            group_members, page_token = __get_group_members(
                group, service, page_token
            )
            formated_group_members = __format_group_members(
                group, group_members, insertion_date, formated_group_members
            )
            if not page_token:
                break
    return formated_group_members


def get_groups_from_users(users, credentials):
    service = build("admin", "directory_v1", credentials=credentials)
    users_x_groups = {}
    for user in users:
        page_token = None
        group_list = []
        while True:
            user_details = (
                service.groups()
                .list(
                    domain=DOMAIN,
                    maxResults=500,
                    userKey=user,
                    pageToken=page_token,
                )
                .execute()
            )
            user_groups = user_details.get("groups", [])
            group_list += __get_groups_from_user(user_groups)
            page_token = user_details.get("nextPageToken")
            if not page_token:
                break
        users_x_groups[user] = group_list
    return users_x_groups


def __get_groups_from_user(user_groups):
    return [group["email"] for group in user_groups]


def __extract_group_info(groups):
    groups_list = []
    for group in groups:
        groups_list.append(group["email"])
    return groups_list


def __get_group_members(group, service, page_token):
    group_details = (
        service.members()
        .list(
            includeDerivedMembership=True,
            maxResults=100,
            groupKey=group,
            pageToken=page_token,
        )
        .execute()
    )
    group_members = group_details.get("members", [])
    page_token = group_details.get("nextPageToken")
    return group_members, page_token


def __format_group_members(
    group, group_members, insertion_date, formated_group_members
):
    for member in group_members:
        user = {}
        user["user_email"] = member["email"]
        user["group_email"] = group
        user["role"] = member["role"].lower()
        user["type"] = member["type"].lower()
        user["id"] = member["id"]
        user["kind"] = member["kind"]
        user["insertion_date"] = insertion_date
        formated_group_members.append(user)
    return formated_group_members
