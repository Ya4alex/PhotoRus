# -*- coding: utf-8 -*-
from flask import (Flask, render_template, redirect, render_template_string)
from flask_login import (LoginManager, login_user, logout_user, login_required)
from flask_restful import Api

import datetime
import os

from data import db_session
from data.users import User
from forms.user import LoginForm, RegisterForm
from forms.pars_form import SyntacticParsForm, MorphParsForm
from generate_html import GenerateSyntacticPars, GenerateMorphPars
from API import blueprint, UserApiResource

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yaalex_andrew_photorus'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=1)

api = Api(app)
api.add_resource(UserApiResource, '/api/user')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

GenerateSyntactic = GenerateSyntacticPars()
GenerateMorph = GenerateMorphPars()


@app.errorhandler(404)
def not_found(error):
    return render_template('not_found.html', title='404')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form, message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пользователь с такой почтой уже есть")
        if db_sess.query(User).filter(User.name == form.name.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пользователь с таким именем уже есть")

        user = User()
        user.name = form.name.data
        user.email = form.email.data
        user.set_password(form.password.data)

        db_sess.add(user)
        db_sess.commit()
        login_user(user)
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/')
def index():
    return redirect('/about_us')


@app.route('/about_us')
def about_us():
    return render_template('about_us.html', title='about_us')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', title='Авторизация', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/api_document')
def api_document():
    return render_template('api_document.html', title='Документация')


@app.route('/syntactic_parsing', methods=['GET', 'POST'])
@login_required
def syntactic_parsing():
    form = SyntacticParsForm()
    if form.validate_on_submit():
        ret = GenerateSyntactic.main_generate(form.text.data, form.check_grammar.data)
        return render_template('syntactic_parsing.html', form=form, content=render_template_string(ret),
                               title='Синтаксический разбор предложения')
    return render_template('syntactic_parsing.html', form=form, content=GenerateSyntactic.plug(),
                           title='Синтаксический разбор предложения')


@app.route('/morph_pars', methods=['GET', 'POST'])
@login_required
def morph_pars():
    form = MorphParsForm()
    if form.validate_on_submit():
        ret, but = GenerateMorph.main_generate(form.text.data, form.check_grammar.data)
        return render_template('morph_parsing.html', form=form, content=render_template_string(ret), but=but,
                               title='Морфологический анализ слова')
    return render_template('morph_parsing.html', form=form, content=GenerateMorph.plug(), but=GenerateMorph.plug(),
                           title='Морфологический анализ слова')


def main():
    db_session.global_init("db/blogs.db")
    app.register_blueprint(blueprint)

    db = db_session.create_session()
    db.commit()

    port = int(os.environ.get("PORT", 5000))
    app.run(port=port)


if __name__ == '__main__':
    main()
