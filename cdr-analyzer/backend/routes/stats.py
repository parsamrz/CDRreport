"""
Statistics endpoints for dashboard visualization
"""
from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from datetime import datetime, timedelta
from models import StatsResponse, DailyStats, ExtensionStats, UniqueCallersStats
from database import get_db

router = APIRouter()

@router.get("/stats/daily", response_model=list[DailyStats])
async def get_daily_stats(
    from_date: Optional[str] = Query(None, description="Start date (ISO format)"),
    to_date: Optional[str] = Query(None, description="End date (ISO format)")
):
    """
    Get daily call statistics for the specified date range
    Returns count of answered and missed calls per day
    """
    try:
        # Default to last 7 days if no dates provided
        if not from_date:
            from_date = (datetime.now() - timedelta(days=7)).isoformat()
        if not to_date:
            to_date = datetime.now().isoformat()
        
        with get_db() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    DATE(timestamp) as call_date,
                    SUM(CASE WHEN status = 'ANSWERED' THEN 1 ELSE 0 END) as answered,
                    SUM(CASE WHEN status = 'MISSED' THEN 1 ELSE 0 END) as missed,
                    COUNT(*) as total
                FROM call_records
                WHERE timestamp >= ? AND timestamp <= ?
                GROUP BY DATE(timestamp)
                ORDER BY call_date ASC
            """, (from_date, to_date))
            
            results = cursor.fetchall()
            
            daily_stats = [
                DailyStats(
                    date=row['call_date'],
                    answered=row['answered'],
                    missed=row['missed'],
                    total=row['total']
                )
                for row in results
            ]
            
            return daily_stats
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/extensions", response_model=list[ExtensionStats])
async def get_extension_stats(
    from_date: Optional[str] = Query(None, description="Start date (ISO format)"),
    to_date: Optional[str] = Query(None, description="End date (ISO format)")
):
    """
    Get extension performance statistics
    Returns call count and duration per extension
    """
    try:
        # Default to last 7 days if no dates provided
        if not from_date:
            from_date = (datetime.now() - timedelta(days=7)).isoformat()
        if not to_date:
            to_date = datetime.now().isoformat()
        
        with get_db() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    extension,
                    COUNT(*) as call_count,
                    SUM(duration) as total_duration,
                    AVG(duration) as avg_duration
                FROM call_records
                WHERE extension IS NOT NULL 
                    AND status = 'ANSWERED'
                    AND timestamp >= ? 
                    AND timestamp <= ?
                GROUP BY extension
                ORDER BY call_count DESC
            """, (from_date, to_date))
            
            results = cursor.fetchall()
            
            extension_stats = [
                ExtensionStats(
                    extension=row['extension'],
                    call_count=row['call_count'],
                    total_duration=row['total_duration'],
                    avg_duration=round(row['avg_duration'], 2)
                )
                for row in results
            ]
            
            return extension_stats
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/unique-callers", response_model=list[UniqueCallersStats])
async def get_unique_callers_stats(
    from_date: Optional[str] = Query(None, description="Start date (ISO format)"),
    to_date: Optional[str] = Query(None, description="End date (ISO format)")
):
    """
    Get unique callers statistics per day
    Counts distinct caller numbers - each phone number is counted once per day
    regardless of how many times they called
    """
    try:
        # Default to last 7 days if no dates provided
        if not from_date:
            from_date = (datetime.now() - timedelta(days=7)).isoformat()
        if not to_date:
            to_date = datetime.now().isoformat()
        
        with get_db() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    DATE(timestamp) as call_date,
                    COUNT(DISTINCT caller_number) as unique_callers,
                    COUNT(*) as total_calls
                FROM call_records
                WHERE DATE(timestamp) >= DATE(?)
                    AND DATE(timestamp) <= DATE(?)
                    AND caller_number IS NOT NULL
                    AND caller_number != ''
                GROUP BY DATE(timestamp)
                ORDER BY call_date ASC
            """, (from_date, to_date))
            
            results = cursor.fetchall()
            
            unique_callers_stats = [
                UniqueCallersStats(
                    date=row['call_date'],
                    unique_callers=row['unique_callers'],
                    total_calls=row['total_calls']
                )
                for row in results
            ]
            
            return unique_callers_stats
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
