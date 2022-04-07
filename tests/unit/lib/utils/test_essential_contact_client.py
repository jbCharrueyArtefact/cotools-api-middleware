import unittest
import pytest
from unittest.mock import patch
from app.clients.essentialContactsClient import EssentialContactsClient
from google.api_core.exceptions import PermissionDenied
from app.lib.utils.custom_error_handling import CustomEssentialContactException
from app.models.essentialContacts import EssentialContact


contact_fixture = EssentialContact(
    email="test.test.ext@orange.com",
    notificationCategorySubscriptions=["TECHNICAL", "LEGAL"],
)


contacts_fixture = {"contacts": [contact_fixture]}


class EssentialContactsTest(unittest.TestCase):
    @patch("app.clients.essentialContactsClient.service_account")
    @patch("app.clients.essentialContactsClient.essential_contacts_v1")
    def test_list_contacts_throw_permission_denied_exception(
        self, essential_contacts_v1, service_account
    ):
        # Given
        essential_contacts_v1.EssentialContactsServiceClient.return_value.list_contacts.side_effect = PermissionDenied(
            "permission Denied"
        )
        client = EssentialContactsClient("sa")

        # When
        with pytest.raises(CustomEssentialContactException) as e:
            client.get_essential_contacts_client("fake project")

        # Then
        assert (
            e.value.message
            == "permission Denied from Essential Contact client"
        )
        assert e.value.status_code == 403

    @patch("app.clients.essentialContactsClient.service_account")
    @patch("app.clients.essentialContactsClient.essential_contacts_v1")
    def test_create_contact_throw_value_error(
        self, essential_contacts_v1, service_account
    ):
        # Given
        essential_contacts_v1.EssentialContactsServiceClient.return_value.create_contact.side_effect = ValueError(
            "Value Error"
        )
        client = EssentialContactsClient("sa")

        # When
        with pytest.raises(CustomEssentialContactException) as e:
            client.create_essential_contacts_client(
                "fake project", contact_fixture
            )

        # Then
        assert e.value.message == "Value Error from Essential Contact client"
        assert e.value.status_code == 500

    @patch("app.clients.essentialContactsClient.service_account")
    @patch("app.clients.essentialContactsClient.essential_contacts_v1")
    def test_create_contact_throw_permission_denied_error(
        self, essential_contacts_v1, service_account
    ):
        # Given
        essential_contacts_v1.EssentialContactsServiceClient.return_value.create_contact.side_effect = PermissionDenied(
            "Permission Denied"
        )
        client = EssentialContactsClient("sa")

        # When
        with pytest.raises(CustomEssentialContactException) as e:
            client.create_essential_contacts_client(
                "fake project", contact_fixture
            )

        # Then
        assert (
            e.value.message
            == "Permission Denied from Essential Contact client"
        )
        assert e.value.status_code == 403

    @patch("app.clients.essentialContactsClient.service_account")
    @patch("app.clients.essentialContactsClient.essential_contacts_v1")
    def test_delete_contact_throw_permission_denied_error(
        self, essential_contacts_v1, service_account
    ):
        # Given
        essential_contacts_v1.EssentialContactsServiceClient.return_value.delete_contact.side_effect = PermissionDenied(
            "Permission Denied"
        )
        client = EssentialContactsClient("sa")

        # When
        with pytest.raises(CustomEssentialContactException) as e:
            client.delete_essentialContact("fake project", contact_fixture)

        # Then
        assert (
            e.value.message
            == "Permission Denied from Essential Contact client"
        )
        assert e.value.status_code == 403

    @patch("app.clients.essentialContactsClient.service_account")
    @patch("app.clients.essentialContactsClient.essential_contacts_v1")
    def test_patch_contact_throw_permission_denied_error(
        self, essential_contacts_v1, service_account
    ):
        # Given
        essential_contacts_v1.EssentialContactsServiceClient.return_value.update_contact.side_effect = PermissionDenied(
            "Permission Denied"
        )
        client = EssentialContactsClient("sa")

        # When
        with pytest.raises(CustomEssentialContactException) as e:
            client.patch_essential_contact(
                "fake project", "fake_email", contact_fixture
            )

        # Then
        assert (
            e.value.message
            == "Permission Denied from Essential Contact client"
        )
        assert e.value.status_code == 403
