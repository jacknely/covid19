import os


class Config(object):
    SECRET_KEY = "XXXXXXXTYUIO"


class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False


class DevConfig(Config):
    DEBUG = True
    MONGODB_HOST = os.environ.get('MONGODB_HOST')
    MONGO_URI = f"mongodb://{MONGODB_HOST}:27017/covid_db"
