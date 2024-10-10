from flask import Flask, request, jsonify
from resources.product import blp as ProductBlueprint
from resources.warehouse import blp as WarehouseBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from blocklist import BLOCKLIST

from db import db
from flask_migrate import Migrate
from dotenv import  load_dotenv
import os

from models.products_tags import ProductsTags
from models.product import ProductModel
from models.warehouse import WarehouseModel
from models.tag import TagModel
from models.user import UserModel

#Load .env
load_dotenv()

# Create a web server using flask
app = Flask(__name__)

# Enable cors
CORS(app)

#Blueprint setup and documentation
app.config["PROPAGATE_EXCEPTIONS"] = True

#Title
app.config["API_TITLE"] = "Warehouses Rest API"
app.config["API_VERSION"] = "v1"

#OpenAPI  setup
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"

#Documentation Website Setup
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/"
app.config["OPENAPI_SWAGGER_UI_URL"] =  "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

#dDatabase
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")


#Connect to database
db.init_app(app)
migrate = Migrate(app, db)


#Register
api = Api(app)
api.register_blueprint(ProductBlueprint)
api.register_blueprint(WarehouseBlueprint)
api.register_blueprint(TagBlueprint)
api.register_blueprint(UserBlueprint)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {"description": "The token has been revoked.", "error":"token_revoked"}, 401
        )
    )


# Run the flask web app
# if __name__ == '__main__':
#     app.run(debug=True)