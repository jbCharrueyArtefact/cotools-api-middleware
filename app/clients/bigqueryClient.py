from google.cloud.bigquery.client import Client
from google.cloud.bigquery import SchemaField, LoadJobConfig
from datetime import datetime
from app.lib.utils.custom_error_handling import CustomBigQueryClientException
from app.config import DATA_GROUPS, GESTIONNAIRE_DATA


class BigQueryWrapper(Client):
    def __new__(cls, service_account_info: str):
        client = Client.from_service_account_info(info=service_account_info)
        client.__class__ = cls
        return client

    def __init__(self, service_account_info, *args, **kwargs):
        pass

    def insert_data(self, table_id=None, rows=None, schema=None):
        schema = [
            SchemaField("email", "STRING"),
            SchemaField("time", "DATETIME"),
            SchemaField("project", "STRING"),
            SchemaField("notificationCategory", "STRING"),
            SchemaField("status", "STRING"),
        ]
        table = self.get_table(table_id)
        job_config = LoadJobConfig()
        job_config.schema = schema
        job = self.load_table_from_json(
            json_rows=rows, destination=table, job_config=job_config
        )
        return job.result()

    # TODO - Verify the output of this function
    def insert_stream_data(self, table_id=None, rows=None):
        table = self.get_table(table_id)
        errors = self.insert_rows(table, rows)
        return errors

    def insert_group(
        self, name, description, entities, is_bank, project, admin
    ):
        name = DATA_GROUPS
        data = [
            {
                "group_name": name,
                "description": description,
                "email": admin,
                "entities": entities,
                "is_banking": is_bank,
                "project": project,
                "creation_date": datetime.now().isoformat(),
            }
        ]

        self.insert_stream_data(name, data)
        name = GESTIONNAIRE_DATA
        data = [{"group_name": name, "admin": admin}]

        self.insert_stream_data(name, data)

    def delete_data(self, table_id=None, condition="1=1"):
        job = self.query(f"DELETE FROM `{table_id}` Where {condition};")
        return job.result()

    def query_data(self, query):
        job = self.query(query)
        return job.result()
