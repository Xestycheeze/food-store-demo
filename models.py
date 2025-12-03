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
    category_id = mapped_column(Integer, ForeignKey("categories.id"), nullable=False)
    category = relationship("Category", back_populates="products")

class Category(db.Model):
    __tablename__ = "categories"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    products = relationship("Product", back_populates="category")

class Customer(db.Model):
    __tablename__ = "customers"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(100))
    phone = mapped_column(String(14))
    orders = relationship("Order", back_populates="customer", cascade="all, delete-orphan")

    def list_incomplete_orders(self):
        return [order for order in self.orders if order.completed == None]

    def list_complete_orders(self):
        return [order for order in self.orders if order.completed != None]


class Order(db.Model):
    __tablename__ = "orders"

    id = mapped_column(Integer, primary_key=True)

    customer_id = mapped_column(Integer, ForeignKey("customers.id"), nullable=False)
    customer = relationship("Customer", back_populates="orders")

    items = relationship("ProductOrder", back_populates="order")

    created = mapped_column(DateTime, nullable=False, default=func.now())
    completed = mapped_column(DateTime, nullable=True, default=None)
    amount = mapped_column(DECIMAL(6, 2), nullable=True, default=None)

    def estimate(self):
        total = 0
        for po in self.items:
          one = po.product.price * po.quantity
          total = total + one
        return total

    def complete(self):
        for po in self.items:
            if po.quantity <= po.product.inventory:
                po.product.inventory = po.product.inventory - po.quantity
            else:
                raise ValueError("Insufficient inventory")
        self.completed = db.func.now()
        self.amount = self.estimate()

class ProductOrder(db.Model):
    __tablename__ = "product_orders"

    product_id = mapped_column(db.ForeignKey("product.id"), nullable=False, primary_key=True)
    product = relationship("Product")
    order_id = mapped_column(db.ForeignKey("orders.id"), nullable=False, primary_key=True)
    order = relationship("Order", back_populates="items")

    quantity = mapped_column(db.Integer, nullable=False)



