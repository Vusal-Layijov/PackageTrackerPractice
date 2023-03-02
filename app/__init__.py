from flask import Flask, render_template, redirect
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
    packages= Package.query.filter(Package.sender.like("v%")).first()
    return render_template('package_status.html', packages=packages)


@app.route("/new_package", methods=["GET", "POST"])
def new_package():
    form = ShippingForm()
    if form.validate_on_submit():
        # Finish adding form data into db
        # e.g., form.origin.data
        print(dir(form))
        print(form.data)
        package= Package(
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
