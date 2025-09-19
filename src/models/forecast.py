"""
Forecast Model and Pydantic Schema

This module defines:
- The SQLAlchemy ORM model for persisting Forecast data.
- The Pydantic schema for validating API requests when creating a Forecast.
"""

from sqlalchemy import Column, DateTime, Integer, String, Numeric
from framework.db import Base
from pydantic import BaseModel
from typing import Optional


class Forecast(Base):
    """
    SQLAlchemy ORM model representing a Forecast record.

    Attributes:
        collection_time (datetime): Primary key, timestamp of the forecast.
        temperature (int | None): Current temperature.
        temperature_min (int | None): Minimum forecasted temperature.
        temperature_max (int | None): Maximum forecasted temperature.
        humidity (int | None): Relative humidity percentage.
        description (str | None): Weather description (e.g. 'clear sky').
        feels_like (int | None): Feels-like temperature.
        wind_speed (float | None): Wind speed in chosen unit.
        wind_direction (int | None): Wind direction in degrees.
    """

    __tablename__ = "weather_forecast"

    collection_time = Column(DateTime(timezone=True), primary_key=True, nullable=False)
    temperature = Column(Integer, nullable=True)
    temperature_min = Column(Integer, nullable=True)
    temperature_max = Column(Integer, nullable=True)
    humidity = Column(Integer, nullable=True)
    description = Column(String(200), nullable=True)
    feels_like = Column(Integer, nullable=True)
    wind_speed = Column(Numeric, nullable=True)
    wind_direction = Column(Integer, nullable=True)

    def __repr__(self):
        """
        Returns a string representation of the Forecast instance.
        """
        return (
            f"<Forecast(collection_time={self.collection_time}, "
            f"temperature={self.temperature}, "
            f"description='{self.description}')>"
        )


class ForecastCreate(BaseModel):
    """
    Pydantic schema for creating a new Forecast.

    Attributes:
        collection_time (datetime): Timestamp of the forecast (UTC).
        temperature (int | None): Current temperature.
        temperature_min (int | None): Minimum forecasted temperature.
        temperature_max (int | None): Maximum forecasted temperature.
        humidity (int | None): Relative humidity percentage.
        description (str | None): Weather description (e.g. 'clear sky').
        feels_like (int | None): Feels-like temperature.
        wind_speed (float | None): Wind speed in chosen unit.
        wind_direction (int | None): Wind direction in degrees.
    """
    collection_time: str
    temperature: Optional[int] = None
    temperature_min: Optional[int] = None
    temperature_max: Optional[int] = None
    humidity: Optional[int] = None
    description: Optional[str] = None
    feels_like: Optional[int] = None
    wind_speed: Optional[float] = None
    wind_direction: Optional[int] = None
