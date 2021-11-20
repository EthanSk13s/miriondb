import os
import yaml

basedir = os.getcwd()


class Config(object):
    try:
        print("Trying to load from yaml...")
        f = open("db.yml", "r")
        yml = yaml.safe_load(f)
        print("Found config.")

        cfg = yml['postgres']
        url = f"postgresql://{cfg['user']}:{cfg['pass']}@localhost/{cfg['database']}"

        host = yml['assets']['host']
        port = yml['assets']['port']
    except FileNotFoundError:
        print("Config yaml not found, resorting to env vars.")
        url = os.environ.get('DATABASE_URL')

        host = os.environ.get('ASSETS_HOST')
        port = os.environ.get('ASSETS_PORT')

    SCHEDULER_API_ENABLED = True
    SQLALCHEMY_DATABASE_URI = url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ASSETS_HOST = host
    ASSETS_PORT = port
