from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, create_refresh_token


import requests as r
from db import db
from blocklist import BLOCKLIST
from models.user import UserModel
from schemas import UserSchema
from sqlalchemy.exc import SQLAlchemyError
import os
from dotenv import load_dotenv

import jinja2


load_dotenv()

template_loader = jinja2.FileSystemLoader("templates")
template_env = jinja2.Environment(loader=template_loader)

def render_template(template_filename, **context):
    return template_env.get_template(template_filename).render(**context)

def send_email(to, subject, body, html):
      
        mailgun_domain = os.getenv("MAILGUN_DOMAIN")
        mailgun_api_key = os.getenv("MAILGUN_API_KEY")

        welcome_email = r.post(
  		    f"https://api.mailgun.net/v3/{mailgun_domain}/messages",
  		    auth=("api", mailgun_api_key),
  		    data={"from": f"Admins <mailgun@{mailgun_domain}>",
  			      "to": to,
  			      "subject": subject,
  			      "text": body,
                  "html": html                  
              
            })
        
        print(welcome_email.json())

        return welcome_email
 


blp = Blueprint("users", __name__, description="Operations on users endpoint.")



@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jwt = get_jwt()
        jti = jwt["jti"]

        BLOCKLIST.add(jti)
        return {"message" : "Successfully logged out."}, 200

@blp.route("/login")
class Userlogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, req_body):
        user = UserModel.query.filter(
            UserModel.username == req_body["username"]
        ).first()

        if user:
            if pbkdf2_sha256.verify(req_body["password"], user.password): 
                if user.id == 1:

                    claim = {
                        'is_admin': True
                        }
                    access_token = create_access_token (identity=user.id, additional_claims=claim, fresh=True)
                    refresh_token = create_refresh_token(identity=user.id, additional_claims=claim)
                else:
                    access_token = create_access_token (identity=user.id, fresh=True)
                    refresh_token = create_refresh_token(identity=user.id)
                return {"access_token" : access_token, "refresh_token": refresh_token}  
            else:
                abort(400, message="Wrong password.")
        else:
            abort(400, message="User does not exist yet.")

@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        jwt = get_jwt()
        user_id =jwt["sub"]  

        if jwt.get("admin") == True:
            access_token = create_access_token (identity=user_id, additional_claims={"admin":True}, fresh=True)
            
        else:
            access_token = create_access_token (identity=user_id)

        return {"access_token": access_token}

        



    
@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_req_body):

        if UserModel.query.filter(UserModel.username == user_req_body["username"]).first():
            abort(409, message="A user with that username already exists.")

        user = UserModel(
            username=user_req_body["username"],
            email = user_req_body["email"],
            password=pbkdf2_sha256.hash(user_req_body["password"])
        )

        html = render_template("action.html", hello=user.username)
        
        # Send email for new user
        send_email(
            to = user.email,
            subject = "Successfully Signed Up!",
            body = f"Hi, {user.username}, You have successfully signed up to the Warehouses Rest API.",
            html= html


        )


        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured  while creating a new user.")

        return {"message" : "User registered successfully."}, 201
    
    @blp.route("/user/<int:user_id>")
    class User(MethodView):
        @blp.response(200, UserSchema)
        def get(self, user_id):
            user = UserModel.query.get_or_404(user_id)
            return user
        
        def delete(self, user_id):
            user = UserModel.query.get_or_404(user_id)
            db.session.delete(user)
            db.session.commit()

            return {"message": "User deleted"}, 200

    @blp.route("/my-info")
    class UserInfo(MethodView):
        @jwt_required()
        @blp.response(200, UserSchema)
        def get(self):
            user = UserModel.query.get_or_404(get_jwt()["sub"])
            return user

