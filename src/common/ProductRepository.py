import os
from typing import Optional

import boto3

from src.common.Product import Product

dynamodb_client = boto3.client("dynamodb")
PRODUCTS_TABLE = os.environ["PRODUCTS_TABLE"]


def get_product(product_id) -> Optional[Product]:
    items = dynamodb_client.get_item(TableName=PRODUCTS_TABLE, Key={"productId": {"S": product_id}})
    product = items.get("Item")
    if not product:
        print("Could not find ikea in DB")
    else:
        result = Product(product_id,
                         product.get("name").get("S"),
                         int(product.get("major_version").get("N")),
                         int(product.get("minor_version").get("N")),
                         int(product.get("hotfix_version").get("N")),
                         "")
        return result


def update_product(updated_product: Product):
    dynamodb_client.put_item(
        TableName=PRODUCTS_TABLE,
        Item={"productId": {"S": updated_product.id},
              "name": {"S": updated_product.name},
              "major_version": {"N": str(updated_product.major_version)},
              "minor_version": {"N": str(updated_product.minor_version)},
              "hotfix_version": {"N": str(updated_product.hotfix_version)}}
    )
