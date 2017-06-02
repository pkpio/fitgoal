"""float for distances

Revision ID: ca17e014a0bf
Revises: 4c085e7f2c9f
Create Date: 2017-06-02 16:23:18.943752

"""

# revision identifiers, used by Alembic.
revision = 'ca17e014a0bf'
down_revision = '4c085e7f2c9f'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
	op.alter_column('users', 'distances', existing_type=postgresql.ARRAY(sa.Integer()), type_=postgresql.ARRAY(sa.Float()))


def downgrade():
	op.alter_column('users', 'distances', existing_type=postgresql.ARRAY(sa.Float()), type_=postgresql.ARRAY(sa.Integer()))
