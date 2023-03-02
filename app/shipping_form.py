from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired

from map.map import map
# tuple(map)
# ('Seattle', 'San Francisco', 'Los Angeles', 'Phoenix', 'Denver', 'Kansas City', 'Houston', 'Chicago', 'Nashville', 'New York', 'Washington D.C.', 'Miami')

class ShippingForm(FlaskForm):
    select_choices = []
    # print(map.items())
    # for tupl in map.items():
    #     select_choices.append(tupl)
    # print(select_choices)
    for each in tuple(map):
        select_choices.append(each)

    sender = StringField("Sender", validators=[DataRequired()])
    recipient = StringField("Recipient", validators=[DataRequired()])
    origin = SelectField("Origin", choices=select_choices, validators=[DataRequired()])
    destination = SelectField("Destination", choices=select_choices, validators=[DataRequired()])
    express = BooleanField("Express", validators=[DataRequired()])
    submit = SubmitField("Send")
    cancel = SubmitField("Cancel")