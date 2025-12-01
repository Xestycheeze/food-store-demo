from db import Session
from models import Product

import csv

product = Product(name="eggs", price=12.34, inventory=100)
session = Session()
session.add(product)
session.commit()

with open("../products.csv", mode = 'r') as products_file:
    products_raw = csv.DictReader(products_file)
    for product_raw in products_raw:
        product = Product()