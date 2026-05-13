from sqlalchemy import (
    Text,
    TIMESTAMP,
    ForeignKey
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from sqlalchemy.sql import func

from app.models.base import Base

from datetime import datetime

class ClubAlias(Base):

    __tablename__ = "club_aliases"
    __table_args__ = {"schema": "yacht_norm"}

    id_alias: Mapped[int] = mapped_column(
        primary_key=True
    )

    raw_name: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    normalized_name: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    id_club: Mapped[int | None] = mapped_column(
        ForeignKey("yacht_norm.clubs.id_club")
    )

    status: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    confidence: Mapped[str | None] = mapped_column(
        Text
    )

    alias_type: Mapped[str | None] = mapped_column(
        Text
    )

    notes: Mapped[str | None] = mapped_column(
        Text
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now()
    )

    club = relationship(
        "Club",
        back_populates="aliases"
    )

    def __repr__(self):
        return (
            f"<ClubAlias(id={self.id_alias}, raw='{self.raw_name}', "
            f"status='{self.status}')>"
        )
    
from app.models.club import Club