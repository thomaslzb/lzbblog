#-*-coding:utf-8-*-
from flask import Blueprint

bp = Blueprint('error',__name__)

from app.error import handlers

