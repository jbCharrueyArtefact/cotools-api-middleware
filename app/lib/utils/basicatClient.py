import requests
from functools import lru_cache


@lru_cache(maxsize=None)
def get_basicat_info(username, password, basicat):
    response = requests.get(
        url=f"http://ioswhp-ecm.itn.ftgroup:8008/FTC/SearchComponent-1?basicat={basicat}",
        auth=(username, password),
    )
    return response
