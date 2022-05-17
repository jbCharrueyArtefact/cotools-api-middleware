import pytest
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


def message(success=True):
    if success:
        message = {"message": "success"}
    else:
        message = {
            "detail": "{'error': {'code': 403, 'message': 'The caller does not have permission', 'status': 'PERMISSION_DENIED'}} from Essential Contact"
        }
    return message


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
    # breakpoint()
    # assert EssentialContactListOut(**response.json())


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
            create_payload(["ALL"], True),
            # marks=pytest.mark.xfail,
        ),  # all good
        pytest.param(
            message(True),
            200,
            "ofr-fgt-appcotools-1-dev",
            create_payload(["LEGAL"], True),
            # marks=pytest.mark.xfail,
        ),  # all good
        pytest.param(
            message(True),
            200,
            "ofr-fgt-appcotools-1-dev",
            create_payload(["ALL"], True),
            # marks=pytest.mark.xfail,
        ),  # all good
        pytest.param(
            message(True),
            200,
            "ofr-fgt-appcotools-1-dev",
            create_payload(["LEGAL"], True),
            # marks=pytest.mark.xfail,
        ),  # all good
        pytest.param(
            message(True),
            200,
            "ofr-fgt-appcotools-1-dev",
            create_payload(["ALL"]),
            # marks=pytest.mark.xfail,
        ),  # all good
        pytest.param(
            message(False),
            403,
            "fake",
            create_payload(["ALL"]),  # marks=pytest.mark.xfail
        ),  # bad project good payload
        pytest.param(
            message(False),
            403,
            "ofr-fgt-app-cotools-1-dev",
            create_payload(["ALL"]),
            # a regarder
        ),  # good project bad payload
        pytest.param(
            message(False),
            403,
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
    url = f"{host}/projects/{project_name}/essential_contacts/"
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
    url = f"{host}/projects/{project_name}/essential_contacts/"
    session.patch(url, data=json.dumps(payload))
    response = session.get(url=url)
    if equal:
        assert response.json() == payload
    else:
        assert response.json() != payload
