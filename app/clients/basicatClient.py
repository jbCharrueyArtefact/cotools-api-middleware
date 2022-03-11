import requests
from functools import lru_cache
from app.config import URL_IOSW


@lru_cache(maxsize=None)
def get_basicat_info(username, password, basicat):
    params = {"basicat": basicat}
    response = requests.get(
        url=URL_IOSW, auth=(username, password), params=params
    )
    return response
