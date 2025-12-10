# Design Document: CDR Analyzer Dashboard

## Context

Phone systems (Issabel/Asterisk) generate highly verbose CDR (Call Detail Record) logs where a single call creates 10-15 database entries representing internal routing, ringing extensions, transfers, and busy signals. Business managers need clean, actionable data showing actual call counts and staff performance without technical noise.

**Stakeholders:**
- Office managers (non-technical users)
- System administrators (upload CSV files weekly)

**Constraints:**
- No direct connection to PBX (file-based only)
- Must support Jalali calendar (Persian business context)
- Single-user desktop deployment initially
- Files contain 500-10,000 records each

## Goals / Non-Goals

**Goals:**
- Aggregate raw CDR records into single call entries
- Provide accurate "answered" vs "missed" call classification
- Display data with Jalali dates throughout UI
- Enable search and filtering by date range and phone number
- Process typical files (10k records) in under 5 seconds

**Non-Goals:**
- Real-time AMI/SIP integration with PBX
- Multi-user authentication system (v1.0)
- PDF/Excel export (focus on dashboard visualization)
- Manual record editing by users
- Multi-tenant support

## Decisions

### 1. UniqueID as Aggregation Key
**Decision:** Use the `UniqueID` column from CDR CSV as the primary grouping key.

**Rationale:** Analysis of sample data shows all records for a single call share the same `UniqueID` (e.g., `1765268086.31589`). This is a reliable, system-generated identifier.

**Alternatives considered:**
- Group by timestamp + caller number: Too fragile (multiple calls from same number)
- Sequential record analysis: Complex state machine, error-prone

### 2. Call Status Algorithm
**Decision:** A call is "ANSWERED" if ANY record in the UniqueID group has `status=ANSWERED` AND `duration > 0`.

**Rationale:** 
- Transfers and multi-ring scenarios create multiple ANSWERED records
- Duration > 0 filters out false positives (immediate hangups)
- Simple boolean logic, easy to test and explain

**Edge cases:**
- Transferred calls: Use extension with longest duration
- Abandoned in queue: Correctly classified as MISSED (no duration)

### 3. Database Choice: SQLite
**Decision:** Use SQLite with UniqueID as primary key.

**Rationale:**
- Single-file portability for desktop deployment
- Built-in deduplication via primary key constraint
- No server setup required
- Sufficient performance for <100k records

**Alternatives:**
- PostgreSQL: Overkill for single-user scenario
- In-memory only: Loses data between sessions

### 4. Date Storage Strategy
**Decision:** Store all dates as ISO 8601 strings in database, convert to Jalali only in presentation layer.

**Rationale:**
- ISO format ensures sorting and filtering work correctly
- Separation of concerns (storage vs display)
- Enables future multi-locale support

**Implementation:**
- Backend stores: `"2024-12-09T14:30:00"`
- Frontend displays: `"۱۴۰۳/۰۹/۱۹ - ۱۴:۳۰"`

### 5. Technology Stack
**Decision:** FastAPI + Vanilla JS + Tailwind CSS

**Rationale:**
- FastAPI: Modern async Python, auto-docs, fast development
- Vanilla JS: No build step, simple deployment
- Tailwind CSS: Rapid responsive UI without custom CSS

**Alternatives:**
- Django: Too heavy for simple file processing
- React/Vue: Unnecessary complexity for single-page dashboard

### 6. Data Processing Library
**Decision:** Use Pandas for CSV parsing and grouping.

**Rationale:**
- Built-in CSV handling with encoding detection
- Efficient groupby operations for UniqueID aggregation
- Widely tested and documented

**Trade-off:** ~100MB memory overhead, acceptable for desktop use

## Data Model

```python
class CallRecord(BaseModel):
    unique_id: str      # Primary key, from UniqueID column
    timestamp: datetime # ISO format, from Date column
    caller_number: str  # From Source column (first record in group)
    extension: str      # From Dst.Channel, extract "209" from "SIP/209-000012ec"
    status: str         # "ANSWERED" or "MISSED"
    duration: int       # Seconds, from Duration column
```

**Database Schema:**
```sql
CREATE TABLE call_records (
    unique_id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    caller_number TEXT,
    extension TEXT,
    status TEXT CHECK(status IN ('ANSWERED', 'MISSED')),
    duration INTEGER DEFAULT 0
);
CREATE INDEX idx_timestamp ON call_records(timestamp);
CREATE INDEX idx_status ON call_records(status);
```

## API Design

```
POST   /api/v1/upload
       Body: multipart/form-data (CSV file)
       Returns: {"processed": 500, "unique_calls": 45}

GET    /api/v1/calls?page=1&limit=50&from=2024-12-01&to=2024-12-31
       Returns: {"calls": [...], "total": 120}

GET    /api/v1/calls/search?phone=0912
       Returns: {"calls": [...]}

GET    /api/v1/stats/daily?from=2024-12-01&to=2024-12-31
       Returns: {"dates": [...], "answered": [...], "missed": [...]}

GET    /api/v1/stats/extensions
       Returns: {"extensions": ["209", "210"], "counts": [45, 32]}
```

## Risks / Trade-offs

### Risk: CSV Format Changes
**Impact:** If PBX changes column names or order, parser breaks.

**Mitigation:**
- Make parser configurable with column mapping
- Add validation step that checks required columns exist
- Log clear error message pointing to format mismatch

### Risk: Complex Transfer Scenarios
**Impact:** Multi-hop transfers might attribute call to wrong extension.

**Mitigation:**
- Document "longest duration" heuristic clearly
- Add future enhancement: show transfer chain in call details
- Acceptable for v1.0 - captures 95% of cases correctly

### Risk: Large Files (>50k records)
**Impact:** Memory usage spikes, UI freezes during processing.

**Mitigation:**
- Implement chunked CSV reading with progress updates
- Add file size validation (reject >10MB files)
- Show loading indicator during processing

### Risk: Date Conversion Errors
**Impact:** Edge cases around leap years, calendar boundaries.

**Mitigation:**
- Use well-tested Jalali library (jdatetime or similar)
- Add comprehensive unit tests for date boundaries
- Always store original timestamp for audit trail

## Migration Plan

N/A - This is a greenfield project. No existing system to migrate from.

## Performance Targets

| Metric | Target | Rationale |
|--------|--------|-----------|
| File processing | <5s for 10k records | User perception threshold |
| Dashboard load | <2s | Standard web performance |
| Search latency | <500ms | Interactive feel |
| Database size | <100MB per 100k calls | Manageable on desktop |

## Security Considerations

- **File upload**: Validate CSV format, limit file size to 10MB
- **SQL injection**: Use parameterized queries (SQLAlchemy ORM)
- **Path traversal**: Validate uploaded filenames
- **No authentication in v1.0**: Document that this is internal-network only

## Open Questions

1. Should we support multiple file formats (XLS, JSON) in future?
   - *Decision: Defer to v2.0, focus on CSV for MVP*

2. Do we need audit log of who uploaded which file?
   - *Decision: Not in v1.0 (no auth system yet)*

3. Should dashboard auto-refresh if new file uploaded?
   - *Decision: Manual refresh acceptable for weekly upload pattern*
