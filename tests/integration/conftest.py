import pytest
import requests
import json
import os


sess = requests.session()
sess.headers.update(
    {
        "accept": "application/json",
        "Content-Type": "application/json",
    }
)


@pytest.fixture(scope="session")
def env():
    return os.environ.get("CI_JOB_STAGE", "local")


@pytest.fixture(scope="session")
def config(env):
    with open("./tests/integration/config.json") as conf:
        config = json.load(conf)
    return config.get(env)


@pytest.fixture(scope="session")
def session():
    yield sess


@pytest.fixture(scope="session")
def host(config):
    return f'{config["host"]}:{config["port"]}'
