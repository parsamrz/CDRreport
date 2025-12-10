# CDR Analyzer Specification

## ADDED Requirements

### Requirement: CSV File Upload
The system SHALL accept CSV file uploads containing raw Call Detail Records from phone systems.

#### Scenario: Valid CSV upload
- **WHEN** user uploads a valid CDR CSV file under 10MB
- **THEN** the system SHALL process the file and return the count of records processed and unique calls identified

#### Scenario: Invalid file format
- **WHEN** user uploads a non-CSV file
- **THEN** the system SHALL reject the file with error message "Invalid file format. Only CSV files are accepted."

#### Scenario: File too large
- **WHEN** user uploads a file larger than 10MB
- **THEN** the system SHALL reject the file with error message "File size exceeds limit of 10MB."

### Requirement: UniqueID Grouping
The system SHALL group all CSV records by the `UniqueID` column to identify individual calls.

#### Scenario: Multiple records same UniqueID
- **WHEN** processing CSV with 10 records sharing UniqueID "1765268086.31589"
- **THEN** the system SHALL treat these as a single call and create one database entry

#### Scenario: Unique records
- **WHEN** processing CSV where each record has different UniqueID
- **THEN** the system SHALL create separate database entries for each

### Requirement: Call Status Detection
The system SHALL determine call status as ANSWERED or MISSED based on record analysis.

#### Scenario: Answered call detection
- **WHEN** any record in UniqueID group has status "ANSWERED" AND duration > 0
- **THEN** the call SHALL be classified as "ANSWERED"

#### Scenario: Missed call detection
- **WHEN** no records in UniqueID group have status "ANSWERED" with duration > 0
- **THEN** the call SHALL be classified as "MISSED"

#### Scenario: Zero duration answered call
- **WHEN** a record has status "ANSWERED" but duration = 0
- **THEN** this SHALL NOT count as an answered call (classified as MISSED)

### Requirement: Call Information Extraction
The system SHALL extract caller number, extension, and duration from grouped records.

#### Scenario: Extract caller number
- **WHEN** processing a UniqueID group
- **THEN** the caller_number SHALL be taken from the Source column of the first record in the group

#### Scenario: Extract answering extension
- **WHEN** an answered call has multiple records
- **THEN** the extension SHALL be extracted from the Dst.Channel of the record with longest duration and status ANSWERED
- **AND** channel format "SIP/209-000012ec" SHALL be parsed to extension "209"

#### Scenario: Extract call duration
- **WHEN** processing call duration
- **THEN** the system SHALL convert duration strings (e.g., "45s", "2min 30s") to integer seconds
- **AND** store the maximum duration from all ANSWERED records in the group

### Requirement: Duplicate Prevention
The system SHALL prevent duplicate call records in the database.

#### Scenario: Upload same file twice
- **WHEN** user uploads a CSV file that contains UniqueIDs already in database
- **THEN** the system SHALL skip duplicate records
- **AND** report "X records skipped (already exist), Y new records added"

### Requirement: Call Records Storage
The system SHALL store cleaned call records in SQLite database with indexed fields.

#### Scenario: Database schema
- **WHEN** system initializes
- **THEN** it SHALL create table with columns: unique_id (PRIMARY KEY), timestamp, caller_number, extension, status, duration
- **AND** create indexes on timestamp and status fields

### Requirement: Dashboard Visualization
The system SHALL display call statistics in graphical dashboard format.

#### Scenario: Daily trend chart
- **WHEN** user views dashboard
- **THEN** a line chart SHALL display count of calls per day for the selected date range
- **AND** separate lines SHALL show ANSWERED vs MISSED calls

#### Scenario: Extension performance chart
- **WHEN** user views dashboard
- **THEN** a bar chart SHALL display call count per extension for the selected date range
- **AND** bars SHALL be sorted by call count descending

### Requirement: Jalali Date Filtering
The system SHALL support filtering by Jalali (Persian/Shamsi) calendar dates.

#### Scenario: Select Jalali date range
- **WHEN** user selects date range "1403/09/01" to "1403/09/30"
- **THEN** all dashboard charts and tables SHALL update to show only calls within that range
- **AND** dates SHALL be converted to Gregorian for database queries

#### Scenario: Default date range
- **WHEN** user first loads dashboard
- **THEN** the system SHALL default to showing last 7 days of data

### Requirement: Jalali Date Display
The system SHALL display all dates in Jalali format throughout the user interface.

#### Scenario: Convert stored dates to Jalali
- **WHEN** displaying any date to user
- **THEN** dates stored as ISO 8601 SHALL be converted to Jalali format "YYYY/MM/DD HH:MM"
- **AND** Persian numerals SHALL be used (۱۴۰۳/۰۹/۱۹)

### Requirement: Phone Number Search
The system SHALL enable searching calls by partial phone number match.

#### Scenario: Search by partial number
- **WHEN** user enters "0912" in search field
- **THEN** system SHALL return all calls where caller_number contains "0912"
- **AND** results SHALL update in real-time as user types

#### Scenario: Empty search
- **WHEN** search field is empty
- **THEN** system SHALL display all calls for the selected date range

### Requirement: Call List Pagination
The system SHALL paginate call lists with configurable page size.

#### Scenario: Navigate pages
- **WHEN** more than 50 calls exist in result set
- **THEN** system SHALL display first 50 calls with pagination controls
- **AND** user SHALL be able to navigate to next/previous pages

#### Scenario: Page size selection
- **WHEN** user changes page size dropdown
- **THEN** system SHALL update display to show selected number of records per page (25, 50, 100)

### Requirement: Performance Targets
The system SHALL meet defined performance benchmarks for file processing.

#### Scenario: Large file processing time
- **WHEN** processing a CSV file with 10,000 records
- **THEN** the system SHALL complete processing within 5 seconds

#### Scenario: Dashboard load time
- **WHEN** user navigates to dashboard
- **THEN** initial page load SHALL complete within 2 seconds

#### Scenario: Search responsiveness
- **WHEN** user performs phone number search
- **THEN** results SHALL appear within 500 milliseconds

### Requirement: Responsive Design
The system SHALL provide usable interface on desktop and mobile devices.

#### Scenario: Mobile layout
- **WHEN** viewing dashboard on screen width < 768px
- **THEN** charts SHALL stack vertically
- **AND** data table SHALL support horizontal scrolling
- **AND** all controls SHALL remain accessible

### Requirement: Error Handling
The system SHALL provide clear error messages for all failure scenarios.

#### Scenario: Malformed CSV
- **WHEN** CSV file is missing required columns (UniqueID, Source, Date, Status, Duration)
- **THEN** system SHALL return error "CSV file missing required columns: [list]"

#### Scenario: Date parsing error
- **WHEN** CSV contains invalid date format in Date column
- **THEN** system SHALL skip that record and log warning with row number

#### Scenario: Database connection failure
- **WHEN** SQLite database cannot be accessed
- **THEN** system SHALL display error "Database unavailable. Please contact administrator."

### Requirement: API Documentation
The system SHALL provide auto-generated API documentation.

#### Scenario: OpenAPI docs available
- **WHEN** user navigates to /docs endpoint
- **THEN** FastAPI SHALL serve interactive Swagger UI documentation
- **AND** all endpoints SHALL be documented with parameters and response schemas
