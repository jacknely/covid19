from flask import Flask
from app.models import JyMongo
from flask_restful import Api
from flask_restful_swagger import swagger


db = JyMongo()
api = swagger.docs(Api(), apiVersion='1', api_spec_url='/api/spec')


def create_app():
    app = Flask(__name__)

    app.config.from_object('config.DevConfig')
    api.init_app(app)
    db.init_app(app)

    return app