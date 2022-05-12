import hvac
import os
from app import config
import cachetools.func
from google.oauth2 import service_account


@cachetools.func.ttl_cache(maxsize=128, ttl=10 * 60)
def get_secrets(secret):
    client = hvac.Client(
        url=config.VAULT, namespace="vault-cotools", verify="app/cert/cert.pem"
    )
    client.auth.ldap.login(
        username=os.environ.get("VAULT_USERNAME"),
        password=os.environ.get("VAULT_PASSWORD"),
    )

    a = client.read(path=f"/{config.VAULT_PATH}/{secret}")

    return a["data"]["data"]


@cachetools.func.ttl_cache(maxsize=128, ttl=10 * 60)
def get_sa_old(sa, engine="sa"):
    client = hvac.Client(
        url=config.VAULT, namespace="vault-cotools", verify="app/cert/cert.pem"
    )
    client.auth.ldap.login(
        username=os.environ.get("VAULT_USERNAME"),
        password=os.environ.get("VAULT_PASSWORD"),
    )

    a = client.read(path=f"/{engine}/data/{sa}")

    return a["data"]["data"]


@cachetools.func.ttl_cache(maxsize=128, ttl=10 * 60)
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


@cachetools.func.ttl_cache(maxsize=128, ttl=10 * 60)
def get_sa_info_from_shared_data_vault(sa, scopes=[]):
    client = hvac.Client(
        url=config.SA_VAULT_URL,
        namespace=config.SA_VAULT_NAMESPACE,
        verify="app/cert/cert.pem",
    )

    client.auth.approle.login(
        role_id=os.environ.get("SHARED_DATA_ROLE_ID"),
        secret_id=os.environ.get("SHARED_DATA_SECRET_ID"),
    )

    secret = client.read(
        path=f"{config.SA_VAULT_DLICE_PATH}/{config.SA_NAMES.get(sa)}"
    )

    if scopes:
        return service_account.Credentials.from_service_account_info(
            secret["data"]["data"], scopes=scopes.split("|")
        )
    else:
        return service_account.Credentials.from_service_account_info(
            secret["data"]["data"]
        )
