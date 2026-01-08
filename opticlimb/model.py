from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Airline(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    code = db.Column(
        db.String,
    )

    records = db.relationship(
        'OpticlimbRecord',
        back_populates = 'airline_object',
    )


class Airport(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    code = db.Column(
        db.String,
    )

    as_departure = db.relationship(
        'OpticlimbRecord',
        foreign_keys = '[OpticlimbRecord.departure_airport_id]',
    )

    as_arrival = db.relationship(
        'OpticlimbRecord',
        foreign_keys = '[OpticlimbRecord.arrival_airport_id]',
    )


class OpticlimbRecordStaging(db.Model):
    """
    Data loaded from external source.
    """

    id = db.Column(db.Integer, primary_key=True)
    airline = db.Column(db.String)
    flight_number = db.Column(db.String)
    date = db.Column(db.Date)
    departure = db.Column(db.String)
    arrival = db.Column(db.String)
    flight_data_available = db.Column(db.Boolean)
    adherence = db.Column(db.Boolean)
    potential_saving = db.Column(db.Integer)


class OpticlimbRecord(db.Model):
    """
    An opticlimb record from the API.
    """

    id = db.Column(db.Integer, primary_key=True)

    airline_id = db.Column(
        db.Integer,
        db.ForeignKey('airline.id'),
    )

    airline_object = db.relationship(
        'Airline',
        back_populates = 'records',
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

    departure_airport_id = db.Column(
        db.Integer,
        db.ForeignKey('airport.id'),
    )

    departure_airport = db.relationship(
        'Airport',
        foreign_keys = [departure_airport_id],
        back_populates = 'as_departure',
    )

    arrival_airport_id = db.Column(
        db.Integer,
        db.ForeignKey('airport.id'),
    )

    arrival_airport = db.relationship(
        'Airport',
        foreign_keys = [arrival_airport_id],
        back_populates = 'as_arrival',
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
