#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click
from app import create_app

app = create_app()


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    from app.models.base import db

    if drop:
        click.confirm('This operation will delete the database, do you want to continue?', abort=True)
        db.drop_all()
        click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')
    else:
        db.create_all()
        click.echo('Initialized database.')


@app.cli.command()
def initrole():
    click.echo('Initializing the roles and permissions...')
    from app.models.user import Role
    Role.role_init()
    click.echo('Done.')


@app.cli.command()
def faker(count=10):
    from faker import Faker
    from app.models.base import db
    from app.models.user import User
    from app.models.content import Article, Comment, Postscript

    faker = Faker('zh_CN')
    for i in range(count):
        user = User()
        article = Article()
        comment = Comment()
        postscript = Postscript()

        user.nickname = faker.user_name()
        user.email = faker.safe_email()
        user.password = faker.isbn10()

        article.name = faker.user_name()
        article.body = faker.text()

        comment.body = faker.sentence()

        postscript.body = faker.sentence()

        with db.auto_commit():
            db.session.add_all([user, article, comment, postscript])


@app.cli.command()
def faker2(count=10):
    from faker import Faker
    from app.models.base import db
    from app.models.content import Like
    faker = Faker('zh_CN')
    for i in range(count):
        with db.auto_commit():
            like = Like()
            like.uid = 12
            like.aid = 3
            db.session.add(like)
    click.echo('Done.')
