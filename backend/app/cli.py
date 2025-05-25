import click
from flask.cli import with_appcontext
from .models import db

@click.command('reset-db')
@with_appcontext
def reset_db():
    """重置数据库：删除并重新创建所有表"""
    db.drop_all()
    db.create_all()
    click.echo("✅ 数据库已重置")