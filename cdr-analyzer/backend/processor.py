"""
CDR File Processing Engine
Handles CSV parsing, grouping, and data extraction
"""
import pandas as pd
import re
from datetime import datetime
from typing import List, Dict, Tuple
from io import BytesIO

def parse_extension(channel: str) -> str:
    """
    Extract extension number from channel string
    Example: "SIP/209-000012ec" -> "209"
    """
    if not channel or pd.isna(channel):
        return None
    
    # Match pattern like SIP/209-... or PJSIP/209-...
    match = re.search(r'(?:SIP|PJSIP)/(\d+)', channel)
    if match:
        return match.group(1)
    return None

def parse_duration(duration_str) -> int:
    """
    Convert duration string to seconds
    Examples: "45s" -> 45, "2min 30s" -> 150, "145" -> 145
    """
    if pd.isna(duration_str):
        return 0
    
    duration_str = str(duration_str).strip()
    
    # If it's already a number
    if duration_str.isdigit():
        return int(duration_str)
    
    total_seconds = 0
    
    # Parse minutes
    min_match = re.search(r'(\d+)\s*min', duration_str)
    if min_match:
        total_seconds += int(min_match.group(1)) * 60
    
    # Parse seconds
    sec_match = re.search(r'(\d+)\s*s', duration_str)
    if sec_match:
        total_seconds += int(sec_match.group(1))
    
    return total_seconds

def normalize_timestamp(date_str) -> str:
    """
    Normalize various date formats to ISO 8601
    """
    if pd.isna(date_str):
        return None
    
    date_str = str(date_str).strip()
    
    # Common formats from CDR systems
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%d/%m/%Y %H:%M:%S",
        "%m/%d/%Y %H:%M:%S",
        "%Y/%m/%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.isoformat()
        except ValueError:
            continue
    
    # If all formats fail, return original
    return date_str

def process_cdr_file(file_content: bytes) -> Tuple[List[Dict], int, int]:
    """
    Process CDR CSV file and extract unique calls
    
    Returns:
        (processed_records, total_records_in_file, unique_calls)
    """
    try:
        # Read CSV with pandas
        df = pd.read_csv(BytesIO(file_content))
        
        total_records = len(df)
        
        # Validate required columns
        required_columns = ['UniqueID', 'Source', 'Date', 'Status', 'Duration']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            # Try case-insensitive match
            df.columns = df.columns.str.strip()
            column_map = {}
            for req_col in required_columns:
                for df_col in df.columns:
                    if df_col.lower() == req_col.lower():
                        column_map[df_col] = req_col
                        break
            
            if column_map:
                df.rename(columns=column_map, inplace=True)
            
            # Check again
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"CSV file missing required columns: {', '.join(missing_columns)}")
        
        # Optional column for destination channel
        dst_channel_col = None
        for col in df.columns:
            if 'dst' in col.lower() and 'channel' in col.lower():
                dst_channel_col = col
                break
        
        # Group by UniqueID
        grouped = df.groupby('UniqueID')
        
        processed_records = []
        
        for unique_id, group in grouped:
            # Skip if unique_id is null
            if pd.isna(unique_id):
                continue
            
            # Get first record for caller info
            first_record = group.iloc[0]
            # Convert caller number and remove .0 suffix if it's a float
            if not pd.isna(first_record['Source']):
                caller_number = str(first_record['Source']).strip()
                # Remove .0 suffix from float representation
                if caller_number.endswith('.0'):
                    caller_number = caller_number[:-2]
            else:
                caller_number = None
            timestamp = normalize_timestamp(first_record['Date'])
            
            if not timestamp:
                continue  # Skip records with invalid dates
            
            # Determine call status
            # A call is ANSWERED if any record has status=ANSWERED and duration > 0
            answered_records = group[
                (group['Status'].str.upper() == 'ANSWERED') & 
                (group['Duration'].notna())
            ]
            
            status = 'MISSED'
            extension = None
            duration = 0
            
            if not answered_records.empty:
                # Parse durations and find record with max duration
                answered_records = answered_records.copy()
                answered_records['duration_sec'] = answered_records['Duration'].apply(parse_duration)
                
                # Filter out zero duration
                answered_records = answered_records[answered_records['duration_sec'] > 0]
                
                if not answered_records.empty:
                    status = 'ANSWERED'
                    
                    # Get record with longest duration
                    max_duration_record = answered_records.loc[answered_records['duration_sec'].idxmax()]
                    duration = int(max_duration_record['duration_sec'])
                    
                    # Extract extension from destination channel
                    if dst_channel_col and dst_channel_col in max_duration_record.index:
                        extension = parse_extension(max_duration_record[dst_channel_col])
            
            # Create call record
            call_record = {
                'unique_id': str(unique_id),
                'timestamp': timestamp,
                'caller_number': caller_number,
                'extension': extension,
                'status': status,
                'duration': duration
            }
            
            processed_records.append(call_record)
        
        return processed_records, total_records, len(processed_records)
    
    except Exception as e:
        raise ValueError(f"Error processing CSV file: {str(e)}")
