from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy import func
from sqlalchemy.orm import Session
from framework.db import get_db
from models.forecast import Forecast, ForecastCreate
from datetime import datetime, UTC

router = APIRouter()

def serialize_sqlalchemy_obj(obj):
    """
    Convert a SQLAlchemy ORM model instance into a dictionary.

    Args:
        obj: SQLAlchemy model instance.

    Returns:
        dict: Dictionary containing all column names and their values.
    """
    return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}


@router.get("/api/v1/forecast/latest")
def get_latest_forecasts(
    db: Session = Depends(get_db)
):
    """
    Retrieve the latest collected Forecast records.
    Based on the maximum collection_time in the table.
    """
    try:
        # Get the latest collection_time
        latest_time = db.query(func.max(Forecast.collection_time)).scalar()

        if not latest_time:
            return []

        # Get all forecasts with that collection_time
        forecast_records = (
            db.query(Forecast)
            .filter(Forecast.collection_time == latest_time)
            .order_by(Forecast.forecast_date)
            .all()
        )

        return [serialize_sqlalchemy_obj(item) for item in forecast_records]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/api/v1/forecast")
def list_forecast(
    page: int = Query(1, ge=1, description="Page number to retrieve"),
    limit: int = Query(10, ge=1, le=100, description="Number of records per page"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a paginated list of Forecast records.

    Args:
        page (int): Page number starting from 1.
        limit (int): Maximum number of records to return per page.
        db (Session): SQLAlchemy database session.

    Returns:
        list[dict]: A list of serialized Forecast records.
    """
    try:
        offset = (page - 1) * limit
        forecast_records = db.query(Forecast).offset(offset).limit(limit).all()
        return [serialize_sqlalchemy_obj(item) for item in forecast_records]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/api/v1/forecast")
def create_record(
    forecast_data: ForecastCreate = Body(..., description="Data for the new record"),
    db: Session = Depends(get_db)
):
    """
    Create a new Forecast record.

    Args:
        forecast_data (ForecastCreate): Data model for the record to create.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: The newly created Forecast record.
    """
    try:
        data = forecast_data.model_dump(exclude_unset=True)
        new_record = Forecast(**data)
        new_record.create_date = datetime.now(UTC)
        new_record.update_date = datetime.now(UTC)

        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        return serialize_sqlalchemy_obj(new_record)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/api/v1/forecast/{id}")
def get_forecast_by_id(id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single Forecast record by ID.

    Args:
        id (int): The ID of the record.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: The matching Forecast record.

    Raises:
        HTTPException: If the record is not found.
    """
    try:
        record = db.query(Forecast).filter(Forecast.id == id).first()
        if not record:
            raise HTTPException(status_code=404, detail=f"Forecast with id {id} not found")
        return serialize_sqlalchemy_obj(record)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.put("/api/v1/forecast/{id}")
def update_forecast_full(
    id: int,
    forecast_data: ForecastCreate = Body(..., description="Updated data for the record"),
    db: Session = Depends(get_db)
):
    """
    Fully update an existing Forecast record (all fields required).

    Args:
        id (int): The ID of the record to update.
        forecast_data (ForecastCreate): Updated record data (all fields).
        db (Session): SQLAlchemy database session.

    Returns:
        dict: The updated Forecast record.

    Raises:
        HTTPException: If the record is not found.
    """
    try:
        record = db.query(Forecast).filter(Forecast.id == id).first()
        if not record:
            raise HTTPException(status_code=404, detail=f"Forecast with id {id} not found")

        data = forecast_data.model_dump(exclude_unset=False)
        for key, value in data.items():
            setattr(record, key, value)

        record.update_date = datetime.now(UTC)
        db.commit()
        db.refresh(record)
        return serialize_sqlalchemy_obj(record)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.patch("/api/v1/forecast/{id}")
def update_forecast_partial(
    id: int,
    forecast_data: ForecastCreate = Body(..., description="Partial updated data for the record"),
    db: Session = Depends(get_db)
):
    """
    Partially update an existing Forecast record (only provided fields are updated).

    Args:
        id (int): The ID of the record to update.
        Forecast_data (ForecastCreate): Partial updated data.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: The updated Forecast record.

    Raises:
        HTTPException: If the record is not found.
    """
    try:
        record = db.query(Forecast).filter(Forecast.id == id).first()
        if not record:
            raise HTTPException(status_code=404, detail=f"Forecast with id {id} not found")

        data = forecast_data.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(record, key, value)

        record.update_date = datetime.now(UTC)
        db.commit()
        db.refresh(record)
        return serialize_sqlalchemy_obj(record)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/api/v1/forecast/{id}")
def delete_forecast(id: int, db: Session = Depends(get_db)):
    """
    Delete a Forecast record by ID.

    Args:
        id (int): The ID of the record to delete.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: Confirmation message.

    Raises:
        HTTPException: If the record is not found.
    """
    try:
        record = db.query(Forecast).filter(Forecast.id == id).first()
        if not record:
            raise HTTPException(status_code=404, detail=f"Forecast with id {id} not found")

        db.delete(record)
        db.commit()
        return {"detail": f"Forecast with id {id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
