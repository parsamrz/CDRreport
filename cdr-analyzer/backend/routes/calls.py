"""
Calls endpoints for retrieving and searching call records
"""
from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from datetime import datetime, timedelta
from models import CallRecord, CallListResponse
from database import get_db, get_calls

router = APIRouter()

@router.get("/calls", response_model=CallListResponse)
async def list_calls(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=100, description="Records per page"),
    from_date: Optional[str] = Query(None, description="Start date (ISO format)"),
    to_date: Optional[str] = Query(None, description="End date (ISO format)"),
):
    """
    Get paginated list of calls with optional date filtering
    """
    try:
        with get_db() as conn:
            calls, total = get_calls(
                conn,
                page=page,
                limit=limit,
                from_date=from_date,
                to_date=to_date
            )
        
        # Convert to Pydantic models
        call_records = [
            CallRecord(
                unique_id=call['unique_id'],
                timestamp=datetime.fromisoformat(call['timestamp']),
                caller_number=call['caller_number'],
                extension=call['extension'],
                status=call['status'],
                duration=call['duration']
            )
            for call in calls
        ]
        
        return CallListResponse(
            calls=call_records,
            total=total,
            page=page,
            limit=limit
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/calls/search", response_model=CallListResponse)
async def search_calls(
    phone: str = Query(..., min_length=3, description="Phone number to search"),
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100)
):
    """
    Search calls by partial phone number match
    """
    try:
        with get_db() as conn:
            calls, total = get_calls(
                conn,
                page=page,
                limit=limit,
                search=phone
            )
        
        call_records = [
            CallRecord(
                unique_id=call['unique_id'],
                timestamp=datetime.fromisoformat(call['timestamp']),
                caller_number=call['caller_number'],
                extension=call['extension'],
                status=call['status'],
                duration=call['duration']
            )
            for call in calls
        ]
        
        return CallListResponse(
            calls=call_records,
            total=total,
            page=page,
            limit=limit
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
