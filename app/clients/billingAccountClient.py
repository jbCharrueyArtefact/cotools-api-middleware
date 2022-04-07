from app.lib.utils.googleRestApi import GoogleRestApi, httpErrorHandler
import json


class BillingAccountClient(GoogleRestApi):
    def __init__(self, sa_info):
        super().__init__(sa_info, "https://cloudbilling.googleapis.com/v1/")
        # credentials = service_account.Credentials.from_service_account_info(
        #     sa_info,
        #     scopes=["https://www.googleapis.com/auth/cloud-platform"],
        # )
        # self.client = billing_v1.CloudBillingClient(credentials=credentials)

    @httpErrorHandler
    def set_billing_account(self, project_id, billing_id):
        project = f"projects/{project_id}"
        billing = f"billingAccounts/{billing_id}"
        data = {"billingAccountName": billing}
        response = self.session.put(
            url=f"{project}/billingInfo", data=json.dumps(data)
        )
        return response.status_code, response.json()

    # def set_billing_account_client(self, project_id, billing_id):
    #     request = billing_v1.UpdateProjectBillingInfoRequest(
    #         name=project_id, project_billing_info=billing_id
    #     )
    #     try:
    #         return self.client.update_billing_account(request=request)
    #     except Exception as e:
    #         raise CustomBillingClientException(e.message, e.code)
