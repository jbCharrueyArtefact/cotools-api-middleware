import pytest
from app.models.essentialContacts import (
    EssentialContactListOut,
)
import json
import random
import string


def create_payload(cat, fixed_user=False):
    letters = string.ascii_lowercase
    random1 = (
        "".join(random.choice(letters) for i in range(10))
        if not fixed_user
        else "test.test"
    )
    data = {
        "contacts": [
            {
                "email": f"{random1}@orange.com",
                "notificationCategorySubscriptions": cat,
            },
        ]
    }
    return data


def message(error_code=200):
    return {
        200: {"message": "success"},
        403: {
            "detail": "The caller does not have permission from Essential Contact client"
        },
    }[error_code]


@pytest.mark.parametrize(
    "expected_status_code, project_name",
    [
        (200, "ofr-fgt-appcotools-1-dev"),  # good project
        pytest.param(403, "fake"),  # bad project
    ],
)
def test_get_essential_contact(
    expected_status_code, project_name, host, session
):
    url = f"{host}/projects/{project_name}/essential_contacts/"
    response = session.get(url=url)
    assert expected_status_code == response.status_code
    assert EssentialContactListOut(**response.json())


@pytest.mark.parametrize(
    [
        "expected_status_code",
        "project_name",
        "payload",
    ],
    [
        pytest.param(
            200,
            "ofr-fgt-appcotools-1-dev",
            create_payload(["ALL"], True),
            # marks=pytest.mark.xfail,
        ),  # all good
        pytest.param(
            200,
            "ofr-fgt-appcotools-1-dev",
            create_payload(["LEGAL"], True),
            # marks=pytest.mark.xfail,
        ),  # all good
        pytest.param(
            200,
            "ofr-fgt-appcotools-1-dev",
            create_payload(["ALL"]),
            # marks=pytest.mark.xfail,
        ),  # all good
        pytest.param(
            403,
            "fake",
            create_payload(["ALL"]),  # marks=pytest.mark.xfail
        ),  # bad project good payload
        pytest.param(
            403,
            "ofr-fgt-app-cotools-1-dev",
            create_payload(["ALL"]),
            # a regarder
        ),  # good project bad payload
        pytest.param(
            403,
            "ofr-fgt-app-cotools-1-dev",
            create_payload(["FAKE"]),
            # marks=pytest.mark.xfail,
        ),  # good project good payload bad category
    ],
)
def test_patch_essential_contact(
    expected_status_code,
    project_name,
    payload,
    host,
    session,
):
    url = f"{host}/projects/{project_name}/essential_contacts/"
    response = session.patch(url, data=json.dumps(payload))
    expected = (expected_status_code, message(expected_status_code))
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
    url = f"{host}/projects/{project_name}/essential_contacts/"
    session.patch(url, data=json.dumps(payload))
    response = session.get(url=url)
    if equal:
        assert response.json() == payload
    else:
        assert response.json() != payload
