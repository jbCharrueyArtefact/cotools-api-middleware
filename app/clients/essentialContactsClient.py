import json
from app.lib.utils.googleRestApi import GoogleRestApi, httpErrorHandler
from app.models.essentialContacts import EssentialContact, EssentialContactList


class EssentialContactsClient(GoogleRestApi):
    def __init__(self, sa_info):

        super().__init__(
            sa_info, "https://essentialcontacts.googleapis.com/v1/"
        )

    def is_requestable(self, project_id):
        response = self.session.get(url=f"projects/{project_id}/contacts")
        return response

    @httpErrorHandler
    def get_essentialContacts(self, project_id):
        response = self.session.get(url=f"projects/{project_id}/contacts")
        return response.status_code, EssentialContactList(**response.json())

    def delete_essentialContact(self, project_id, email):
        return self._get_id_by_contact_mail_and_func(
            project_id, email, self._del_essential_contact_by_id
        )

    @httpErrorHandler
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
        return response.status_code, response.json()

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

    @httpErrorHandler
    def _del_essential_contact_by_id(self, contact_id):

        response = self.session.delete(
            url=f"{contact_id}",
        )
        return response.status_code, response.json

    @httpErrorHandler
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

        return response.status_code, response.json
