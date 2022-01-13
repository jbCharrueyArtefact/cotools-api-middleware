import os
import dotenv

ENV = os.environ.get("ENV", "DEV")

if ENV == "PRD":
    dotenv.load_dotenv("./app/env/.prod")
else:
    dotenv.load_dotenv("./app/env/.dev")

VAULT = os.environ.get("VAULT_URL")
PROJET = os.environ.get("PROJECT")

GROUP_CREATION_CLIENT_ID = (
    "498329607286-7mq34redtdhq8niqr3f6mq2i58eshus6.apps.googleusercontent.com"
)
URL_GROUP_CREATION = "https://ofr-0tm-iam-secu-1-prd.ey.r.appspot.com"
HIERARCHY_URL = "https://gitlab.si.francetelecom.fr/api/v4/projects/24016/jobs/artifacts/master/raw/output.json?job=google-cloud-platform:list-folders:onmaster"
REFERENCE_TABLE_IAM_HISTORY = f"{PROJET}.view_iam_rights.history-setiam"
ESSENTIAL_CONTACTS_CURRENT_TABLE = f"{PROJET}.fgt_backend_cotools_audit_dev.raw_fact_auditessentialcontactcurrent_t"
ESSENTIAL_CONTACTS_CURRENT_VIEW = (
    f"{PROJET}.fgt_backend_cotools_audit_dev.view_essentialcontact_current"
)


SECRETS = {
    "biqquery": "bigquery_cotools_dev",
    "essential_contacts": "essential_contacts",
    "create_project": "create_project",
}
