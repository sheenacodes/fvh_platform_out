from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flasgger import Swagger
from flask_jwt_extended import JWTManager

app = Flask(__name__)

from app import config
app.config.from_object(config.Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
swagger = Swagger(app)
jwt = JWTManager(app)
from app import routes, models

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)

