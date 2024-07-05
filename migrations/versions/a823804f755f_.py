"""empty message

Revision ID: a823804f755f
Revises: b3b5e9def632
Create Date: 2024-07-03 17:38:39.977971

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a823804f755f'
down_revision = 'b3b5e9def632'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('travel_packages', schema=None) as batch_op:
        batch_op.alter_column('destinations',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.Text(),
               existing_nullable=True)
        batch_op.alter_column('activities',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.Text(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('travel_packages', schema=None) as batch_op:
        batch_op.alter_column('activities',
               existing_type=sa.Text(),
               type_=mysql.VARCHAR(length=255),
               existing_nullable=True)
        batch_op.alter_column('destinations',
               existing_type=sa.Text(),
               type_=mysql.VARCHAR(length=255),
               existing_nullable=True)

    # ### end Alembic commands ###