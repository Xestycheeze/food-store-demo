from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, DECIMAL, String, Table, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


from db import db

class Product(db.Model):
    __tablename__ = "product"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    price = mapped_column(DECIMAL(10, 2))
    inventory = mapped_column(Integer, default=0)
    category_id = mapped_column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="products")

class Category(db.Model):
    __tablename__ = "categories"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    products = relationship("Product", back_populates="category")




