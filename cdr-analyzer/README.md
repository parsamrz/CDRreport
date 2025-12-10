# CDR Analyzer Dashboard

A web application for analyzing Call Detail Records (CDR) from phone systems like Issabel and Asterisk.

## Features

- 📤 Upload CDR CSV files
- 🔄 Automatic data deduplication and aggregation
- 📊 Interactive dashboard with charts
- 📅 Jalali (Persian/Shamsi) calendar support
- 🔍 Search and filter capabilities
- 📱 Responsive design for mobile and desktop

## Architecture

- **Backend**: FastAPI (Python 3.10+)
- **Database**: SQLite
- **Frontend**: HTML5, Vanilla JavaScript, Tailwind CSS
- **Charts**: Chart.js
- **Date**: Jalali/Persian calendar support

## Installation

### Backend Setup

```bash
cd cdr-analyzer/backend
pip install -r requirements.txt
python main.py
```

The API will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

### Frontend Setup

Simply open `frontend/index.html` in a web browser, or serve it with a simple HTTP server:

```bash
cd cdr-analyzer/frontend
python -m http.server 8080
```

Then navigate to `http://localhost:8080`

## Usage

1. **Upload CSV File**: Click "آپلود" and select your CDR CSV file
2. **View Dashboard**: Statistics and charts update automatically
3. **Filter by Date**: Use Jalali date picker to select date range
4. **Search Calls**: Enter phone number to search specific calls

## CSV Format

Required columns:
- `UniqueID`: Unique identifier for call grouping
- `Source`: Caller phone number
- `Date`: Call timestamp
- `Status`: Call status (ANSWERED/MISSED)
- `Duration`: Call duration
- `Dst.Channel` (optional): Destination channel for extension extraction

## API Endpoints

- `POST /api/v1/upload` - Upload CSV file
- `GET /api/v1/calls` - List calls with pagination
- `GET /api/v1/calls/search` - Search by phone number
- `GET /api/v1/stats/daily` - Daily statistics
- `GET /api/v1/stats/extensions` - Extension performance

## Performance

- Processes 10,000 records in under 5 seconds
- Dashboard loads in under 2 seconds
- Search results appear within 500ms

## License

Internal use only
