import datetime

from google.cloud.essential_contacts_v1.types.enums import NotificationCategory
from app.lib.ressources.models import EssentialContact, EssentialContactList
import json
import time


def modify_essentialContacts(
    project_id,
    essConClient,
    data: EssentialContactList,
    db_client,
    current_table_id,
):
    existing_contacts = essConClient.get_essentialContacts(project_id)

    _update_essential_contacts_in_cloud(
        project_id, essConClient, data, existing_contacts
    )

    _update_db(
        project_id, data, existing_contacts, db_client, current_table_id
    )


def create_essential_contact_from_list_email(
    project_id,
    list_email,
    notificationCategorySubscriptions,
    essConClient,
    db_client,
    table_id,
):
    list_contact = []
    for email in list_email:
        essContacte = EssentialContact(
            email=email,
            notificationCategorySubscriptions=[
                notificationCategorySubscriptions
            ],
        )
        list_contact.append(essContacte)

    return modify_essentialContacts(
        project_id=project_id,
        essConClient=essConClient,
        data=EssentialContactList(essentialContacts=list_contact),
        db_client=db_client,
        current_table_id=table_id,
    )


def wait_essential_contacts_disponibility(client, name):
    created = False
    count = 10

    while not created:
        try:
            time.sleep(1)
            client.get_essentialContacts(name)
            created = True
            count -= 1
        except Exception:
            print("Permission denied retrying")


def _update_essential_contacts_in_cloud(
    project_id, essConClient, data, existing_contacts: EssentialContactList
):

    arriving_contacts_email = _list_email_from_ContactList(data)
    existing_contacts_email = _list_email_from_ContactList(existing_contacts)

    _create_or_patch_essential_contacts(
        project_id, essConClient, data, existing_contacts_email
    )

    _delete_essential_contacts(
        project_id, essConClient, existing_contacts, arriving_contacts_email
    )


def _list_email_from_ContactList(ContactList: EssentialContactList):
    return [contact.email for contact in ContactList.essentialContacts]


def _create_or_patch_essential_contacts(
    project_id, essConClient, data, existing_contact_email
):
    for contact in data.essentialContacts:

        if contact.email in existing_contact_email:
            essConClient.patch_essentialContact(
                project_id, contact.email, data=contact
            )

        else:
            essConClient.create_essentialContacts(
                project_id=project_id, data=contact
            )


def _delete_essential_contacts(
    project_id, essConClient, existing_contacts, arriving_contact_email
):
    for existing_contact in existing_contacts.essentialContacts:
        if existing_contact.email not in arriving_contact_email:
            essConClient.delete_essentialContact(
                project_id=project_id, email=existing_contact.email
            )


def _update_db(
    project_id, data, existing_contacts, db_client, current_table_id
):
    arriving = _create_rows_from_contact_list(project_id, data)
    existing = _create_rows_from_contact_list(project_id, existing_contacts)

    to_disable = [d for d in existing if d not in arriving]

    to_enable = [d for d in arriving if d not in existing]
    rows = []
    _add_status_and_datetime_and_append(to_disable, "disabled", rows)
    _add_status_and_datetime_and_append(to_enable, "enabled", rows)

    if len(rows) > 0:

        return db_client.insert_data(current_table_id, rows)

    else:
        return None


def _create_rows_from_contact_list(
    project_id, contact_list: EssentialContactList
):
    return [
        {
            "project": project_id,
            "email": contact.email,
            "notificationCategory": role,
        }
        for contact in contact_list.essentialContacts
        for role in contact.notificationCategorySubscriptions
    ]


def _add_status_and_datetime_and_append(input_list, status, output_list):
    for row in input_list:

        row["status"] = status
        row["time"] = datetime.datetime.now()
        output_list.append(row)
