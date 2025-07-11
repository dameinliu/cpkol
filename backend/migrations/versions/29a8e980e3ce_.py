"""empty message

Revision ID: 29a8e980e3ce
Revises: 
Create Date: 2025-07-09 16:53:16.275912

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29a8e980e3ce'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('influencer', schema=None) as batch_op:
        batch_op.alter_column('handle',
               existing_type=sa.VARCHAR(length=254),
               type_=sa.String(length=128),
               existing_nullable=False)
        batch_op.alter_column('sec_uid',
               existing_type=sa.VARCHAR(length=254),
               type_=sa.String(length=256),
               existing_nullable=True)
        batch_op.alter_column('updated_date',
               existing_type=sa.DATE(),
               type_=sa.DateTime(),
               existing_nullable=True)
        batch_op.alter_column('content_type',
               existing_type=sa.VARCHAR(length=254),
               type_=sa.String(length=64),
               existing_nullable=True)
        batch_op.alter_column('note',
               existing_type=sa.VARCHAR(length=254),
               type_=sa.String(length=256),
               existing_nullable=True)
        batch_op.create_unique_constraint(None, ['handle'])

    with op.batch_alter_table('videos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('comment_count', sa.Integer(), nullable=True))
        batch_op.alter_column('id',
               existing_type=sa.VARCHAR(length=254),
               nullable=False)
        batch_op.drop_column('comment_cou')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('videos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('comment_cou', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.alter_column('id',
               existing_type=sa.VARCHAR(length=254),
               nullable=True)
        batch_op.drop_column('comment_count')

    with op.batch_alter_table('influencer', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('note',
               existing_type=sa.String(length=256),
               type_=sa.VARCHAR(length=254),
               existing_nullable=True)
        batch_op.alter_column('content_type',
               existing_type=sa.String(length=64),
               type_=sa.VARCHAR(length=254),
               existing_nullable=True)
        batch_op.alter_column('updated_date',
               existing_type=sa.DateTime(),
               type_=sa.DATE(),
               existing_nullable=True)
        batch_op.alter_column('sec_uid',
               existing_type=sa.String(length=256),
               type_=sa.VARCHAR(length=254),
               existing_nullable=True)
        batch_op.alter_column('handle',
               existing_type=sa.String(length=128),
               type_=sa.VARCHAR(length=254),
               existing_nullable=False)

    # ### end Alembic commands ###
