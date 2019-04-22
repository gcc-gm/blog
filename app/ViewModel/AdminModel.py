from flask import url_for, flash
from flask_admin import expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_user
from wtforms import TextAreaField
from wtforms.widgets import TextArea


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class BlogView(AdminIndexView):

    @expose('/', methods=['POST', 'GET'])
    def index(self):
        from app.form.user import LoginForm

        form = LoginForm()
        if form.validate_on_submit():
            from app.models.user import User
            login_user(User.query.filter_by(email=form.email.data).first())
            flash('登陆成功!')
        return self.render('admin/index.html', form=form)


class AdminUser(ModelView):
    column_list = ('timestamp', 'id', 'nickname', 'email', 'status', 'role_id')
    column_labels = {
        'timestamp': '创建时间',
        'id': 'ID',
        'nickname': '新闻标题',
        'email': '邮箱',
        'status': '状态',
        'role_id': '角色'
    }
    can_delete = True  # disable model deletion
    page_size = 50  # the number of entries to display on the list view
    create_modal = True
    edit_modal = True

    def __init__(self, session, **kwargs):
        from app.models.user import User
        super(AdminUser, self).__init__(User, session, **kwargs)

    def is_accessible(self):
        if current_user.is_authenticated and current_user.auth_identify('superadmin'):
            return True
        return False


class AdminArticle(ModelView):
    column_list = ('timestamp', 'id', 'hot', 'author_id', 'author.nickname', 'status', 'body')
    column_labels = {
        'timestamp': 'time',
        'id': 'ID',
        'hot': '推荐',
        'author_id': 'uid',
        'author.nickname': '作者',
        'status': '状态',
        'body': '内容'
    }

    form_overrides = {
        'body': CKTextAreaField
    }

    def __init__(self, session, **kwargs):
        from app.models.content import Article
        super(AdminArticle, self).__init__(Article, session, **kwargs)

    def is_accessible(self):
        if current_user.is_authenticated and current_user.auth_identify('superadmin'):
            return True
        return False

    def render(self, template, **kwargs):
        """
        using extra js in render method allow use
        url_for that itself requires an app context
        """
        self.extra_js = [url_for('static', filename='ckeditor/ckeditor.js')]

        return super(AdminArticle, self).render(template, **kwargs)

    extra_js = []
    can_delete = True  # disable model deletion
    page_size = 50  # the number of entries to display on the list view
    create_modal = False
    edit_modal = False


class MessageAdmin(ModelView):
    pass
