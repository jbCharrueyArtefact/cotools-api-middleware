from fastapi import Depends, Request
from app.clients.bigqueryClient import BigQueryWrapper
from app.clients.billingAccountClient import BillingAccountClient
from app.clients.essentialContactsClient import EssentialContactsClient
from app.clients.projectClient import ProjectClient
from app.lib.utils.secret import get_sa_info


def get_sa_dependency(sa):
    def get_sa(request: Request):
        return get_sa_info(sa)

    return get_sa


def get_bq_client(sa=Depends(get_sa_dependency("bq"))):
    return BigQueryWrapper(sa)


def get_essential_contact_client(
    sa=Depends(get_sa_dependency("essential_contacts")),
):
    return EssentialContactsClient(sa)


def get_billing_client(sa=Depends(get_sa_dependency("create_project"))):
    return BillingAccountClient(sa)


def get_project_client(sa=Depends(get_sa_dependency("create_project"))):
    return ProjectClient(sa)
