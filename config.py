import os
import yaml

basedir = os.getcwd()

try:
    with open("db.yml", "r") as f:
        cfg = yaml.safe_load(f)['postgres']
        url = f"postgresql://{cfg['user']}:{cfg['pass']}@localhost/{cfg['database']}"
except FileNotFoundError:
    print("Config yaml not found, resorting to env vars.")
    url = os.environ.get('DATABASE_URL')


class Config(object):
    SCHEDULER_API_ENABLED = True
    SQLALCHEMY_DATABASE_URI = url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
