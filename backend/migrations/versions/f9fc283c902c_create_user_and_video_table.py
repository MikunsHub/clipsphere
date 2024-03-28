"""create user and video table

Revision ID: f9fc283c902c
Revises: 
Create Date: 2024-03-28 10:47:03.650979

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f9fc283c902c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        email VARCHAR UNIQUE NOT NULL,
        password VARCHAR NOT NULL,
        is_active BOOLEAN DEFAULT FALSE,
        is_superuser BOOLEAN DEFAULT FALSE,
        firstname VARCHAR,
        lastname VARCHAR,
        channel_name VARCHAR
    )
    """)

    op.execute("""
    CREATE TABLE videos (
        id SERIAL PRIMARY KEY,
        title VARCHAR,
        description VARCHAR,
        upload_date TIMESTAMP,
        view_count INTEGER DEFAULT 0,
        like_count INTEGER DEFAULT 0,
        quality VARCHAR,
        raw_url VARCHAR,
        processed_url VARCHAR,
        user_id INTEGER REFERENCES users(id)
    )
    """)


def downgrade() -> None:
    op.execute("DROP TABLE videos")
    op.execute("DROP TABLE users")
