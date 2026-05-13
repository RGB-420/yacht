from sqlalchemy import Text, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from datetime import datetime

from app.models.base import Base


class Club(Base):

    __tablename__ = "clubs"
    __table_args__ = {"schema": "yacht_norm"}

    id_club: Mapped[int] = mapped_column(
        primary_key=True
    )

    canonical_name: Mapped[str] = mapped_column(
        Text,
        unique=True,
        nullable=False
    )

    country: Mapped[str | None] = mapped_column(
        Text
    )

    website: Mapped[str | None] = mapped_column(
        Text
    )

    entity_type: Mapped[str | None] = mapped_column(
        Text
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now()
    )

    aliases = relationship(
        "ClubAlias",
        back_populates="club"
    )

    def __repr__(self):
        return f"<Club(id={self.id_club}, canonical='{self.canonical_name}')>"
    
from app.models.club_alias import ClubAlias