from flask import Flask, render_template
from pathlib import Path
from db import db

app = Flask(__name__)
# This will make Flask use a 'sqlite' database with the filename provided
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///i_copy_pasted_this.db"
# This will make Flask store the database file in the path provided
app.instance_path = Path(".").resolve()
# Adjust to your needs / liking. Most likely, you want to use "." for your instance path. This is up to you. You may also use "data".

db.init_app(app)
@app.route("/")
def home():
    return render_template("../start/base.html", name="lmaoo")




if __name__ == "__main__":
    app.run(debug=True, port=8888)
