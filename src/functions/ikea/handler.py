import os

import boto3
import requests

dynamodb_client = boto3.client("dynamodb")
PRODUCTS_TABLE = os.environ["PRODUCTS_TABLE"]


def go(event, context):
    local_ikea_values = get_product("ikea")

    local_major_version = int(local_ikea_values["major_version"])
    local_minor_version = int(local_ikea_values["minor_version"])
    local_hotfix_version = int(local_ikea_values["hotfix_version"])

    remote_ikea_values = get_remote_ikea_version()

    remote_major_version = int(remote_ikea_values["major_version"])
    remote_minor_version = int(remote_ikea_values["minor_version"])
    remote_hotfix_version = int(remote_ikea_values["hotfix_version"])
    release_notes_link = remote_ikea_values["release_notes_link"]

    if (remote_major_version > local_major_version
            or remote_minor_version > local_minor_version
            or remote_hotfix_version > local_hotfix_version):
        print(
            f"There is an update from {local_major_version}.{local_minor_version}.{local_hotfix_version} to {remote_major_version}.{remote_minor_version}.{remote_hotfix_version} available! "
            f"You can find the release notes here: {release_notes_link}"
        )
    else:
        print(f"Your local version of {local_major_version}.{local_minor_version}.{local_hotfix_version} is up to date")


# response_body = {
#             "message": "The current latest Ikea tradfri GW is " + remote_version_complete,
#             "releaseNotes": release_notes_link,
#             "input": event,
#         }
#
#         response = {
#             "statusCode": 200,
#             "body": json.dumps(response_body)
#         }
#
# return response


def get_remote_ikea_version():
    ikea_response = requests.get("http://fw.ota.homesmart.ikea.net/feed/version_info.json").json()
    for info in ikea_response:
        if info["fw_type"] == 0:
            remote_major_version = info["fw_major_version"]
            remote_minor_version = info["fw_minor_version"]
            remote_hotfix_version = info["fw_hotfix_version"]
            release_notes_link = info["fw_weblink_relnote"]

            result = {
                "major_version": remote_major_version,
                "minor_version": remote_minor_version,
                "hotfix_version": remote_hotfix_version,
                "release_notes_link": release_notes_link,
            }
            return result


def get_product(product_id):
    result = dynamodb_client.get_item(TableName=PRODUCTS_TABLE, Key={'productId': {'S': product_id}})
    product = result.get('Item')
    if not product:
        print("Could not find ikea in DB")
    else:
        result = {
            "product_id": product.get('productId').get('S'),
            "major_version": product.get('major_version').get('S'),
            "minor_version": product.get('minor_version').get('S'),
            "hotfix_version": product.get('hotfix_version').get('S'),
        }
        return result


def create_product():
    product_id = "ikea"
    major_version = "1"
    minor_version = "16"
    hotfix_version = "25"

    dynamodb_client.put_item(
        TableName=PRODUCTS_TABLE,
        Item={'productId': {'S': product_id},
              'major_version': {'S': major_version},
              'minor_version': {'S': minor_version},
              'hotfix_version': {'S': hotfix_version}}
    )


if __name__ == "__main__":
    print(go(None, None))
