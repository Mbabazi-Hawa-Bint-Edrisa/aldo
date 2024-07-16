"""empty message

Revision ID: 1094f41b65f2
Revises: 
Create Date: 2024-07-12 10:57:47.611776

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1094f41b65f2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notifications',
    sa.Column('notification_id', sa.Integer(), nullable=False),
    sa.Column('message', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('notification_id')
    )
    op.create_table('travel_packages',
    sa.Column('package_id', sa.Integer(), nullable=False),
    sa.Column('package_name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('destinations', sa.Text(), nullable=True),
    sa.Column('activities', sa.Text(), nullable=True),
    sa.Column('inclusions', sa.Text(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.Column('end_date', sa.Date(), nullable=True),
    sa.Column('availability', sa.Boolean(), nullable=True),
    sa.Column('image_url', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('package_id')
    )
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('contact', sa.String(length=20), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('bookings',
    sa.Column('booking_id', sa.Integer(), nullable=False),
    sa.Column('package_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('date_of_booking', sa.DateTime(), nullable=True),
    sa.Column('travel_start_date', sa.Date(), nullable=True),
    sa.Column('travel_end_date', sa.Date(), nullable=True),
    sa.Column('total_cost', sa.Float(), nullable=True),
    sa.Column('payment_status', sa.String(length=20), nullable=True),
    sa.Column('booking_status', sa.String(length=20), nullable=True),
    sa.Column('transportation', sa.String(length=100), nullable=True),
    sa.Column('booking_source', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['package_id'], ['travel_packages.package_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('booking_id')
    )
    op.create_table('payments',
    sa.Column('payment_id', sa.Integer(), nullable=False),
    sa.Column('booking_id', sa.Integer(), nullable=False),
    sa.Column('payment_date', sa.DateTime(), nullable=True),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.Column('payment_method', sa.String(length=50), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['booking_id'], ['bookings.booking_id'], ),
    sa.PrimaryKeyConstraint('payment_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payments')
    op.drop_table('bookings')
    op.drop_table('users')
    op.drop_table('travel_packages')
    op.drop_table('notifications')
    # ### end Alembic commands ###