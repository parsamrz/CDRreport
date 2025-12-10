# Change: Add CDR Analyzer Dashboard

## Why

Call Detail Record (CDR) files from phone systems (Issabel/Asterisk) are raw and contain 10-15 records per single actual call, making it impossible for managers to understand basic metrics like "how many real calls did we receive today" or "which receptionist answered the most calls". This creates a critical business intelligence gap.

## What Changes

- **NEW**: CDR file upload and processing system with CSV parsing
- **NEW**: Data deduplication and aggregation engine (groups by UniqueID)
- **NEW**: SQLite database for storing cleaned call records
- **NEW**: Dashboard with charts showing call trends and extension performance
- **NEW**: Jalali (Persian/Shamsi) date filtering and display
- **NEW**: Call search functionality by phone number
- **NEW**: RESTful API backend using FastAPI
- **NEW**: Responsive frontend using Tailwind CSS

This is a completely new capability - no breaking changes to existing systems.

## Impact

- **Affected specs**: Creates new capability `cdr-analyzer`
- **Affected code**: 
  - New backend service with FastAPI
  - New frontend SPA
  - New SQLite database schema
  - Data processing module using Pandas
- **Dependencies**: Python 3.10+, FastAPI, Pandas, SQLite, Tailwind CSS
- **Performance**: Must process 10,000 records within 5 seconds
- **Localization**: Full Jalali calendar support required
