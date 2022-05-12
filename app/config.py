import os
from typing import Literal
import dotenv

ENV: Literal["ENV", "PPR", "PRD"] = os.environ.get("ENV", "DEV")

if ENV == "PRD":
    dotenv.load_dotenv("./app/env/.prod")
else:
    dotenv.load_dotenv("./app/env/.dev")

VAULT = os.environ.get("VAULT_URL")
VAULT_PATH = f"co-tools-secrets/data/{ENV.lower()}"

PROJET = f"ofr-fgt-backend-cotools-{ENV.lower()}"
PROJECT_SHARED_DATA_API = f"ofr-fgt-shared-data-{ENV.lower()}"

# ajouté
AUTH_METHOD = os.getenv("AUTH_METHOD", "vault")
SA_VAULT_DLICE_PATH = f"ofr-fgt-shared-data/data/gcp/{ENV.lower()}/service-account/applicative_deployment"
DOMAIN = "orange.com"
# PROJECT_NAME = f"ofr-fgt-shared-data-{ENV}"

GROUP_CREATION_CLIENT_ID = (
    "498329607286-7mq34redtdhq8niqr3f6mq2i58eshus6.apps.googleusercontent.com"
)
URL_GROUP_CREATION = (
    "https://manage-group-dot-ofr-0tm-iam-secu-1-prd.ey.r.appspot.com/"
)
HIERARCHY_URL = "https://gitlab.si.francetelecom.fr/api/v4/projects/24016/jobs/artifacts/master/raw/output.json?job=google-cloud-platform:list-folders:onmaster"
REFERENCE_TABLE_IAM_HISTORY = (
    f"{PROJET}.fgt_backend_cotools_iam_{ENV.lower()}.view_iam"
)
ESSENTIAL_CONTACTS_CURRENT_TABLE = f"{PROJET}.fgt_backend_cotools_audit_{ENV.lower()}.raw_fact_auditessentialcontactfromui_t"
ESSENTIAL_CONTACTS_CURRENT_VIEW = f"{PROJET}.fgt_backend_cotools_audit_{ENV.lower()}.view_essentialcontact_current"
URL_IOSW = os.environ.get("IOSW_URL")
SA_VAULT_PATH = f"ofr-fgt-backend-cotools/data/gcp/{ENV.lower()}/service-account/applicative_deployment/"
SA_VAULT_URL = "https://area51-sophia.hbx.geo.francetelecom.fr/"
SA_VAULT_NAMESPACE = "DLiCe"

BILLING_ID = "0136C4-D63C36-ED132B"

SA_NAMES = {
    "bq": "sa-ofr-fgt-bigquery",
    "create_project": "sa-ofr-fgt-create-project",
    "iam": "sa-ofr-fgt-iam",
    "essential_contacts": "sa-ofr-fgt-essential-contacts",
    "logging": "sa-ofr-fgt-logging-app",
    "billing": "sa-ofr-fgt-billing-account",
    "google_groups_assets": "sa-ofr-fgt-assetggroups-viewer",
    "group_creation": "sa-ofr-group-creation",
    "bq_shared_data": "sa-ofr-fgt-shared-data-bq-editor",
    "fire": "sa-ofr-fgt-firestore",
}

DATA_GROUPS = (
    f"{PROJECT_SHARED_DATA_API}.fgt_data_groups_info_dev.raw_fact_datagroups"
)

GESTIONNAIRE_DATA = f"{PROJECT_SHARED_DATA_API}.fgt_data_groups_info_dev.raw_fact_gestionnairedata"

ENTITIES = f"{PROJECT_SHARED_DATA_API}.fgt_data_groups_info_dev.raw_fact_restrictionentities"

SECRET = ["iosw"]
