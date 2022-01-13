from logging import exception
import hvac
from functools import lru_cache
import os
from app import config


@lru_cache(maxsize=None)
def get_secrets(engine, secret):
    client = hvac.Client(
        url=config.VAULT,
        namespace="vault-cotools",
        verify="app/cert/cert.pem",
    )
    client.auth.ldap.login(
        username=os.environ.get("VAULT_USERNAME"),
        password=os.environ.get("VAULT_PASSWORD"),
    )

    a = client.read(path=f"/{engine}/data/{secret}")

    return a["data"]["data"]


def get_sa_info(secret):
    return get_secrets("sa", secret)
