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
    effective_saving = db.Column(db.Integer)

    @classmethod
    def truncate(cls, session):
        stmt = db.text(f'TRUNCATE TABLE {cls.__tablename__} RESTART IDENTITY CASCADE;')
        session.execute(stmt)

    @classmethod
    def missing_airlines_query(cls):
        """
        Return a query that select airlines in the staging table that are
        missing from the airline table.
        """
        return (
            db.select(
                cls.airline.distinct().label('code')
            )
            .outerjoin(
                Airline,
                Airline.code == cls.airline
            )
            .where(Airline.code.is_(None))
        )

    @classmethod
    def insert_missing_airlines(cls, session):
        insert_missing_airlines = Airline.__table__.insert().from_select(
            ['code'],
            OpticlimbRecordStaging.missing_airlines_query(),
        )
        session.execute(insert_missing_airlines)

    @classmethod
    def missing_airports_query(cls, attrib):
        """
        Return a query selecting the airport codes from staging that are
        missing in the lookup table.
        :param attrib: Either "arrival" or "departure"
        """
        if attrib not in ('arrival', 'departure'):
            raise ValueError(
                f'attrib must be "arrival" or "departure" not {attrib}')
        attr = getattr(OpticlimbRecordStaging, attrib)
        query = (
            db.select(attr.label('code'))
            .outerjoin(Airport, Airport.code == attr)
            .where(Airport.code.is_(None))
        )
        return query

    @classmethod
    def insert_missing_airports(cls, session):
        for airport_attr in ['arrival', 'departure']:
            missing_airports = cls.missing_airports_query(airport_attr)
            insert_missing_airports = Airport.__table__.insert().from_select(
                ['code'],
                missing_airports
            )
            session.execute(insert_missing_airports)

    @classmethod
    def load_from_data(cls, data, trigram):
        """
        Load database with data from API. The data first goes into a staging table
        to be used to update the others on the database side.

        :param data: deserialized and typed data from API.
        :param trigram: three-letter airline code.
        """
        # clear staging table
        cls.truncate(db.session)

        staging_data = [cls(airline=trigram, **record) for record in data]

        db.session.bulk_save_objects(staging_data)
        db.session.flush()

        # Insert missing airlines
        cls.insert_missing_airlines(db.session)

        # Insert missing airports from arrival and departure.
        cls.insert_missing_airports(db.session)

        arrival_airport = db.alias(Airport, name='arrival')
        departure_airport = db.alias(Airport, name='departure')
        arrival_staging = db.alias(cls, name='arrival_stage')
        departure_staging = db.alias(cls, name='departure_stage')
        staging_record = db.alias(cls, name='staging_record')

        missing_records = (
            db.select(
                Airline.id.label('airline_id'),
                staging_record.c.adherence,
                staging_record.c.date,
                staging_record.c.flight_data_available,
                staging_record.c.flight_number,
                staging_record.c.potential_saving,
                staging_record.c.effective_saving,
                arrival_airport.c.id.label('arrival_airport_id'),
                departure_airport.c.id.label('departure_airport_id'),
            )
            .select_from(
                staging_record
            )
            .join(
                Airline,
                staging_record.c.airline == Airline.code,
            )
            .outerjoin(
                OpticlimbRecord,
                db.and_(
                    staging_record.c.airline == Airline.code,
                    staging_record.c.date == OpticlimbRecord.date,
                    staging_record.c.flight_number == OpticlimbRecord.flight_number,
                )
            )
            .join(
                arrival_airport,
                arrival_airport.c.code == staging_record.c.arrival,
            )
            .join(
                departure_airport,
                departure_airport.c.code == staging_record.c.departure,
            )
            .where(OpticlimbRecord.id.is_(None))
        )
        insert_missing_records = OpticlimbRecord.__table__.insert().from_select(
            [
                'airline_id',
                'adherence',
                'date',
                'flight_data_available',
                'flight_number',
                'potential_saving',
                'effective_saving',
                'arrival_airport_id',
                'departure_airport_id',
            ],
            missing_records
        )
        db.session.execute(insert_missing_records)


class OpticlimbRecord(db.Model):
    """
    An opticlimb record from the API.
    """

    __table_args__ = (
        db.Index(
            'airline_id', 'date', 'flight_number',
        ),
    )

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

    arrival_airport_id = db.Column(
        db.Integer,
        db.ForeignKey('airport.id'),
    )

    arrival_airport = db.relationship(
        'Airport',
        foreign_keys = [arrival_airport_id],
        back_populates = 'as_arrival',
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
            'description': 'The opticlimb recommendation was used.',
        },
    )

    potential_saving = db.Column(
        db.Integer,
        info = {
            'label': 'Potential Saving',
        },
    )

    effective_saving = db.Column(
        db.Integer,
        info = {
            'label': 'Effective Saving',
        },
    )
