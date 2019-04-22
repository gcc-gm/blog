#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click
from app import create_app

app = create_app()


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def sql_init(drop):
    """Initialize the database."""
    from app.models.base import db
    if drop:
        click.confirm(
            'This operation will delete the database, do you want to continue?',
            abort=True)
        db.drop_all()
        click.echo('Drop tables.')
        db.create_all()
        from app.models.user import Role
        Role.role_init()
        click.echo('Initialized database.')
    else:
        db.create_all()
        from app.models.user import Role
        Role.role_init()
        click.echo('Initialized database.')


@app.cli.command()
def init_role():
    click.echo('Initializing the roles and permissions...')
    from app.models.user import Role
    Role.role_init()
    click.echo('Done.')


@app.cli.command()
def init_st():
    click.echo('Initializing the some sorted and tags...')
    from app.models.content import Sorted, Tag
    from app.models.base import db
    default_sorted = ['实用的教程', '随笔', '学习', 'Flask', 'python']
    default_tags = ['win10', '安卓', '教程', '心情', '电脑', '骚操作']
    for con in default_sorted:
        with db.auto_commit():
            s = Sorted()
            s.name = con
            db.session.add(s)
    for t in default_tags:
        with db.auto_commit():
            tt = Tag()
            tt.name = t
            db.session.add(tt)

    click.echo('all done')


if __name__ == "__main__":
    app.run()
