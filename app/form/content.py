#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_pagedown.fields import PageDownField
from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import SubmitField, StringField, Form, IntegerField
from wtforms.validators import DataRequired


class ArticleForm(FlaskForm):
    name = StringField('文章标题:', validators=[DataRequired()])
    body = CKEditorField('文章内容:', validators=[DataRequired()])
    submit = SubmitField('Submit')


class PostscriptForm(FlaskForm):
    body = PageDownField('what is your mind?', validators=[DataRequired()])
    submit = SubmitField()


class CommentForm(PostscriptForm):
    pass


class SearchForm(Form):
    keyboard = StringField(validators=[DataRequired(message='关键字不能为空')])
