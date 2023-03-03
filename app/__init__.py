from flask import Flask, render_template, redirect, request
from app.config import Config
from .shipping_form import ShippingForm
from flask_migrate import Migrate
from .models import db, Package

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def home():

    all_packages = Package.query.all()
    single_package = Package.query.filter(Package.sender == "vusal").first()
    return render_template('package_status.html', packages=all_packages)


@app.route("/new_package", methods=["GET", "POST"])
def new_package():
    form = ShippingForm()
    if form.validate_on_submit():
        # if form.cancel.data:
        #     return redirect("/")
        # Finish adding form data into db
        # e.g., form.origin.data
        # print(dir(form))
        # print(form.data)
        package = Package(
            sender=form.data['sender'],
            recipient=form.data['recipient'],
            origin=form.data['origin'],
            destination=form.data['destination'],
            location=form.data['origin']
        )

        db.session.add(package)
        db.session.commit()
        Package.advance_all_locations()
        return redirect("/")
    return render_template("shipping_request.html", form=form)


# UPDATE PACKAGE
@app.route("/update_package/<int:id>", methods=["GET", "POST"])
def update_package(id):
    form = ShippingForm()
    package = Package.query.get(id)
    # print("SENDER INFO: ", package.sender)
    # print(form)
    if form.validate_on_submit():
        # NEED TO WORK ON AUTO POPULATE OLD DATA INTO INPUT FIELDS
        package.sender = form.data['sender']
        package.recipient = form.data['recipient']
        package.origin = form.data['origin']
        package.destination = form.data['destination']
        package.express = form.data['express']
        # for key, value in request.form:
        #     setattr(package, key, value)
        db.session.commit()
        return redirect("/")
    return render_template("package_update.html", form=form, package=package)


# DELETE PACKAGE
@app.route("/delete_package/<int:id>", methods=["POST"])
def delete_package(id):
    package = Package.query.get(id)
    db.session.delete(package)
    db.session.commit()
    return redirect("/")
