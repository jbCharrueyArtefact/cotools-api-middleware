from fastapi import APIRouter, Depends, Response, status
from app.dependencies import get_bq_client
from app.lib.utils.customRoute import CustomRoute
from app.models.iam import (
    HistoricalIamDetails,
    Policy,
    SetIamDetails,
)

from app import config


from google.oauth2 import service_account
from googleapiclient import discovery
from app.lib.utils.iam import get_interval_historical_data

from app.lib.utils.secret import get_sa_info


subrouter = APIRouter(route_class=CustomRoute)


@subrouter.get("/", response_model=Policy)
def get_project_iam_rights(project_id: str, response: Response):
    credentials = service_account.Credentials.from_service_account_info(
        get_sa_info("iam"),
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    service = discovery.build(
        "cloudresourcemanager", "v1", credentials=credentials
    )

    try:
        return_value = (
            service.projects()
            .getIamPolicy(resource=project_id, body={})
            .execute(num_retries=5)
        )
        return return_value
    except Exception:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {}


@subrouter.patch("/")
def set_project_iam_rights(
    request: SetIamDetails, project_id: str, response: Response
):
    credentials = service_account.Credentials.from_service_account_info(
        get_sa_info("iam"),
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )

    service = discovery.build(
        "cloudresourcemanager", "v1", credentials=credentials
    )

    try:

        body = {"policy": request.details.dict()}
        response = (
            service.projects()
            .setIamPolicy(resource=project_id, body=body)
            .execute(num_retries=5)
        )
        return {"message": "success"}
    except Exception as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "failed", "error": str(e.error_details)}


@subrouter.get("/history/")
def list_iam_history(
    project_id, interval: HistoricalIamDetails, bqclient=Depends(get_bq_client)
):
    time_interval = get_interval_historical_data(interval)
    query_root = f"SELECT * FROM `{config.REFERENCE_TABLE_IAM_HISTORY}` where project_name = '{str(project_id)}'"
    query = (
        f"{query_root} AND {time_interval}" if time_interval else query_root
    )
    result = bqclient.query_data(query)
    return [dict(row) for row in result]
