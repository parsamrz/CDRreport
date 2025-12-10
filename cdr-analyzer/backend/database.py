"""
Database configuration and schema for SQLite
"""
import sqlite3
from contextlib import contextmanager
from typing import Generator
import os

DATABASE_PATH = "cdr.db"

def get_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn

@contextmanager
def get_db() -> Generator[sqlite3.Connection, None, None]:
    """Context manager for database connections"""
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def init_db():
    """Initialize database schema"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Create call_records table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS call_records (
                unique_id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                caller_number TEXT,
                extension TEXT,
                status TEXT CHECK(status IN ('ANSWERED', 'MISSED')) NOT NULL,
                duration INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create indexes for performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_timestamp 
            ON call_records(timestamp)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_status 
            ON call_records(status)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_caller_number 
            ON call_records(caller_number)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_extension 
            ON call_records(extension)
        """)
        
        conn.commit()
        print("✅ Database initialized successfully")

def insert_call_record(conn: sqlite3.Connection, record: dict) -> bool:
    """
    Insert a call record into database
    Returns True if inserted, False if duplicate
    """
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO call_records 
            (unique_id, timestamp, caller_number, extension, status, duration)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            record['unique_id'],
            record['timestamp'],
            record['caller_number'],
            record['extension'],
            record['status'],
            record['duration']
        ))
        return True
    except sqlite3.IntegrityError:
        # Duplicate unique_id
        return False

def get_calls(conn: sqlite3.Connection, 
              page: int = 1, 
              limit: int = 50,
              from_date: str = None,
              to_date: str = None,
              search: str = None) -> tuple:
    """
    Get paginated list of calls with optional filters
    Returns (calls, total_count)
    """
    cursor = conn.cursor()
    
    # Build WHERE clause
    where_clauses = []
    params = []
    
    if from_date:
        where_clauses.append("timestamp >= ?")
        params.append(from_date)
    
    if to_date:
        where_clauses.append("timestamp <= ?")
        params.append(to_date)
    
    if search:
        where_clauses.append("caller_number LIKE ?")
        params.append(f"%{search}%")
    
    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
    
    # Get total count
    cursor.execute(f"SELECT COUNT(*) FROM call_records WHERE {where_sql}", params)
    total = cursor.fetchone()[0]
    
    # Get paginated results
    offset = (page - 1) * limit
    query_params = params + [limit, offset]
    
    cursor.execute(f"""
        SELECT unique_id, timestamp, caller_number, extension, status, duration
        FROM call_records
        WHERE {where_sql}
        ORDER BY timestamp DESC
        LIMIT ? OFFSET ?
    """, query_params)
    
    calls = [dict(row) for row in cursor.fetchall()]
    
    return calls, total
