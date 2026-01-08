import argparse

import requests

from .model import Airline
from .model import Airport
from .model import OpticlimbRecord
from .model import OpticlimbRecordStaging
from .model import db
from .schema import OpticlimbSchema

production_authentication_url = 'https://www.opti-climb.fr/{trigram}/ws/login/basic'

dashboard_url = 'https://www.opti-climb.fr/{trigram}/ws/connector/dashboard/list'

def get_production_authentication_url(trigram):
    return production_authentication_url.format(trigram=trigram)

def get_dashboard_url(trigram):
    return dashboard_url.format(trigram=trigram)

def load_data(data, trigram):
    OpticlimbRecordStaging.load_from_data(data, trigram)
    db.session.commit()

