from flask_admin import BaseView, expose, AdminIndexView


class MyView(AdminIndexView):
    # def __init__(self, models_name, session, **kwargs):
    #     super(MyView, self).__init__(models_name, session, **kwargs)

    @expose('/')
    def index(self):
        return self.render('admin/index.html')
