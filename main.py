from flask import (Flask, render_template, make_response, redirect, request, jsonify, render_template_string)
from flask_login import (LoginManager, login_user, logout_user, login_required)
from flask_restful import reqparse

import uuid
import jwt
import datetime
from functools import wraps
from werkzeug.security import check_password_hash

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

Generator = GenerateMorphPars()

parser = reqparse.RequestParser()
parser.add_argument('text', required=True, type=str)


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


@app.route('/')
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


@app.route('/morph_pars', methods=['GET', 'POST'])
@login_required
def morph_pars():
    form = MorphParsForm()
    if form.validate_on_submit():
        try:
            ret = Generator.main_generate(form.text.data)
            return render_template('morph_pars.html', form=form, content=render_template_string(ret))
        except:
            return render_template('morph_pars.html', form=form, content=Generator.plug(),
                                   errors='Не получилось(\nПопробуйте другой текст.')
    return render_template('morph_pars.html', form=form, content=Generator.plug())


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        print(request.headers)
        if 'token' in request.headers:
            token = request.headers['token']
        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            db_sess = db_session.create_session()
            current_user = db_sess.query(User).filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'token is invalid'})
        return f(current_user, *args, **kwargs)

    return decorator


@app.route('/api/get_token', methods=['GET', 'POST'])
def get_token():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    db_sess = db_session.create_session()
    user = db_sess.query(User).filter_by(name=auth.username).first()
    if not user:
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "Password required"'})
    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},
            app.config['SECRET_KEY'],
            algorithm='HS256',
        )
        return jsonify({'token': token})

    return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "Password required"'})


@app.route('/api/user', methods=['GET'])
@token_required
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
@token_required
def get():
    args = parser.parse_args()
    ret = LOGIC.json_pars(args['text'])
    return jsonify({'result': ret})


def main():
    db_session.global_init("db/blogs.db")
    app.run()


if __name__ == '__main__':
    main()
