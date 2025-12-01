import csv
from pathlib import Path

from sqlalchemy import func, select
from app import app
from db import db




def drop_tables():
    with app.app_context():
        print("Dropping existing tables...")
        db.drop_all()

def create_tables():
    with app.app_context():
        print("Creating database tables...")
        db.create_all()

def import_products():
    with app.app_context():
        print("Importing products...")
        csv_path = Path(__file__).parent / "customers.csv"
        print(f"\nLoading data from {csv_path}...")
