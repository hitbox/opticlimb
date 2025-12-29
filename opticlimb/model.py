from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class OpticlimbRecord(db.Model):
    """
    An opticlimb record from the API.
    """

    id = db.Column(db.Integer, primary_key=True)

    airline = db.Column(
        db.String,
        index = True,
        info = {
            'label': 'Airline',
        },
    )

    flight_number = db.Column(
        db.String,
        index = True,
        info = {
            'label': 'Flight Number',
        },
    )

    date = db.Column(
        db.Date(),
        info = {
            'label': 'Date',
        },
    )

    departure = db.Column(
        db.String(),
        info = {
            'label': 'Depature',
        },
    )

    arrival = db.Column(
        db.String(),
        info = {
            'label': 'Arrival',
        },
    )

    flight_data_available = db.Column(
        db.Boolean,
        info = {
            'label': 'Flight Data Available?',
        },
    )

    adherence = db.Column(
        db.Boolean,
        info = {
            'label': 'Adherence?',
        },
    )

    effective_saving = db.Column(
        db.Integer,
        info = {
            'label': 'Effective Saving',
        },
    )
