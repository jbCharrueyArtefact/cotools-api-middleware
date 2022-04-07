import json

from app.lib.utils.googleRestApi import GoogleRestApi, httpErrorHandler
from app.lib.utils.custom_error_handling import CustomEssentialContactException
from google.cloud import essential_contacts_v1
from app.models.essentialContacts import EssentialContact, EssentialContactList
from google.oauth2 import service_account
from google.api_core.exceptions import PermissionDenied


class EssentialContactsClient(GoogleRestApi):
    def __init__(self, sa_info):
        # super().__init__(
        #     sa_info, "https://essentialcontacts.googleapis.com/v1/"
        # )
        credentials = service_account.Credentials.from_service_account_info(
            sa_info,
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )
        self.client = essential_contacts_v1.EssentialContactsServiceClient(
            credentials=credentials
        )

    def is_requestable(self, project_id):
        response = self.session.get(url=f"projects/{project_id}/contacts")
        return response

    @httpErrorHandler
    def get_essential_contacts(self, project_id):
        response = self.session.get(url=f"projects/{project_id}/contacts")
        return response.status_code, EssentialContactList(**response.json())

    def get_essential_contacts_client(self, project_id):
        # Initialize request argument(s)
        try:
            name = f"projects/{project_id}"
            request = essential_contacts_v1.ListContactsRequest(
                parent=name,
            )

            # Make the request

            response = self.client.list_contacts(request=request)
            contacts_out = []
            for response_contact in response:
                list_cat = []
                for (
                    cat
                ) in response_contact.notification_category_subscriptions:
                    list_cat.append(cat.name)
                contacts_out.append(
                    EssentialContact(
                        email=response_contact.email,
                        notificationCategorySubscriptions=list_cat,
                        name=response_contact.name,
                    )
                )
            return EssentialContactList(contacts=contacts_out)
        except PermissionDenied as e:
            raise CustomEssentialContactException(e.message, e.code)
        except Exception as e:
            raise CustomEssentialContactException(e.message, e.code)

    def delete_essentialContact(self, project_id, email):
        return self._get_id_by_contact_mail_and_func(
            project_id, email, self._del_essential_contact_by_id_client
        )

    @httpErrorHandler
    def create_essentialContacts(self, project_id, data: EssentialContact):
        sentData = {
            "email": data.email,
            "notificationCategorySubscriptions": data.notificationCategorySubscriptions,
            "languageTag": "en",
        }
        response = self.session.post(
            url=f"projects/{project_id}/contacts", data=json.dumps(sentData)
        )
        return response.status_code, response.json()

    def create_essential_contacts_client(
        self, project_id, data: EssentialContact
    ):
        # Create a client
        try:
            contact = {
                "email": data.email,
                "notification_category_subscriptions": data.notificationCategorySubscriptions,
                "language_tag": "en",
            }
            # Initialize request argument(s)
            request = essential_contacts_v1.CreateContactRequest(
                parent=f"projects/{project_id}", contact=contact
            )

            # Make the request
            response = self.client.create_contact(request=request)
            return response
        except ValueError as e:
            raise CustomEssentialContactException(e.args[0], 500)
        except Exception as e:
            raise CustomEssentialContactException(e.message, e.code)

    def patch_essential_contact(self, project_id, contact_email, data):
        self._get_id_by_contact_mail_and_func(
            project_id=project_id,
            contact_email=contact_email,
            func=self._patch_essential_contact_by_id_client,
            data=data,
        )

    def _get_id_by_contact_mail_and_func(
        self, project_id, contact_email, func, **kwargs
    ):
        name = self.get_essential_contact(
            project_id=project_id, contact_email=contact_email
        )
        return func(contact_name=name, **kwargs)

    def get_essential_contact(self, project_id, contact_email):
        for contact in self.get_essential_contacts_client(
            project_id
        ).essentialContacts:
            if contact.email == contact_email:
                return contact.name

    @httpErrorHandler
    def _del_essential_contact_by_id(self, contact_id):

        response = self.session.delete(url=f"{contact_id}")
        return response.status_code, response.json

    def _del_essential_contact_by_id_client(self, contact_name):

        # Initialize request argument(s)

        try:
            request = essential_contacts_v1.DeleteContactRequest(
                name=contact_name,
            )

            # Make the request
            self.client.delete_contact(request=request)
        except Exception as e:
            raise CustomEssentialContactException(e.message, e.code)

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
            url=f"{contact_id}", data=json.dumps(sentData)
        )

        return response.status_code, response.json

    def _patch_essential_contact_by_id_client(self, contact_name, data):

        try:
            contact = {
                "name": contact_name,
                "email": data.email,
                "notification_category_subscriptions": data.notificationCategorySubscriptions,
                "language_tag": "en",
            }
            # Initialize request argument(s)
            request = essential_contacts_v1.UpdateContactRequest(
                contact=contact
            )

            # Make the request
            response = self.client.update_contact(request=request)
            return response
        except Exception as e:
            raise CustomEssentialContactException(e.message, e.code)
