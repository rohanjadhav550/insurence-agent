"""create threads conversations messages tables

Baselines the schema for the app's own "insurence_agent" database, matching
the raw SQL already run against it in app/main.py and app/rags/insurence_chat.py:
  - threads: created per chat session, referenced by thread_id everywhere else
  - conversations: one row per thread, holds the sidebar title and last-updated time
  - messages: chat history rows (user + assistant), scoped to a thread

Revision ID: 8e95407b5fa4
Revises:
Create Date: 2026-07-10 07:48:53.483141

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '8e95407b5fa4'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        CREATE TABLE threads (
            thread_id VARCHAR(36) NOT NULL PRIMARY KEY,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    op.execute("""
        CREATE TABLE conversations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            thread_id VARCHAR(36) NOT NULL,
            title VARCHAR(255) NOT NULL DEFAULT 'New Conversation',
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            UNIQUE KEY uq_conversations_thread_id (thread_id),
            CONSTRAINT fk_conversations_thread_id FOREIGN KEY (thread_id)
                REFERENCES threads (thread_id) ON DELETE CASCADE
        )
    """)

    op.execute("""
        CREATE TABLE messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            thread_id VARCHAR(36) NOT NULL,
            role VARCHAR(20) NOT NULL,
            content TEXT NOT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            KEY idx_messages_thread_id (thread_id),
            CONSTRAINT fk_messages_thread_id FOREIGN KEY (thread_id)
                REFERENCES threads (thread_id) ON DELETE CASCADE
        )
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE IF EXISTS messages")
    op.execute("DROP TABLE IF EXISTS conversations")
    op.execute("DROP TABLE IF EXISTS threads")
