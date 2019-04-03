#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_moment import Moment

from app.libs.blogflask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_mail import Mail
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_pagedown import PageDown
from flask_admin import Admin
from app.ViewModel.AdminModel import MyView

admin = Admin(index_view=MyView(), template_mode='bootstrap3')
pagedown = PageDown()
ckeditor = CKEditor()
csrf = CSRFProtect()
bootstrap = Bootstrap()
mail = Mail()
login_manager = LoginManager()
migrate = Migrate()
moment = Moment()


def create_app():
    from app.blog import blog
    from app.models.base import db
    from app.models.user import User

    app = Flask(__name__.split('.')[0])
    app.config.from_object('app.config.setting')
    app.config.from_object('app.config.ckeditor4')
    migrate.init_app(app, db=db)
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'blog.login'
    login_manager.login_message = '请先登陆或注册'
    login_manager.init_app(app)
    bootstrap.init_app(app)
    pagedown.init_app(app)
    ckeditor.init_app(app)
    moment.init_app(app)
    admin.init_app(app)

    csrf.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    app.register_blueprint(blog)
    return app
