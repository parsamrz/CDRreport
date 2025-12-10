"""
Admin endpoints for database management
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import get_db, clear_all_data

router = APIRouter()

class ClearResponse(BaseModel):
    """Response model for clear database operation"""
    success: bool
    message: str
    records_deleted: int

@router.delete("/clear-database")
async def clear_database():
    """
    Clear all data from the database
    ⚠️ WARNING: This will delete all call records permanently!
    """
    try:
        with get_db() as conn:
            count = clear_all_data(conn)
        
        return ClearResponse(
            success=True,
            message=f"Database cleared successfully. {count} records deleted.",
            records_deleted=count
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear database: {str(e)}")
