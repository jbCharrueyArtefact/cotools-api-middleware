from google.cloud.bigquery.client import Client
from google.oauth2 import service_account


class BigQueryWrapper(Client):
    def __new__(cls, service_account_info: str):
        client = Client.from_service_account_info(info=service_account_info)
        client.__class__ = cls
        return client

    def __init__(self, *args, **kwargs):
        pass

    def insert_data(self, table_id=None, rows=None):
        table = self.get_table(table_id)
        errors = self.insert_rows(table, rows)
        return errors

    def delete_data(self, table_id=None, condition="1=1"):
        job = self.query(f"DELETE FROM `{table_id}` Where {condition};")
        return job.result()

    def query_data(self, query):
        job = self.query(query)
        return job.result()
