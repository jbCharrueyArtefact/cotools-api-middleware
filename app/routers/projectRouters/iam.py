from fastapi import APIRouter, Depends, Response
from app.dependencies import get_iam_client
from app.lib.utils.customRoute import CustomRoute
from app.models.iam import Policy, SetIamDetails

from app.lib.utils.iam import get_interval_historical_data
from app.dependencies import get_bq_client
from app import config
from app.models.iam import HistoricalIamDetails
from app.lib.utils.custom_error_handling import (
    CustomIamManagementException,
    CustomIamManagementError,
)

subrouter = APIRouter(route_class=CustomRoute)


@subrouter.get("/", response_model=Policy)
def get_project_iam_rights(
    project_id: str, response: Response, iam_client=Depends(get_iam_client)
):
    try:
        return iam_client.get_project_iam_rights(project_id)
    except (CustomIamManagementError, CustomIamManagementException) as e:
        response.status_code = e.status_code
        return {"message": e.message}


@subrouter.patch("/")
def set_project_iam_rights(
    request: SetIamDetails,
    project_id: str,
    response: Response,
    iamClient=Depends(get_iam_client),
):
    try:
        return iamClient.set_project_iam_rights(
            request.details.dict(), project_id
        )
    except (CustomIamManagementError, CustomIamManagementException) as e:
        response.status_code = e.status_code
        return {"message": e.message}


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
