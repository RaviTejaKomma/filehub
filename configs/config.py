import json
import os

FLASK_ENV = os.environ.get('FLASK_ENV')


def get_config():
    if FLASK_ENV == 'production':
        config = json.load(open(os.path.join(os.getcwd(), "configs/prod.json")))
    else:
        config = json.load(open(os.path.join(os.getcwd(), "configs/dev.json")))
    return config
