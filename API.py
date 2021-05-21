# -*- coding: utf-8 -*-
from functools import wraps
from flask import (make_response, jsonify, g, Blueprint)
from flask_restful import reqparse, abort, Api, Resource
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

from data import db_session
from data.users import User
from Rus.Logic import Logic

blueprint = Blueprint(
    'blueprint',
    __name__,
    template_folder='templates'
)

LOGIC = Logic()

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(header='token')


# Tokens: -----------------------------------------------------------
@blueprint.errorhandler(404)
def not_found(error=None):
    return make_response(jsonify({'error': 'Not found'}), 404)


@token_auth.error_handler
def token_auth_error():
    return make_response(jsonify({'error': 'Unauthorized token'}), 401)


@basic_auth.error_handler
def basic_auth_error():
    return make_response(jsonify({'error': 'Incorrect login or password'}), 401)


@basic_auth.verify_password
def verify_password(name, password):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.name == name).first()
    if user is None:
        return False
    g.current_user = user
    db_sess.close()
    return user.check_password(password)


@token_auth.verify_token
def verify_token(token):
    g.current_user = User.check_token(token) if token else None
    return g.current_user is not None


@blueprint.route('/api/get_token', methods=['GET'])
@basic_auth.login_required
def get_token():
    token = g.current_user.get_token()
    return jsonify({'token': token})


def admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if g.current_user.admin:
            return func(*args, **kwargs)
        return make_response(jsonify({'error': 'For admin only'}), 403)
    return wrapper


# -------------------------------------------------------------------

parser = reqparse.RequestParser()
parser.add_argument('text', required=True, type=str)
parser.add_argument('check_grammar', type=bool)


@blueprint.route('/api/syntactic_parsing', methods=['GET'])
@token_auth.login_required
def api_syntactic_parsing():
    args = parser.parse_args()
    ret = LOGIC.syntactic_pars(args['text'], args['check_grammar'])
    return jsonify({'result': ret})


@blueprint.route('/api/morph_pars', methods=['GET'])
@token_auth.login_required
def api_morph_pars():
    args = parser.parse_args()
    ret = LOGIC.morph_pars(args['text'], args['check_grammar'])
    return jsonify({'result': ret})


class UserApiResource(Resource):
    user_pars = reqparse.RequestParser()
    user_pars.add_argument('id', type=int)
    user_pars.add_argument('public_id', type=int)
    user_pars.add_argument('name')
    user_pars.add_argument('email')
    user_pars.add_argument('password')
    user_pars.add_argument('admin', type=bool)

    @token_auth.login_required
    @admin
    def get(self):
        db_sess = db_session.create_session()
        users = db_sess.query(User).all()
        result = []
        for user in users:
            result.append({
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'admin': user.admin,
            })
        return jsonify({'users': result})

    @token_auth.login_required
    @admin
    def post(self):
        args = self.user_pars.parse_args()
        if not all((args['name'], args['email'], args['password'])):
            return make_response(jsonify({'error': 'The request must contain name, mail, password'}), 400)
        session = db_session.create_session()
        try:
            user = User()
            user.name = args['name']
            user.email = args['email']
            user.password = args['password']
            user.admin = args['admin']
            session.add(user)
            session.commit()
            return jsonify({'success': True})
        except:
            return make_response(jsonify({'error': 'A user with such data already exists'}), 405)

    @token_auth.login_required
    @admin
    def delete(self):
        args = self.user_pars.parse_args()
        if not args['id']:
            return make_response(jsonify({'error': 'The request must contain id'}), 400)
        session = db_session.create_session()
        user = session.query(User).filter(User.id == args['id']).first()
        if user:
            if user.admin:
                return make_response(jsonify({'error': 'You cannot remove admin'}), 403)
            session.delete(user)
            session.commit()
            return jsonify({'success': True})
        return make_response(jsonify({'error': 'No user with this id'}), 405)

    @token_auth.login_required
    @admin
    def put(self):
        args = self.user_pars.parse_args()
        session = db_session.create_session()
        if args.get('id'):
            user = session.query(User).filter(User.id == args['id']).first()
        elif args.get('public_id'):
            user = session.query(User).filter(User.public_id == args['public_id']).first()
        elif args.get('name'):
            user = session.query(User).filter(User.name == args['name']).first()
        elif args.get('email'):
            user = session.query(User).filter(User.email == args['email']).first()
        else:
            return make_response(jsonify({'error': 'It is impossible to identify the user from such data'}), 405)

        if user:
            if user.admin:
                return make_response(jsonify({'error': 'You cannot change admin data'}), 403)
            if args.get('public_id'):
                user.public_id = args['public_id']
            if args.get('name'):
                user.name = args['name']
            if args.get('email'):
                user.email = args['email']
            if args.get('password'):
                user.password = args['password']
            if 'admin' in args.keys():
                user.admin = bool(args['admin'])
            session.commit()
            return jsonify({'success': True})
        return make_response(jsonify({'error': 'There is no user with such parameters'}), 405)
