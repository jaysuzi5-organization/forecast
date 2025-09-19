"""
Forecast Model and Pydantic Schema

This module defines:
- The SQLAlchemy ORM model for persisting Forecast data.
- The Pydantic schema for validating API requests when creating a Forecast.
"""

from sqlalchemy import Column, DateTime, Date, Integer, String
from framework.db import Base
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Forecast(Base):
    """
    SQLAlchemy ORM model representing a Forecast record.

    Attributes:
        collection_time (datetime): The time the forecast was collected (part of PK).
        forecast_date (date): The forecasted date (part of PK).
        temperature_min (int | None): Minimum forecasted temperature.
        temperature_max (int | None): Maximum forecasted temperature.
        humidity_min (int | None): Minimum forecasted humidity.
        humidity_max (int | None): Maximum forecasted humidity.
        description (str | None): Forecast description, up to 200 characters.
    """

    __tablename__ = "weather_forecast"

    collection_time = Column(DateTime(timezone=True), primary_key=True, nullable=False)
    forecast_date = Column(Date, primary_key=True, nullable=False)
    temperature_min = Column(Integer, nullable=True)
    temperature_max = Column(Integer, nullable=True)
    humidity_min = Column(Integer, nullable=True)
    humidity_max = Column(Integer, nullable=True)
    description = Column(String(200), nullable=True)

    def __repr__(self):
        """
        Returns a string representation of the Forecast instance.

        Example:
            <Forecast(collection_time=2025-09-19T10:00Z, forecast_date=2025-09-20)>
        """
        return (
            f"<Forecast(collection_time={self.collection_time}, "
            f"forecast_date={self.forecast_date}, "
            f"temp_min={self.temperature_min}, temp_max={self.temperature_max})>"
        )


class ForecastCreate(BaseModel):
    """
    Pydantic schema for creating a new Forecast.

    Attributes:
        collection_time (datetime): The time the forecast was collected.
        forecast_date (date): The forecasted date.
        temperature_min (int | None): Minimum forecasted temperature.
        temperature_max (int | None): Maximum forecasted temperature.
        humidity_min (int | None): Minimum forecasted humidity.
        humidity_max (int | None): Maximum forecasted humidity.
        description (str | None): Forecast description.
    """

    collection_time: datetime
    forecast_date: datetime
    temperature_min: Optional[int] = None
    temperature_max: Optional[int] = None
    humidity_min: Optional[int] = None
    humidity_max: Optional[int] = None
    description: Optional[str] = None
