import os
from typing import Optional

import boto3

from src.common.Product import Product

dynamodb_client = boto3.client("dynamodb")
PRODUCTS_TABLE = os.environ["PRODUCTS_TABLE"]


def get_product(product_id) -> Optional[Product]:
    items = dynamodb_client.get_item(TableName=PRODUCTS_TABLE, Key={'productId': {'S': product_id}})
    product = items.get('Item')
    if not product:
        print("Could not find ikea in DB")
    else:
        result = Product(product_id,
                         int(product.get('major_version').get('N')),
                         int(product.get('minor_version').get('N')),
                         int(product.get('hotfix_version').get('N')),
                         "")
        return result


def create_product(product_id="ikea", major_version="1", minor_version="16", hotfix_version="25"):
    dynamodb_client.put_item(
        TableName=PRODUCTS_TABLE,
        Item={'productId': {'S': product_id},
              'major_version': {'N': major_version},
              'minor_version': {'N': minor_version},
              'hotfix_version': {'N': hotfix_version}}
    )
