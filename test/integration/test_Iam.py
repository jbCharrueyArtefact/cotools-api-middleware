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
    ["expected_status_code", "project_id"],
    [
        (200, "ofr-fgt-appcotools-1-dev"),
        pytest.param(404, "fake"),
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
            create_payload(),
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
    assert (response.json(), response.status_code) == (
        expected_response,
        expected_status_code,
    )


@pytest.mark.parametrize(
    ["equal", "project_id", "payload"],
    [
        pytest.param(True, "ofr-fgt-appcotools-1-dev", create_payload()),
        pytest.param(False, "fake", create_payload()),
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
