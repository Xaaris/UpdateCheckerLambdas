import json
from typing import Optional

import requests

from src.common.Product import Product
from src.common.ProductRepository import get_product


def go(event, context):
    local = get_product("ikea")

    remote = get_remote_ikea_version()

    if is_remote_version_higher(local, remote):
        msg = f"There is an update from {local.major_version}.{local.minor_version}.{local.hotfix_version} to {remote.major_version}.{remote.minor_version}.{remote.hotfix_version} available! " \
              f"You can find the release notes here: {remote.release_notes_link}"
    else:
        msg = f"Your local version of {local.major_version}.{local.minor_version}.{local.hotfix_version} is up to date"

    print(msg)
    response_body = {
        "message": msg,
        "input": event,
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(response_body)
    }
    return response


def is_remote_version_higher(local: Product, remote: Product) -> bool:
    return (remote.major_version > local.major_version
            or remote.minor_version > local.minor_version
            or remote.hotfix_version > local.hotfix_version)


def get_remote_ikea_version() -> Optional[Product]:
    ikea_response = requests.get("http://fw.ota.homesmart.ikea.net/feed/version_info.json").json()
    for info in ikea_response:
        if info["fw_type"] == 0:
            remote_major_version = int(info["fw_major_version"])
            remote_minor_version = int(info["fw_minor_version"])
            remote_hotfix_version = int(info["fw_hotfix_version"])
            release_notes_link = info["fw_weblink_relnote"]

            result = Product("ikea",
                             remote_major_version,
                             remote_minor_version,
                             remote_hotfix_version,
                             release_notes_link)
            return result


if __name__ == "__main__":
    print(go(None, None))
