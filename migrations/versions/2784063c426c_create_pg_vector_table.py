"""create-pg-vector-table

Revision ID: 2784063c426c
Revises: 
Create Date: 2026-08-27 19:01:21.272649

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2784063c426c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        CREATE EXTENSION IF NOT EXISTS vector;
    """)
    op.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_base (
            id SERIAL PRIMARY KEY,
            title TEXT,
            content TEXT,
            metadata JSONB,
            embedding VECTOR(1024)
        );
    """)
    op.execute("""
        CREATE INDEX ON knowledge_base USING hnsw (embedding vector_cosine_ops);
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        DROP INDEX IF EXISTS knowledge_base_embedding_idx;
    """)
    op.execute("DROP TABLE knowledge_base")
