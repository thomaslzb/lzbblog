#!/usr/bin/python3.6
#-*-coding:utf-8-*-
from flask import jsonify, g
from app import db
from app.api import bp
from app.api.auth import token_auth

@bp.route('/tokens', methods=['POST'])
@token_auth.login_required
def get_token():
    token = g.current_user.get_token()
    db.session.commit()
    return jsonify({'token': token})

@bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    g.current_user.revoke_token()
    db.session.commit()
    return '', 204