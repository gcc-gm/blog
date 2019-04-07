#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class TokenOperation():
    @classmethod
    def generate_token(cls, **keyword):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=current_app.config['EXPIRATION'])
        # 为byte, 故要编码
        return s.dumps(keyword).decode('utf-8')

    @classmethod
    def verify_token(cls, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except Exception as e:
            raise e

        return data
