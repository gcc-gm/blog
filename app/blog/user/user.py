#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, logout_user, login_user, current_user
from app.blog import blog
from app.form.user import RegisterForm, SetPasswordForm, LoginForm, EmailForm, ChangePwdForm
from app.libs.Token import TokenOperation
from app.models.base import db
from app.models.user import User
from app.libs.send_mail import send_mail


@blog.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email_token = TokenOperation.generate_token(email=form.email.data)
        send_mail(
            'gccgm8564@qq.com',
            'token',
            'email/send_token.html',
            email_token=email_token, email=form.email.data)
        with db.auto_commit():
            user = User(nickname=form.nickname.data, email=form.email.data)
            db.session.add(user)
        flash('请注意查收邮件!')
        return redirect(url_for('blog.index'))

    return render_template('user/register.html', form=form)


@blog.route('/setPassword/<string:token>', methods=['POST', 'GET'])
def set_password_by_token(token):
    form = SetPasswordForm()
    email = TokenOperation.verify_token(token)['email']
    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first_or_404()
        with db.auto_commit():
            user.password = form.password_1.data
            flash('设置成功!')
        return redirect(url_for('blog.login'))
    return render_template('user/setpassword.html', form=form)


@blog.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        flash('请不要重复登陆!')
        return redirect(url_for('blog.index'))
    form = LoginForm()
    if form.validate_on_submit():
        login_user(User.query.filter_by(email=form.email.data).first())
        _next = request.args.get('next')
        if _next and _next.startswith('/'):
            return redirect(_next)
        else:
            flash('欢迎来到BLK的个人博客!')
            return redirect(url_for('blog.index'))
    return render_template('user/login.html', form=form)


@blog.route('/logout')
@login_required
def logout():
    logout_user()
    return 'logout'


@blog.route('/forget', methods=['POST', 'GET'])
def forget_request():
    form = EmailForm()
    if form.validate_on_submit():
        token = TokenOperation.generate_token(email=form.email.data)
        send_mail(
            form.email.data,
            'forget_request',
            'email/text.html',
            email_token=token)
        flash('success')
        return redirect(url_for('blog.index'))
    return render_template('user/forget_request.html', form=form)


@blog.route('/reset_pwd', methods=['POST', 'GET'])
@login_required
def rest_pwd():
    form = ChangePwdForm()
    if form.validate_on_submit():
        with db.auto_commit():
            user = User.query.get_or_404(current_user.id)
            user.password = form.new_pwd1.data
            db.session.add(user)
            flash('设置成功!')
        return redirect(url_for('blog.login'))
    return render_template('user/reset_pwd.html', form=form)
