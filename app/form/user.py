#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo
from app.models.user import User


class RegisterForm(FlaskForm):
    nickname = StringField('昵称:', validators=[DataRequired(), Length(2, 19, message='长度不符合')])

    email = StringField('请输入你的电子邮箱:', validators=[DataRequired(), Length(8, 64),
                                                  Email(message='电子邮箱不符合规范！')])
    submit = SubmitField('Submit')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError('该电子邮件已被注册!')


class SetPasswordForm(FlaskForm):
    password_1 = PasswordField('请输入你的密码:', validators=[DataRequired(), Length(6, 15, message='密码长度不符合')])
    password_2 = PasswordField('再次确认你的密码:', validators=[DataRequired(), EqualTo('password_1', message='两次密码不一致,请重新输入')])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    email = StringField('请输入你的电子邮箱:', validators=[DataRequired(), Email(message='电子邮箱不符合规范！')])
    password = PasswordField('请输入你的密码:', validators=[DataRequired(), Length(6, 15, message='密码长度不符合')])

    submit = SubmitField('Submit')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if not user:
            raise ValidationError('找不到该邮箱')

    def validate_password(self, field):
        from app.models.user import User
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            if not user.check_password(field.data):
                raise ValidationError('密码错误')


class EmailForm(FlaskForm):
    email = StringField('请输入你的电子邮箱:', validators=[DataRequired(), Length(8, 64),
                                                  Email(message='电子邮箱不符合规范')])
    submit = SubmitField('Submit')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if not user:
            raise ValidationError('找不到该邮箱')


class ChangePwdForm(FlaskForm):
    old_pwd = PasswordField('输入当前密码:', validators=[DataRequired()])
    new_pwd1 = PasswordField('输入新密码:', validators=[DataRequired(), Length(6, 15)])
    new_pwd2 = PasswordField('再次输入:', validators=[DataRequired(), EqualTo('new_pwd1', message='两次输入不一致')])
    submit = SubmitField('Submit')

    def validate_old_pwd(self, field):
        user = User.query.get_or_404(current_user.id)
        if user.password != field.data:
            raise ValidationError('旧密码错误')
