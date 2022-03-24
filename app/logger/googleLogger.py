import json
import logging
from google.cloud.logging_v2 import Client
from google.cloud.logging_v2.handlers import CloudLoggingHandler
from google.oauth2 import service_account
from app.lib.utils.secret import get_sa_info

from app.config import PROJET

credentials = service_account.Credentials.from_service_account_info(
    get_sa_info("logging")
)


class GCPFormatter(logging.Formatter):
    def format(self, record):

        invalid = ["status", "path", "method"]
        payload = {k: v for k, v in record.msg.items() if k not in invalid}

        httpsrequest = {}

        if record.msg.get("method", None) is not None:
            httpsrequest["requestMethod"] = record.msg["method"]

        if record.msg.get("path", None) is not None:
            httpsrequest["requestUrl"] = record.msg["path"]

        if record.msg.get("status", None) is not None:
            httpsrequest["status"] = record.msg["status"]

        log = {
            "jsonPayload": payload,
            "sourceLocation": {
                "file": record.module,
                "line": record.lineno,
                "function": record.funcName,
            },
            "operation": {"id": "cotools-middleware"},
        }

        if len(httpsrequest.keys()) > 0:
            log["httpRequest"] = httpsrequest

        return log


class GoogleLogger(CloudLoggingHandler):
    def __init__(self):
        client = Client(project=PROJET, credentials=credentials)
        client._use_grpc = False
        super(GoogleLogger, self).__init__(client)

    def emit(self, record):

        message = super(CloudLoggingHandler, self).format(record)
        self.transport.send(
            record,
            message=message["jsonPayload"],
            # resource={"type":"co-tools-middleware"},
            labels=record._labels,
            trace=record._trace,
            span_id=record._span_id,
            http_request=message.get("httpRequest"),
            source_location=message["sourceLocation"],
            operation=message["operation"],
        )
