from app.lib.utils.googleRestApi import GoogleRestApi, httpErrorHandler
import json


class BillingAccountClient(GoogleRestApi):
    def __init__(self, sa_info):
        super().__init__(sa_info, "https://cloudbilling.googleapis.com/v1/")

    @httpErrorHandler
    def set_billing_account(self, project_id, billing_id):
        project = f"projects/{project_id}"
        billing = f"billingAccounts/{billing_id}"
        data = {"billingAccountName": billing}
        response = self.session.put(
            url=f"{project}/billingInfo", data=json.dumps(data)
        )
        print(response.json())
        return response.status_code, response.json()
