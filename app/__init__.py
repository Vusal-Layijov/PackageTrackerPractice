from flask import Flask, render_template, redirect
from app.config import Config
from .shipping_form import ShippingForm
from flask_migrate import Migrate
from .models import db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

@app.route("/")
def home():
    return "Package Tracker"


@app.route("/new_package", methods=["GET", "POST"])
def new_package():
    form = ShippingForm()
    if form.validate_on_submit():
        # Finish adding form data into db
        # e.g., form.origin.data
        return redirect("/")
    return render_template("shipping_request.html", form=form)
