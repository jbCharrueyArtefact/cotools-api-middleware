from logging import exception
import hvac
from functools import lru_cache
import os
from app import config


@lru_cache(maxsize=None)
def get_secrets(secret):
    client = hvac.Client(
        url=config.VAULT,
        namespace="vault-cotools",
        verify="app/cert/cert.pem",
    )
    client.auth.ldap.login(
        username=os.environ.get("VAULT_USERNAME"),
        password=os.environ.get("VAULT_PASSWORD"),
    )

    a = client.read(path=f"/{config.VAULT_PATH}/{secret}")

    return a["data"]["data"]


@lru_cache(maxsize=None)
def get_sa_old(sa, engine="sa"):
    client = hvac.Client(
        url=config.VAULT,
        namespace="vault-cotools",
        verify="app/cert/cert.pem",
    )
    client.auth.ldap.login(
        username=os.environ.get("VAULT_USERNAME"),
        password=os.environ.get("VAULT_PASSWORD"),
    )

    a = client.read(path=f"/{engine}/data/{sa}")

    return a["data"]["data"]


@lru_cache(maxsize=None)
def get_sa_info(sa):
    client = hvac.Client(
        url=config.SA_VAULT_URL,
        namespace=config.SA_VAULT_NAMESPACE,
        verify="app/cert/cert.pem",
    )

    client.auth.approle.login(
        role_id=os.environ.get("ROLE_ID"),
        secret_id=os.environ.get("SECRET_ID"),
    )

    secret = client.read(
        path=f"{config.SA_VAULT_PATH}{config.SA_NAMES.get(sa)}"
    )
    return secret["data"]["data"]
