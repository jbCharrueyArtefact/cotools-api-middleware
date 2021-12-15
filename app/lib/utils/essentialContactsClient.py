import json

from requests import Session
from urllib.parse import urljoin
from google.oauth2 import service_account
from google.auth.transport.requests import Request

from app.lib.ressources.models import EssentialContact, EssentialContactList


class EssentialContactsClient:
    def __init__(self, sa_info):

        self.session = _ApiSession(
            sa_info, "https://essentialcontacts.googleapis.com/v1/"
        )

    def is_requestable(self, project_id):
        response = self.session.get(url=f"projects/{project_id}/contacts")
        return response

    def get_essentialContacts(self, project_id):
        response = self.session.get(url=f"projects/{project_id}/contacts")
        return EssentialContactList(**response.json())

    def delete_essentialContact(self, project_id, email):
        return self._get_id_by_contact_mail_and_func(
            project_id, email, self._del_essential_contact_by_id
        )

    def create_essentialContacts(self, project_id, data: EssentialContact):
        sentData = {
            "email": data.email,
            "notificationCategorySubscriptions": data.notificationCategorySubscriptions,
            "languageTag": "en",
        }
        response = self.session.post(
            url=f"projects/{project_id}/contacts",
            data=json.dumps(sentData),
        )
        return response.json

    def patch_essentialContact(self, project_id, contact_email, data):
        self._get_id_by_contact_mail_and_func(
            project_id=project_id,
            contact_email=contact_email,
            func=self._patch_essential_contact_by_id,
            data=data,
        )

    def _get_id_by_contact_mail_and_func(
        self, project_id, contact_email, func, **kwargs
    ):
        name = self.get_essentialContact(
            project_id=project_id, contact_email=contact_email
        )
        return func(contact_id=name, **kwargs)

    def get_essentialContact(self, project_id, contact_email):
        for contact in self.get_essentialContacts(
            project_id
        ).essentialContacts:
            if contact.email == contact_email:
                return contact.name

    def _del_essential_contact_by_id(self, contact_id):

        response = self.session.delete(
            url=f"{contact_id}",
        )
        return response.json

    def _patch_essential_contact_by_id(
        self, contact_id, data: EssentialContact
    ):
        sentData = {
            "email": data.email,
            "notificationCategorySubscriptions": data.notificationCategorySubscriptions,
            "languageTag": "en",
        }
        response = self.session.patch(
            url=f"{contact_id}",
            data=json.dumps(sentData),
        )

        return response.json


class _ApiSession(Session):
    def __init__(self, sa, prefix_url=None, *args, **kwargs):
        super(_ApiSession, self).__init__(*args, **kwargs)
        self.prefix_url = prefix_url

        cred = service_account.Credentials.from_service_account_info(
            sa,
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )
        cred.refresh(Request())
        self.headers.update(
            {
                "Authorization": f"Bearer {cred.token}",
                "Content-Type": "application/json; charset=utf-8",
            }
        )

    def request(self, method, url, *args, **kwargs):
        url = urljoin(self.prefix_url, url)
        return super(_ApiSession, self).request(method, url, *args, **kwargs)
