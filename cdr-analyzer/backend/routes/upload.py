"""
Upload endpoint for CDR files
"""
from fastapi import APIRouter, File, UploadFile, HTTPException
from models import UploadResponse
from processor import process_cdr_file
from database import get_db, insert_call_record

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_cdr_file(file: UploadFile = File(...)):
    """
    Upload and process CDR CSV file
    
    - Accepts CSV files up to 10MB
    - Groups records by UniqueID
    - Extracts unique calls
    - Prevents duplicates
    """
    # Validate file type
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Only CSV files are accepted."
        )
    
    # Read file content
    content = await file.read()
    
    # Validate file size (10MB limit)
    max_size = 10 * 1024 * 1024  # 10MB
    if len(content) > max_size:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds limit of 10MB."
        )
    
    try:
        # Process the CSV file
        records, total_records, unique_calls = process_cdr_file(content)
        
        # Insert records into database
        inserted = 0
        skipped = 0
        
        with get_db() as conn:
            for record in records:
                if insert_call_record(conn, record):
                    inserted += 1
                else:
                    skipped += 1
        
        message = f"Processed {total_records} records, {inserted} unique calls added"
        if skipped > 0:
            message += f", {skipped} duplicates skipped"
        
        return UploadResponse(
            processed=total_records,
            unique_calls=inserted,
            skipped=skipped,
            message=message
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )
