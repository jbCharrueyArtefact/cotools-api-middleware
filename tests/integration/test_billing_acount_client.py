import pytest


@pytest.mark.parametrize(
    ["expected_status_code", "project_id"],
    [
        (200, "ofr-fgt-appcotools-1-dev"),
        (403, "fake"),
    ],
)
def test_get_iam(expected_status_code, project_id, session, host):
    url = f"{host}/projects/{project_id}/iam/"
    response = session.get(url=url)
    assert response.status_code == expected_status_code
