import enum
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.persistence.database import Base
from app.infrastructure.persistence.models.base import TimestampMixin, UUIDMixin


class EventCategory(str, enum.Enum):
    music = "music"
    visual_art = "visual_art"
    theater = "theater"
    dance = "dance"
    spoken_word = "spoken_word"
    cinema = "cinema"
    festival = "festival"
    workshop = "workshop"
    street_performance = "street_performance"


class EventStatus(str, enum.Enum):
    draft = "draft"
    pending = "pending"
    published = "published"
    cancelled = "cancelled"
    past = "past"


class Event(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "events"

    title: Mapped[str] = mapped_column(String, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[EventCategory] = mapped_column(Enum(EventCategory), nullable=False, index=True)
    status: Mapped[EventStatus] = mapped_column(
        Enum(EventStatus), default=EventStatus.draft, index=True
    )

    start_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    end_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    cover_image: Mapped[str | None] = mapped_column(String, nullable=True)
    gallery: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    video_url: Mapped[str | None] = mapped_column(String, nullable=True)

    ticket_url: Mapped[str | None] = mapped_column(String, nullable=True)
    ticket_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    currency: Mapped[str] = mapped_column(String, default="MXN")
    is_free: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    capacity: Mapped[int | None] = mapped_column(Integer, nullable=True)

    tags: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)

    venue_id: Mapped[str] = mapped_column(String, ForeignKey("venues.id"), nullable=False)
    organizer_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)

    venue: Mapped["Venue"] = relationship("Venue", back_populates="events")  # noqa: F821
    organizer: Mapped["User"] = relationship(  # noqa: F821
        "User", back_populates="events", foreign_keys=[organizer_id]
    )
    event_artists: Mapped[list["EventArtist"]] = relationship(
        "EventArtist", back_populates="event", cascade="all, delete-orphan"
    )
    saved_by: Mapped[list["SavedEvent"]] = relationship(
        "SavedEvent", back_populates="event", cascade="all, delete-orphan"
    )


class EventArtist(Base, UUIDMixin):
    __tablename__ = "event_artists"

    event_id: Mapped[str] = mapped_column(String, ForeignKey("events.id", ondelete="CASCADE"))
    artist_id: Mapped[str] = mapped_column(String, ForeignKey("artists.id", ondelete="CASCADE"))
    order: Mapped[int] = mapped_column(Integer, default=0)

    event: Mapped[Event] = relationship("Event", back_populates="event_artists")
    artist: Mapped["Artist"] = relationship("Artist", back_populates="event_artists")  # noqa: F821


class SavedEvent(Base, UUIDMixin):
    __tablename__ = "saved_events"

    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id", ondelete="CASCADE"))
    event_id: Mapped[str] = mapped_column(String, ForeignKey("events.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship("User", back_populates="saved_events")  # noqa: F821
    event: Mapped[Event] = relationship("Event", back_populates="saved_by")
