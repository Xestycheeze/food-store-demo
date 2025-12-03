from flask import Flask, render_template, redirect, url_for
from pathlib import Path
from db import db
from models import Product, Category, Customer, Order, ProductOrder

app = Flask(__name__)
# This will make Flask use a 'sqlite' database with the filename provided
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mara3uHe.db"
# This will make Flask store the database file in the path provided
app.instance_path = Path(".").resolve()
# Adjust to your needs / liking. Most likely, you want to use "." for your instance path. This is up to you. You may also use "data".

db.init_app(app)
@app.route("/")
def home():
    return render_template("home.html", name="lmaoo")


@app.route("/products")
def products():
    stmt = db.select(Product)
    produktih = db.session.execute(stmt).scalars().all()
    return render_template("products.html", products=produktih)

@app.route("/categories")
def categories():
    stmt = db.select(Category)
    kategorii = db.session.execute(stmt).scalars().all()
    return render_template("categories.html", categories=kategorii)

@app.route("/categories/<string:name>")
def category_detail(name):
    stmt = db.select(Product).where(Product.category.has(Category.name == name))
    # Find the category with name 'name'
    produktih = db.session.execute(stmt).scalars().all()
    # cat.products # contains all the products in that category (use back_populates)
    return render_template("products.html", products=produktih)

@app.route("/customers")
def customers():
    stmt = db.select(Customer)
    klientih = db.session.execute(stmt).scalars().all()
    return render_template("customers.html", customers=klientih)

@app.route("/customers/<int:id>")
def customer_detail(id):
    stmt = db.select(Customer).where(Customer.id == id)
    customer = db.session.execute(stmt).scalar()
    return render_template("customers.html", selected_customer=customer)

@app.route("/orders")
def orders():
    completed_rows = db.select(Order).where(Order.completed != None) # using `is` keyword doesnt work?
    completed_orders = db.session.execute(completed_rows).scalars()
    incomplete_rows = db.select(Order).where(Order.completed == None)
    incomplete_orders = db.session.execute(incomplete_rows).scalars()
    return render_template("orders.html",
                           completed_orders=completed_orders,
                           incomplete_orders=incomplete_orders)

@app.route("/orders/<int:id>")
def order_detail(id):
    stmt = db.select(Order).where(Order.id == id)
    zakaz = db.session.execute(stmt).scalar()
    return render_template("orders.html", selected_order=zakaz)

@app.route("/orders/<int:id>/complete", methods=["POST"])
def complete_order(id):
    try:
        order = db.get_or_404(Order, id)
        order.complete()
        db.session.add(order)
        db.session.commit()
        return redirect(url_for("orders"))
    except ValueError as e:
        return render_template("error.html", message=f"{e}"), 400




if __name__ == "__main__":
    app.run(debug=True, port=8888)
