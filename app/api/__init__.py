#!/usr/bin/python3.6
#-*-coding:utf-8-*-

from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import users, errors, tokens
