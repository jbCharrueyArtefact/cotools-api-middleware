from fastapi import Depends, Request
from app.clients.bigqueryClient import BigQueryWrapper
from app.clients.billingAccountClient import BillingAccountClient
from app.clients.essentialContactsClient import EssentialContactsClient
from app.clients.projectClient import ProjectClient
from app.clients.iamClient import IamClient
from app.lib.utils.secret import (
    get_sa_info,
    get_sa_info_from_shared_data_vault,
)
from app.clients.groupClient import GroupClient


def get_sa_dependency(sa):
    def get_sa(request: Request):
        return get_sa_info(sa)

    return get_sa


def get_shared_data_secret(sa):
    def get_sa(request: Request):
        return get_sa_info_from_shared_data_vault(sa)

    return get_sa


def get_essential_contact_client(
    sa=Depends(get_sa_dependency("essential_contacts")),
):
    return EssentialContactsClient(sa)


def get_billing_client(sa=Depends(get_sa_dependency("create_project"))):
    return BillingAccountClient(sa)


def get_project_client(sa=Depends(get_sa_dependency("create_project"))):
    return ProjectClient(sa)


def get_iam_client(sa=Depends(get_sa_dependency("iam"))):
    return IamClient(sa)


def get_bq_client(sa=Depends(get_sa_dependency("bq"))):
    return BigQueryWrapper(sa)


def get_group_client(
    credential_creation=Depends(get_sa_dependency("group_creation")),
    credentials=Depends(get_shared_data_secret("google_groups_assets")),
):
    return GroupClient(
        credentials_creation=credential_creation, credentials=credentials
    )
