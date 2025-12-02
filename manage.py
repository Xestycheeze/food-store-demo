import csv, sys
from pathlib import Path
from random import randint
import math
from datetime import datetime, timedelta

from sqlalchemy import func

from app import app
from db import db
from models import Product, Category, Customer, Order, ProductOrder


def main(cmd):
    match cmd.lower():
        case "initialize":
            drop_tables()
            create_tables()
        case "nuke":
            drop_tables()
        case "import":
            import_data()
        case "order":
            orders = input("Enter the amount of orders: ")
            products = input("Enter the max amount of product types for each order: ")
            generate_order(orders, products)
        case _:
            print("Enter a valid command. (Initialize/Nuke/Import)")


def drop_tables():
    try:
        with app.app_context():
            print("Dropping existing tables...")
            db.drop_all()
            db.session.commit()
            print("Dropped existing tables...")
    except Exception as err:
        print(err)


def create_tables():
    try:
        with app.app_context():
            print("Creating database tables...")
            db.create_all()
            db.session.commit()
            print("Created database tables.")
    except Exception as err:
        print(err)


def import_data():
    with app.app_context():
        print("Importing products...")
        products_path = Path(__file__).parent / "products.csv"
        with open(products_path, 'r') as products_file:
            print(f"\nLoading data from {products_path}...")
            for raw_product in csv.DictReader(products_file, delimiter=','):
                stmt =db.select(Category).where(Category.name == raw_product.get('category'))
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

def generate_order(orders, products):
    with app.app_context():
        for i in range(int(orders)):
            rand_time = datetime.now() - timedelta(days=randint(0, 14), hours=randint(0, 23), minutes=randint(1, 59))
            random_customer = db.session.execute(db.select(Customer).order_by(func.random())).scalar()
            new_order = Order(customer=random_customer, created=rand_time)
            db.session.add(new_order)

            num_prods = randint(1, int(products))
            random_prods = db.session.execute(db.select(Product).order_by(func.random()).limit(num_prods)).scalars()
            for random_prod in random_prods:
                random_request_prod_quantity = randint(1, 1 + math.floor(random_prod.inventory*1.5))
                new_prod_order = ProductOrder(product=random_prod,
                                              order=new_order,
                                              quantity=random_request_prod_quantity)
                db.session.add(new_prod_order)
        db.session.commit()
        print(f"Generated {orders} orders!")





if __name__ == "__main__":
    main(sys.argv[1])
