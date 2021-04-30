# -*- coding: utf-8 -*-
from flask import (Flask, render_template, make_response, redirect, jsonify, render_template_string, g)
from flask_login import (LoginManager, login_user, logout_user, login_required)
from flask_restful import reqparse
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

import uuid
import datetime

from data import db_session
from data.users import User
from forms.user import LoginForm, RegisterForm
from forms.morph_pars_form import MorphParsForm
from generate_morph_pars_html import GenerateMorphPars, LOGIC

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yaalex_andrew_photorus'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=1)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

Generator = GenerateMorphPars()

parser = reqparse.RequestParser()
parser.add_argument('text', required=True, type=str)

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@app.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    db_sess = db_session.create_session()
    token = g.current_user.get_token()
    db_sess.commit()
    return jsonify({'token': token})


@basic_auth.verify_password
def verify_password(name, password):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.name == name).first()
    if user is None:
        return False
    g.current_user = user
    return user.check_password(password)


@token_auth.verify_token
def verify_token(token):
    g.current_user = User.check_token(token) if token else None
    return g.current_user is not None


@token_auth.error_handler
def token_auth_error():
    return make_response(jsonify({'error': 'Unauthorized'}), 401)


@basic_auth.error_handler
def basic_auth_error():
    return make_response(jsonify({'error': 'Unauthorized'}), 401)


# basic

@app.errorhandler(404)
def not_found(error=None):
    return make_response(jsonify({'error': 'Not found'}), 404)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form, message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")

        user = User(
            name=form.name.data,
            public_id=str(uuid.uuid4()),
            email=form.email.data,
        )
        user.set_password(form.password.data)
        user.admin = True
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/')  # redirect on morph_pars
def index():
    return redirect('/morph_pars')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/morph_pars")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/api_document')
def api_document():
    return render_template('api_document.html')


@app.route('/morph_pars', methods=['GET', 'POST'])
@login_required
def morph_pars():
    form = MorphParsForm()
    if form.validate_on_submit():
        ret = Generator.main_generate(form.text.data)
        return render_template('morph_pars.html', form=form, content=render_template_string(ret))

    return render_template('morph_pars.html', form=form, content=Generator.plug())


@app.route('/api/user', methods=['GET'])
@token_auth.login_required
def get_all_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    result = []

    for user in users:
        result.append({
            'public_id': user.public_id,
            'name': user.name,
            'password': user.password,
            'admin': user.admin
        })
    return jsonify({'users': result})


@app.route('/api/morph_pars', methods=['GET'])
@token_auth.login_required
def api_morph_pars():
    args = parser.parse_args()
    ret = LOGIC.json_pars(args['text'])
    return jsonify({'result': ret})


def main():
    db_session.global_init("db/blogs.db")
    app.run()


if __name__ == '__main__':
    main()
