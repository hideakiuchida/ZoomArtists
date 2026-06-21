import enum

from sqlalchemy import Boolean, Enum, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.persistence.database import Base
from app.infrastructure.persistence.models.base import TimestampMixin, UUIDMixin


class UserRole(str, enum.Enum):
    attendee = "attendee"
    artist = "artist"
    organizer = "organizer"
    admin = "admin"


class User(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str | None] = mapped_column(String, nullable=True)
    avatar: Mapped[str | None] = mapped_column(String, nullable=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.attendee)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    notifications_enabled: Mapped[bool] = mapped_column(Boolean, default=True)

    # Location preferences
    pref_lat: Mapped[float | None] = mapped_column(Float, nullable=True)
    pref_lng: Mapped[float | None] = mapped_column(Float, nullable=True)
    pref_radius_km: Mapped[int] = mapped_column(Integer, default=5)

    # Relationships
    events: Mapped[list["Event"]] = relationship(  # noqa: F821
        "Event", back_populates="organizer", foreign_keys="Event.organizer_id"
    )
    saved_events: Mapped[list["SavedEvent"]] = relationship(  # noqa: F821
        "SavedEvent", back_populates="user"
    )
    followed_artists: Mapped[list["ArtistFollow"]] = relationship(  # noqa: F821
        "ArtistFollow", back_populates="user"
    )
