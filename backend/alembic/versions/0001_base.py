"""Base revision: empty anchor for the migration chain.

Tables land here starting with FMCG-008 (master data). This revision is intentionally
empty so the upgrade/downgrade harness is exercised before any schema exists.

Revision ID: 0001
Revises:
"""

from collections.abc import Sequence

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
