#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_pagedown.fields import PageDownField
from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import SubmitField, StringField, Form, FileField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired


class ArticleForm(FlaskForm):
    name = StringField('文章标题:', validators=[DataRequired()])
    body = CKEditorField('文章内容:', validators=[DataRequired()])
    intro = StringField('简单的文章简介 :', validators=[DataRequired()])
    pre_image = FileField('文章预览图', render_kw={'accept': ".jpg, .png"},
                          validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    # tags = SelectMultipleField('some word', choices=Tag.get_tags())
    # sort = SelectField('Job', choices=Sorted.get_sort())
    submit = SubmitField('Submit')

    def validate_name(self, field):
        from app.models.content import Article
        article = Article.query.filter_by(name=field.data).first()
        return article is None


class PostscriptForm(FlaskForm):
    body = PageDownField('what is your mind?', validators=[DataRequired()])
    submit = SubmitField()


class CommentForm(PostscriptForm):
    pass


class SearchForm(Form):
    keyboard = StringField(validators=[DataRequired(message='关键字不能为空')])
