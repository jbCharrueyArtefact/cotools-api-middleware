import pytest
import json
from app.roles.ProjectCreationRoles import ProjectCreationRoles

test_user = "user:louis.rousselotdesaintceran.ext@orange.com"
test_service_account = (
    "serviceAccount:196576718626-compute@developer.gserviceaccount.com"
)
test_group_user = "group:gcp-ofr-FGT-test-cotools-tests-dev-dev@orange.com"


def create_payload(user, role):
    data = {
        "bindings": [
            {
                "members": [user],
                "role": role,
            }
        ]
    }

    return data


@pytest.mark.parametrize(
    ["expected_status_code", "project_id"],
    [
        (200, "ofr-fgt-appcotools-1-dev"),
        (403, "fake"),
        (403, "nautilus-sandbox-268214"),
    ],
)
def test_get_iam(expected_status_code, project_id, session, host):
    url = f"{host}/projects/{project_id}/iam/"
    response = session.get(url=url)
    assert response.status_code == expected_status_code


@pytest.mark.parametrize(
    ["expected_response", "expected_status_code", "project_id", "payload"],
    [
        pytest.param(
            {"message": "success"},
            200,
            "ofr-fgt-appcotools-1-dev",
            create_payload(test_user, ProjectCreationRoles.editor),
        ),
        pytest.param(
            {"message": "success"},
            200,
            "ofr-fgt-appcotools-1-dev",
            create_payload(test_group_user, ProjectCreationRoles.editor),
        ),
        pytest.param(
            {"message": "success"},
            200,
            "ofr-fgt-appcotools-1-dev",
            create_payload(test_service_account, ProjectCreationRoles.editor),
        ),
        pytest.param(
            {
                "message": "User fake_user@orange.com does not exist. from Iam Management client"
            },
            400,
            "ofr-fgt-appcotools-1-dev",
            create_payload(
                "user:fake_user@orange.com", ProjectCreationRoles.editor
            ),
        ),
        pytest.param(
            {
                "message": "User louis.rousselotdesaintceran.ext@artefact.com does not exist. from Iam Management client"
            },
            400,
            "ofr-fgt-appcotools-1-dev",
            create_payload(
                "user:louis.rousselotdesaintceran.ext@artefact.com",
                ProjectCreationRoles.editor,
            ),
        ),
        pytest.param(
            {
                "message": "Request contains an invalid argument. from Iam Management client"
            },
            400,
            "fake_project",
            create_payload(test_user, ProjectCreationRoles.editor),
        ),
        pytest.param(
            {
                "message": "Role (roles/servicemanagement.serviceConsumer) does not exist in the resource's hierarchy. from Iam Management client"
            },
            400,
            "ofr-fgt-appcotools-1-dev",
            create_payload(
                test_user, ProjectCreationRoles.serviceManagementConsumer
            ),
        ),
        pytest.param(
            {
                "detail": [
                    {
                        "loc": ["body", "details"],
                        "msg": "value is not a valid dict",
                        "type": "type_error.dict",
                    }
                ]
            },
            422,
            "ofr-fgt-appcotools-1-dev",
            json.dumps("This is a fake json to throw an error"),
        ),
        pytest.param(
            {"message": "success"},
            200,
            "ofr-fgt-appcotools-1-dev",
            create_payload(test_user, ProjectCreationRoles.viewer),
        ),
    ],
)
def test_set_iam(
    expected_response,
    expected_status_code,
    project_id,
    payload,
    session,
    host,
):
    url = f"{host}/projects/{project_id}/iam/"
    payload2 = {"details": payload}
    response = session.patch(url=url, data=json.dumps(payload2))
    assert response.json() == expected_response
    assert response.status_code == expected_status_code


@pytest.mark.parametrize(
    ["equal", "project_id", "payload"],
    [
        pytest.param(
            True,
            "ofr-fgt-appcotools-1-dev",
            create_payload(test_user, ProjectCreationRoles.editor),
        ),
        pytest.param(
            False,
            "fake",
            create_payload(test_user, ProjectCreationRoles.editor),
        ),
    ],
)
def test_iam_changed(equal, project_id, payload, session, host):
    url = f"{host}/projects/{project_id}/iam/"
    payload2 = {"details": payload}
    session.patch(url=url, data=json.dumps(payload2))
    response = session.get(url=f"{host}/projects/{project_id}/iam/")
    if equal:
        assert response.json() == payload
    else:
        assert response.json() != payload
