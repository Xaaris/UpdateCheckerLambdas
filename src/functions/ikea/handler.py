from typing import Optional

import requests

from src.common.Product import Product
from src.common.ProductRepository import get_product, update_product
from src.functions.mail.mail import send_update_info_mail


def go(event, context):
    local = get_product("ikea")

    remote = get_remote_ikea_version()

    if is_remote_version_higher(local, remote):
        print(f"Update available for {local.id} from {local.get_full_version()} to {remote.get_full_version()}")
        send_update_info_mail("xaaris+updatecheckertest@googlemail.com", remote.name, local.get_full_version(),
                              remote.get_full_version(), remote.release_notes_link)
        update_product(remote)
    else:
        print(f"Your local version for {local.name} of {local.get_full_version()} is up to date")

    response = {"statusCode": 200}
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
                             "IKEA Tradfri Gateway",
                             remote_major_version,
                             remote_minor_version,
                             remote_hotfix_version,
                             release_notes_link)
            return result


if __name__ == "__main__":
    print(go(None, None))
