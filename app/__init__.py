from flask import Flask
from flask_jwt_extended import JWTManager
from flasgger import Swagger
import yaml

from app.config.config import Config
from app.database.db import mongo

from app.routes.auth_routes import auth_bp
from app.routes.analysis_routes import analysis_bp
from app.routes.user_routes import user_bp


jwt = JWTManager()


def create_app():

    app = Flask(__name__)

    # Config
    app.config.from_object(Config)

    # MongoDB
    mongo.init_app(app)

    # JWT
    jwt.init_app(app)


    # Swagger
    with open("app/docs/swagger.yml", "r", encoding="utf-8") as file:
        swagger_template = yaml.safe_load(file)

    Swagger(app, template=swagger_template)

    app.register_blueprint(auth_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(user_bp)

    # Rota principal
    @app.route("/")
    def home():
        return {
            "message": "API Dengue AI Online"
        }

    return app