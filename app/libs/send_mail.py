#!/usr/bin/env python
# -*- coding: utf-8 -*-
from threading import Thread

from flask import current_app, render_template
from flask_mail import Message

from app import mail

def send_async_email(app, msg):
    # 入栈
    with app.app_context():
        try:

            mail.send(msg)
        except Exception as e:
            raise e


def send_mail(to, subject, template, **kwargs):
    msg = Message('[测试]' + '' + subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.html = render_template(template, **kwargs)
    app = current_app._get_current_object()
    thread_send_mail = Thread(target=send_async_email, args=[app, msg])
    thread_send_mail.start()
