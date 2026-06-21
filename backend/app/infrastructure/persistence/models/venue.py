from geoalchemy2 import Geometry
from sqlalchemy import Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.persistence.database import Base
from app.infrastructure.persistence.models.base import TimestampMixin, UUIDMixin


class Venue(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "venues"

    name: Mapped[str] = mapped_column(String, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)
    city: Mapped[str] = mapped_column(String, nullable=False, index=True)
    country: Mapped[str] = mapped_column(String, nullable=False)
    google_maps_url: Mapped[str | None] = mapped_column(String, nullable=True)
    capacity: Mapped[int | None] = mapped_column(Integer, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    accessibility: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    transit_info: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)

    # Geospatial — PostGIS Point (lng, lat), SRID 4326
    coordinates: Mapped[object] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326), nullable=False
    )

    events: Mapped[list["Event"]] = relationship("Event", back_populates="venue")  # noqa: F821
