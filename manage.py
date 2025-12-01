import csv
from pathlib import Path

from app import app
from db import db
from models import Product, Category, Customer

def drop_tables():
    with app.app_context():
        print("Dropping existing tables...")
        db.drop_all()
        db.session.commit()

def create_tables():
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        db.session.commit()

def import_products():
    with app.app_context():
        print("Importing products...")
        products_path = Path(__file__).parent / "products.csv"
        with open(products_path, 'r') as products_file:
            print(f"\nLoading data from {products_path}...")
            for raw_product in csv.DictReader(products_file, delimiter=','):
                stmt =db.select(Category).wher(Category.name == raw_product.get('category'))
                possible_category_obj = db.session.execute(stmt).scalar()
                if possible_category_obj:
                    category_obj = possible_category_obj
                else:
                    category_obj = Category(name=raw_product.get('category'))
                    db.session.add(category_obj)
                product = Product(name=raw_product.get('name'),
                                  price=raw_product.get('price'),
                                  inventory=raw_product.get('available'),
                                  category=category_obj) # relationship() is smart enough to populate the category_id automatically
                db.session.add(product)
            db.session.commit()
            print(f"Product & Category session committed!")

        customers_path = Path(__file__).parent / "customers.csv"
        with open(customers_path, 'r') as customers_file:
            print(f"\nLoading data from {customers_path}...")
            for raw_customer in csv.DictReader(customers_file, delimiter=','):
                customer = Customer(name=raw_customer.get('name'),phone=raw_customer.get('phone'))
                db.session.add(customer)
            db.session.commit()
            print(f"Customer session committed!")



