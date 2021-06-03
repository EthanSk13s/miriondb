import os
basedir = os.getcwd()


class Config(object):
    SCHEDULER_API_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'theater.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
