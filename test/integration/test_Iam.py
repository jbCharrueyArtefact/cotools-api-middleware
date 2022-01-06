import pytest
import json


def create_payload():
    data = {
        "bindings": [
            {
                "members": ["user:louis.rousselotdesaintceran.ext@orange.com"],
                "role": "roles/bigquery.admin",
            }
        ]
    }
    return data


@pytest.mark.parametrize(
    ["expected_status_code", "project_name"],
    [
        (200, "ofr-fgt-appcotools-1-dev"),
        pytest.param(404, "fake"),
    ],
)
def test_get_iam(expected_status_code, project_name, session, host):
    url = f"{host}/get_project_iam_rights/{project_name}"
    response = session.get(url=url)
    assert response.status_code == expected_status_code


@pytest.mark.parametrize(
    ["expected_response", "expected_status_code", "project_name", "payload"],
    [
        pytest.param(
            {"message": "success"},
            200,
            "ofr-fgt-appcotools-1-dev",
            create_payload(),
        ),
    ],
)
def test_set_iam(
    expected_response,
    expected_status_code,
    project_name,
    payload,
    session,
    host,
):
    url = f"{host}/set_project_iam_rights"
    payload2 = {"project_id": project_name, "details": payload}
    response = session.post(url=url, data=json.dumps(payload2))
    assert (response.json(), response.status_code) == (
        expected_response,
        expected_status_code,
    )


@pytest.mark.parametrize(
    ["equal", "project_name", "payload"],
    [
        pytest.param(True, "ofr-fgt-appcotools-1-dev", create_payload()),
        pytest.param(False, "fake", create_payload()),
    ],
)
def test_iam_changed(equal, project_name, payload, session, host):
    url = f"{host}/set_project_iam_rights"
    payload2 = {"project_id": project_name, "details": payload}
    session.post(url=url, data=json.dumps(payload2))
    response = session.get(url=f"{host}/get_project_iam_rights/{project_name}")
    if equal:
        assert response.json() == payload
    else:
        assert response.json() != payload
