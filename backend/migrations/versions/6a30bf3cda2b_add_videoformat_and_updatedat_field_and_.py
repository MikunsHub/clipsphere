"""add videoFormat and updatedAt field and make quality field optional

Revision ID: 6a30bf3cda2b
Revises: f9fc283c902c
Create Date: 2024-04-20 23:11:54.621019

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '6a30bf3cda2b'
down_revision: Union[str, None] = 'f9fc283c902c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
	sql = """
        CREATE TYPE public.video_format_type AS ENUM ('mp4', 'avi', 'mov', 'mkv', 'webm');

        ALTER TABLE videos
            ADD COLUMN video_format public.video_format_type,
            ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ALTER COLUMN upload_date SET DEFAULT CURRENT_TIMESTAMP,
            ALTER COLUMN quality DROP NOT NULL;
    """
	op.execute(sql)


def downgrade() -> None:
	sql = """
        ALTER TABLE videos
            ALTER COLUMN quality SET NOT NULL,
            DROP COLUMN video_format,
            DROP COLUMN updated_at,
            ALTER COLUMN upload_date DROP DEFAULT;

        DROP TYPE public.video_format_type;
    """
	op.execute(sql)
