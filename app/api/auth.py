#!/usr/bin/python3.6
#-*-coding:utf-8-*-
from flask import g
from flask_httpauth import HTTPBasicAuth
from app.models import User
from app.api.errors import error_response

token_auth = HTTPBasicAuth()

@token_auth.verify_password
def verify_token(username, password):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return False
    g.current_user = user
    return user.check_password(password)

@token_auth.error_handler
def token_auth_error():
    return error_response(401)
