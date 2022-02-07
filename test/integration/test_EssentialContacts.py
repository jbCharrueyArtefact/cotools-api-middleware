import pytest
from app.lib.ressources.models import (
    EssentialContactList,
    EssentialContactListOut,
)
import json
import random
import string


def create_payload(cat):
    letters = string.ascii_lowercase
    random1 = "".join(random.choice(letters) for i in range(10))
    data = {
        "contacts": [
            {
                "email": f"{random1}@orange.com",
                "notificationCategorySubscriptions": cat,
            },
        ]
    }
    return data


def message(success=True):
    if success:
        message = "success"
    else:
        message = "failed"
    return {"message": f"{message}"}


@pytest.mark.parametrize(
    "expected_status_code, project_name",
    [
        (200, "ofr-fgt-appcotools-1-dev"),  # good project
        pytest.param(404, "fake"),  # bad project
    ],
)
def test_get_essential_contact(
    expected_status_code, project_name, host, session
):
    url = f"{host}/projects/{project_name}/essential_contacts"
    response = session.get(url=url)
    assert expected_status_code == response.status_code
    assert EssentialContactListOut(**response.json())


@pytest.mark.parametrize(
    [
        "expected_response",
        "expected_status_code",
        "project_name",
        "payload",
    ],
    [
        pytest.param(
            message(True),
            200,
            "ofr-fgt-appcotools-1-dev",
            create_payload(["ALL"]),
            # marks=pytest.mark.xfail,
        ),  # all good
        pytest.param(
            message(False),
            404,
            "fake",
            create_payload(["ALL"]),  # marks=pytest.mark.xfail
        ),  # bad project good payload
        pytest.param(
            message(False),
            404,
            "ofr-fgt-app-cotools-1-dev",
            create_payload(["ALL"]),
            #
        ),  # good project bad payload
        pytest.param(
            message(False),
            404,
            "ofr-fgt-app-cotools-1-dev",
            create_payload(["FAKE"]),
            # marks=pytest.mark.xfail,
        ),  # good project good payload bad category
    ],
)
def test_patch_essential_contact(
    expected_response,
    expected_status_code,
    project_name,
    payload,
    host,
    session,
):
    url = f"{host}/projects/{project_name}/essential_contacts"
    response = session.patch(url, data=json.dumps(payload))
    expected = (expected_status_code, expected_response)
    result = (response.status_code, response.json())
    assert expected == result


@pytest.mark.parametrize(
    ["equal", "project_name", "payload"],
    [
        (
            True,
            "ofr-fgt-appcotools-1-dev",
            create_payload(["LEGAL"]),
        ),  # all good
        (
            False,
            "ofr-fgt-appcotools-1-dev",
            create_payload(["FAKE"]),
        ),  # good project bad category
    ],
)
def test_change_working_patch(equal, project_name, payload, host, session):
    url = f"{host}/projects/{project_name}/essential_contacts"
    session.patch(url, data=json.dumps(payload))
    response = session.get(url=url)
    if equal:
        assert response.json() == payload
    else:
        assert response.json() != payload
