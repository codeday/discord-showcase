"""initial commit

Revision ID: 7d23fcd11240
Revises: 
Create Date: 2020-11-25 17:22:42.714295

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d23fcd11240'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pods',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('tc_id', sa.String(), nullable=False),
    sa.Column('mentor', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teams',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('showcase_id', sa.String(), nullable=False),
    sa.Column('pod_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['pod_id'], ['pods.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('teams')
    op.drop_table('pods')
    # ### end Alembic commands ###
