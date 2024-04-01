"""create user and video table

Revision ID: f9fc283c902c
Revises:
Create Date: 2024-03-28 10:47:03.650979

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'f9fc283c902c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
	sql = """
    CREATE TYPE public.video_quality_type AS ENUM (
        '240p',
        '360p',
        '480p',
        '720p',
        '1080p',
        '4K'
    );

    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        email VARCHAR UNIQUE NOT NULL,
        username VARCHAR UNIQUE,
        password VARCHAR NOT NULL,
        is_active BOOLEAN DEFAULT FALSE,
        is_superuser BOOLEAN DEFAULT FALSE,
        firstname VARCHAR,
        lastname VARCHAR
    );

    CREATE TABLE channels (
        id SERIAL PRIMARY KEY,
        channel_name VARCHAR,
        channel_description VARCHAR,
        channel_owner INTEGER REFERENCES users(id)
    );
    
    CREATE TABLE subscriptions (
        user_id INTEGER REFERENCES users(id),
        channel_id INTEGER REFERENCES channels(id),
        PRIMARY KEY (user_id, channel_id)
    );
            
    CREATE TABLE videos (
        id SERIAL PRIMARY KEY,
        title VARCHAR,
        description VARCHAR,
        upload_date TIMESTAMP,
        view_count INTEGER DEFAULT 0,
        like_count INTEGER DEFAULT 0,
        quality public.video_quality_type NOT NULL,
        raw_url VARCHAR,
        processed_url VARCHAR,
        channel_id INTEGER REFERENCES channels(id)
    );
    """
	op.execute(sql)


def downgrade() -> None:
	sql = """
    DROP TABLE videos;

    DROP TABLE subscriptions;

    DROP TABLE channels;

    DROP TABLE users;

    DROP TYPE public.video_quality_type;
    """
	op.execute(sql)
