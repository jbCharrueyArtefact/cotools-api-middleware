import os
import dotenv

ENV = os.environ.get("ENV", "DEV")

if ENV == "PRD":
    dotenv.load_dotenv("./app/env/.prod")
else:
    dotenv.load_dotenv("./app/env/.dev")

VAULT = os.environ.get("VAULT_URL")
PROJET = f"ofr-fgt-backend-cotools-{ENV.lower()}"

GROUP_CREATION_CLIENT_ID = (
    "498329607286-7mq34redtdhq8niqr3f6mq2i58eshus6.apps.googleusercontent.com"
)
URL_GROUP_CREATION = "https://ofr-0tm-iam-secu-1-prd.ey.r.appspot.com"
HIERARCHY_URL = "https://gitlab.si.francetelecom.fr/api/v4/projects/24016/jobs/artifacts/master/raw/output.json?job=google-cloud-platform:list-folders:onmaster"
REFERENCE_TABLE_IAM_HISTORY = (
    f"{PROJET}.fgt_backend_cotools_iam_{ENV.lower()}.view_iam"
)
ESSENTIAL_CONTACTS_CURRENT_TABLE = f"{PROJET}.fgt_backend_cotools_audit_{ENV.lower()}.raw_fact_auditessentialcontactcurrent_t"
ESSENTIAL_CONTACTS_CURRENT_VIEW = f"{PROJET}.fgt_backend_cotools_audit_{ENV.lower()}.view_essentialcontact_current"


SA_VAULT_PATH = f"ofr-fgt-backend-cotools/data/gcp/{ENV.lower()}/service-account/applicative_deployment/"
SA_VAULT_URL = "https://area51-sophia.hbx.geo.francetelecom.fr/"
SA_VAULT_NAMESPACE = "DLiCe"

SA_NAMES = {
    "bq": "sa-ofr-fgt-bigquery",
    "create_project": "sa-ofr-fgt-create-project",
    "iam": "sa-ofr-fgt-iam",
    "essential_contacts": "sa-ofr-fgt-essential-contacts",
}


SECRETS = {
    "biqquery": "bigquery_cotools_dev",
    "essential_contacts": "essential_contacts",
    "create_project": "create_project",
}
