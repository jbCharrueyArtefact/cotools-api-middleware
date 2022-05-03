from typing import List
import pytest
import json


def payload_template(type: str, content: List[str]):
    a = {type: content}
    return a


def payload_0user():
    return payload_template("users", [])


def payload_1user_ok():
    return payload_template(
        "users", ["louis.rousselotdesaintceran.ext@orange.com"]
    )


def payload_1user_not_ok():
    return payload_template("users", ["not_ok"])


def payload_2user_ok():
    return payload_template(
        "users",
        [
            "louis.rousselotdesaintceran.ext@orange.com",
            "florent.leroy.ext@orange.com",
        ],
    )


def payload_1user_ok_but_inexistant():
    return payload_template("users", ["inexistant.inexistant@orange.com"])


def payload_1group_ok():
    return payload_template(
        "groups", ["gcp-ofr-fgt-shared-data-cotools-dev-npr@orange.com"]
    )


def payload_2group_ok():
    return payload_template(
        "groups",
        [
            "gcp-ofr-fgt-shared-data-cotools-dev-npr@orange.com",
            "gcp-ofr-fgt-backend-cotools-dev-prd@orange.com",
        ],
    )


def payload_1group_not_ok():
    return payload_template("groups", ["not_ok"])


@pytest.mark.parametrize("status_code,", [200])
def test_list_group(host, session, status_code):
    url = f"{host}/groups/"
    response1 = session.get(url=url)
    payload = payload_0user()
    response2 = session.get(url=url, data=json.dumps(payload))
    assert response1.status_code == status_code
    assert response2.status_code == status_code
    assert response1.json() == response2.json()
    assert len(response2.json()) > 1
    assert len(response1.json()) > 1


@pytest.mark.parametrize(
    "status_code,payload,len_result",
    [
        (200, payload_1user_ok(), 1),
        (200, payload_2user_ok(), 2),
        (200, payload_1user_ok_but_inexistant(), 1),
    ],
)
def test_list_group_user_ok(host, session, status_code, payload, len_result):
    url = f"{host}/groups/"
    response = session.get(url=url, data=json.dumps(payload))
    expected = (status_code, len_result)
    result = (response.status_code, len(response.json()))
    assert expected == result


@pytest.mark.parametrize(
    "status_code,payload,return_value",
    [
        (
            400,
            payload_1user_not_ok(),
            {
                "detail": "[{'message': 'Invalid Input: memberKey', 'domain': 'global', 'reason': 'invalid'}] from Group"
            },
        )
    ],
)
def test_list_group_user_not_ok(
    host, session, status_code, payload, return_value
):
    url = f"{host}/groups/"
    response = session.get(url=url, data=json.dumps(payload))
    expected = (status_code, return_value)
    result = (response.status_code, response.json())
    assert expected == result


@pytest.mark.parametrize(
    "status_code,payload,len_result",
    [
        (200, payload_1group_ok(), 1),
        (200, payload_2group_ok(), 2),
    ],
)
def test_members_group_ok(host, session, status_code, payload, len_result):
    url = f"{host}/groups/members/"
    response = session.get(url=url, data=json.dumps(payload))
    expected = (status_code, len_result)
    result = (response.status_code, len(response.json()))
    assert expected == result


@pytest.mark.parametrize(
    "status_code,payload,return_value",
    [
        (
            404,
            payload_1group_not_ok(),
            {
                "detail": "[{'message': 'Resource Not Found: groupKey', 'domain': 'global', 'reason': 'notFound'}] from Group"
            },
        )
    ],
)
def test_members_group_not_ok(
    host, session, status_code, payload, return_value
):
    url = f"{host}/groups/members/"
    response = session.get(url=url, data=json.dumps(payload))
    expected = expected = (status_code, return_value)
    result = (response.status_code, response.json())
    assert expected == result
