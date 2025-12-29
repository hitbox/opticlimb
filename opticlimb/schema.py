from marshmallow import Schema
from marshmallow.fields import String
from marshmallow.fields import Integer
from marshmallow.fields import Date
from marshmallow.fields import Boolean

class OpticlimbSchema(Schema):

    flight_number = String(data_key='flightNumber')
    date = Date()
    departure = String()
    arrival = String()
    flight_data_available = Boolean(data_key='flightDataAvailable')
    adherence = Boolean()
    effective_saving = Integer(data_key='effectiveSaving')
