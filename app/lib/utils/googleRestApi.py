from requests import Session
from urllib.parse import urljoin
from google.oauth2 import service_account
from google.auth.transport.requests import Request


def httpErrorHandler(func):
    def wrapper(*args, **kwargs):
        status_code, return_value = func(*args, **kwargs)
        print(return_value)
        if status_code == 200:
            return return_value
        else:
            raise Exception()

    return wrapper


class GoogleRestApi:
    def __init__(self, sa_info, api):

        self.session = _ApiSession(sa_info, api)


class _ApiSession(Session):
    def __init__(self, sa, prefix_url=None, *args, **kwargs):
        super(_ApiSession, self).__init__(*args, **kwargs)
        self.prefix_url = prefix_url

        cred = service_account.Credentials.from_service_account_info(
            sa,
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )
        cred.refresh(Request())
        self.headers.update(
            {
                "Authorization": f"Bearer {cred.token}",
                "Content-Type": "application/json; charset=utf-8",
            }
        )

    def request(self, method, url, *args, **kwargs):
        url = urljoin(self.prefix_url, url)
        return super(_ApiSession, self).request(method, url, *args, **kwargs)
