# from requests import session
import json
from typing import List
from contextlib import contextmanager


from app.lib.utils.googleRestApi import GoogleRestApi, error_handler_factory

from app.lib.utils.custom_error_handling import CustomFirestoreClientException


scopes = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/firebase.database",
    "https://www.googleapis.com/auth/datastore",
    "https://www.googleapis.com/auth/cloud-platform",
]


class FirestoreClient(GoogleRestApi):
    def __init__(self, sa_info, project, database):
        super().__init__(
            sa_info,
            f"https://firestore.googleapis.com/v1/projects/{project}/databases/{database}",
            scopes=scopes,
        )
        self.project = project
        self.database = database

    @error_handler_factory(CustomFirestoreClientException)
    def _list_document_aux(self, key, transaction_id=None, page_token=None):
        params = {
            "transaction": transaction_id,
            "page_token": page_token,
            "pageSize": 100,
        }
        resp = self.session.get(f"/documents/{key}", params=params)
        return resp.status_code, resp.json()

    def list_documents(self, key, transaction_id=None):
        documents = []
        page_token = None
        while True:
            result = self._list_document_aux(key, transaction_id, page_token)
            documents.extend(result["documents"])
            if not (page_token := result.get("nextPageToken")):
                break
        return documents

    @error_handler_factory(CustomFirestoreClientException)
    def _list_collections_aux(self, key=None, page_token=None):
        data = {"pageSize": 100, "pageToken": page_token}
        resp = self.session.post(
            f"/documents{'/'+key if key else '' }:listCollectionIds",
            data=json.dumps(data),
        )
        return resp.status_code, resp.json()

    def list_collections(self, key=None):
        page_token = None
        collections = []
        while True:
            result = self._list_collections_aux(key=key, page_token=page_token)
            collections.extend(result["collectionIds"])
            if not (page_token := result.get("nextPageToken")):
                break
        return collections

    @error_handler_factory(CustomFirestoreClientException)
    def read_data(self, collection, key, transaction_id=None):
        resp = self.session.get(
            url=f"/documents/{collection}/{key}",
            params={"transaction": transaction_id},
        )
        return resp.status_code, resp.json()

    # Example of payload: {'documents': ['projects/ofr-fgt-shared-data-dev/databases/(default)/documents/users/alovelace', 'projects/ofr-fgt-shared-data-dev/databases/(default)/documents/users/alovelace/test2/LhDYXes4ACBsZhsjOwnN']}
    @error_handler_factory(CustomFirestoreClientException)
    def read_batch_data(self, data, transaction_id=None):
        data["transaction"] = transaction_id
        resp = self.session.post(
            url="/documents:batchGet", data=json.dumps(data)
        )
        return resp.status_code, resp.json()

    # {"fields":{"born":{"integerValue":1000},"first":{"stringValue":"Victor"},"last":{"stringValue":"HUGO"}}}
    @error_handler_factory(CustomFirestoreClientException)
    def write_data(self, collection, key, data, update_mask=None):
        resp = self.session.patch(
            url=f"/documents/{collection}/{key}",
            params={"updateMask.fieldPaths": update_mask},
            data=json.dumps({"fields": data}),
        )
        return resp.status_code, resp.json()

    # Example of payload: {"writes":[{"update":{"name":"projects/ofr-fgt-shared-data-dev/databases/(default)/documents/users/alovelace","fields":{"first":{"stringValue":"toto"},"last":{"stringValue":"tata"},"born":{"integerValue":1910}}}}]}
    @error_handler_factory(CustomFirestoreClientException)
    def write_batch_data(self, writes: List = []):
        data = {"writes": writes}
        resp = self.session.post(
            url="/documents:batchWrite",
            data=json.dumps(data),
        )
        return resp.status_code, resp.json()

    # Example of query: {"structuredQuery": {"from": [{"collectionId": "users"}],"where": {"fieldFilter": {"field": {"fieldPath": "first"},"op": "EQUAL","value": {"stringValue": "carter"}}}}}
    @error_handler_factory(CustomFirestoreClientException)
    def query_data(self, query, transaction_id=None):
        query["transaction"] = transaction_id
        resp = self.session.post(
            url="/documents:runQuery", data=json.dumps(query)
        )
        return resp.status_code, resp.json()

    @error_handler_factory(CustomFirestoreClientException)
    def begin_transaction(self):
        resp = self.session.post(url="/documents:beginTransaction")
        return resp.status_code, resp.json()

    @error_handler_factory(CustomFirestoreClientException)
    def commit_transaction(self, transaction_id, writes: List = []):
        data = {"writes": writes, "transaction": transaction_id}
        resp = self.session.post(
            url="/documents:commit", data=json.dumps(data)
        )
        return resp.status_code, resp.json()

    @contextmanager
    def transaction(self):
        a = _Transaction(self)
        try:
            yield a
        except Exception as e:
            raise e
        finally:
            print("done")

    @contextmanager
    def batch_read(self, transaction_id=None):
        a = _BatchRead(self, transaction_id)
        try:
            yield a
        except Exception as e:
            raise e
        finally:
            print("done")

    @contextmanager
    def batch_write(self):
        a = _BatchWrite(self)
        try:
            yield a
        except Exception as e:
            raise e
        finally:
            print("done")


class _BatchWrite:
    def __init__(self, outer: FirestoreClient):
        self._outer = outer
        self.data = []

    def write_data(self, collection, key, data, update_mask=None):
        write = {
            # "updateMask":self.update_mask,
            "update": {
                "name": f"projects/{self._outer.project}/databases/{self._outer.database}/documents/{collection}/{key}",
                "fields": data,
            },
        }
        self.data.append(write)

    def execute(self):
        resp = self._outer.write_batch_data(self.data)
        return resp


class _BatchRead:
    def __init__(self, outer: FirestoreClient, transaction_id=None):
        self._outer = outer
        self.data = {"documents": []}
        self.transaction_id = transaction_id

    def read_data(self, collection, key):
        self.data["documents"].append(
            f"projects/{self._outer.project}/databases/{self._outer.database}/documents/{collection}/{key}"
        )

    def execute(self):
        resp = self._outer.read_batch_data(self.data, self.transaction_id)
        return resp


class _Transaction:
    def __init__(self, outer: FirestoreClient):
        self._outer = outer
        self.transaction_id = self._outer.begin_transaction()["transaction"]
        self.data = []

    def write_data(self, collection, key, data, update_mask=None):
        write = {
            # "updateMask":self.update_mask,
            "update": {
                "name": f"projects/{self._outer.project}/databases/{self._outer.database}/documents/{collection}/{key}",
                "fields": data,
            },
        }
        self.data.append(write)

    def query_data(self, query):
        return self._outer.query_data(query, self.transaction_id)

    def read_data(self, collection, key):
        return self._outer.read_data(collection, key, self.transaction_id)

    def list_documents(self, key):
        return self._outer.list_documents(key, self.transaction_id)

    def batch_read(self):
        return self._outer.batch_read(self.transaction_id)

    def execute(self):
        resp = self._outer.commit_transaction(
            self.transaction_id, writes=self.data
        )
        return resp
