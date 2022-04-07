import unittest
import pytest
from unittest.mock import patch
from app.clients.iamClient import IamClient
from app.lib.utils.custom_error_handling import (
    CustomIamManagementException,
)
from app.roles.ProjectCreationRoles import ProjectCreationRoles
from googleapiclient.errors import HttpError


policy_fixture = {
    "bindings": [
        {
            "members": ["user:" + "test@user.com"],
            "role": ProjectCreationRoles.editor,
        }
    ],
}


# Mocking google discovery Client
class IamManagementsTests(unittest.TestCase):
    @patch("app.clients.iamClient.service_account")
    @patch("app.clients.iamClient.discovery")
    def test_get_iam(self, discovery, service_account):
        # Given
        discovery.build.return_value.projects.return_value.getIamPolicy.return_value.execute.return_value = (
            policy_fixture
        )
        client = IamClient("fake argument")

        # When
        result = client.get_project_iam_rights("project_id")

        # Then
        assert result == policy_fixture

    @patch("app.clients.iamClient.service_account")
    @patch("app.clients.iamClient.discovery")
    def test_get_iam_custom_iam_error_exception(
        self, discovery, service_account
    ):
        # Given
        discovery.build.return_value.projects.return_value.getIamPolicy.return_value.execute.side_effect = Exception(
            "message"
        )
        client = IamClient("fake argument")

        # When
        with self.assertRaises(CustomIamManagementException) as e:
            client.get_project_iam_rights("project_id")

        # Then
        assert e.exception.status_code == 500
        assert e.exception.message == "message from Iam Management client"

    @patch("app.clients.iamClient.service_account")
    @patch("app.clients.iamClient.discovery")
    def test_set_iam(self, discovery, service_account):
        # Given
        discovery.build.return_value.projects.return_value.setIamPolicy.return_value.execute.return_value = (
            policy_fixture
        )
        client = IamClient("fake argument")

        # When
        result = client.set_project_iam_rights(policy_fixture, "project_id")

        # Then
        assert result == {"message": "success"}

    @patch("app.clients.iamClient.service_account")
    @patch("app.clients.iamClient.discovery")
    def test_set_iam_custom_iam_error_exception(
        self, discovery, service_account
    ):
        # Given
        discovery.build.return_value.projects.return_value.setIamPolicy.return_value.execute.side_effect = ConnectionError(
            "message", 404
        )
        client = IamClient("fake argument")

        # When
        with pytest.raises(CustomIamManagementException) as e:
            client.set_project_iam_rights(policy_fixture, "project_id")

        # Then
        assert e.value.status_code == 500
        assert e.value.message == "message from Iam Management client"

    @patch("app.clients.iamClient.service_account")
    @patch("app.clients.iamClient.discovery")
    def test_set_iam_custom_iam_http_error_exception(
        self, discovery, service_account
    ):
        # Given
        discovery.build.return_value.projects.return_value.setIamPolicy.return_value.execute.side_effect = Exception(
            "message", 404
        )
        client = IamClient("fake argument")

        # When
        with pytest.raises(CustomIamManagementException) as e:
            client.set_project_iam_rights(policy_fixture, "project_id")

        # Then
        assert e.value.status_code == 500
        assert e.value.message == "message from Iam Management client"
