# CDR Analyzer Project

This repository contains the **CDR Analyzer Dashboard** - a comprehensive web application for analyzing Call Detail Records (CDR) from phone systems like Issabel and Asterisk.

## 🎯 Project Overview

The CDR Analyzer solves a critical business intelligence problem: phone systems generate 10-15 raw log entries per actual call, making it impossible for managers to understand basic metrics. This system aggregates those raw records into actionable insights with Persian/Jalali calendar support.

## 📁 Repository Structure

```
.
├── openspec/                          # OpenSpec project management
│   ├── AGENTS.md                      # AI collaboration guidelines
│   ├── rules.md                       # Development rules and workflow
│   ├── design-guidelines.md           # Technical conventions
│   ├── architechture.md               # System architecture
│   └── changes/                       # Active change proposals
│       └── add-cdr-analyzer-dashboard/
│           ├── proposal.md            # Change proposal
│           ├── tasks.md               # Implementation checklist (38/38 ✓)
│           ├── design.md              # Technical design decisions
│           └── specs/                 # Requirements specifications
│
├── cdr-analyzer/                      # CDR Analyzer Application
│   ├── backend/                       # FastAPI Backend
│   │   ├── main.py                    # Application entry point
│   │   ├── models.py                  # Pydantic data models
│   │   ├── database.py                # SQLite database layer
│   │   ├── processor.py               # CSV processing engine
│   │   ├── routes/                    # API endpoints
│   │   │   ├── upload.py              # File upload
│   │   │   ├── calls.py               # Call retrieval
│   │   │   └── stats.py               # Statistics
│   │   ├── tests/                     # Unit tests
│   │   ├── requirements.txt           # Python dependencies
│   │   └── verify_setup.py            # Setup verification
│   │
│   ├── frontend/                      # Web Frontend
│   │   ├── index.html                 # Main dashboard UI
│   │   └── app.js                     # JavaScript application
│   │
│   ├── README.md                      # Application documentation
│   ├── QUICKSTART.md                  # Quick start guide
│   ├── DEPLOYMENT.md                  # Production deployment guide
│   └── docker-compose.yml             # Docker configuration
│
└── prd/                               # Product Requirements
    └── prd1.1.md                      # Original PRD (Persian)
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Modern web browser

### Installation (5 minutes)

```bash
# 1. Install backend dependencies
cd cdr-analyzer/backend
pip install fastapi uvicorn pydantic pandas python-multipart

# 2. Verify setup
python verify_setup.py

# 3. Start backend
python main.py
```

Backend runs on `http://localhost:8000`

### Open Frontend

Simply open `cdr-analyzer/frontend/index.html` in your browser, or:

```bash
cd cdr-analyzer/frontend
python -m http.server 8080
```

Navigate to `http://localhost:8080`

### Test with Sample Data

Upload `backend/test_sample.csv` to see the system in action!

## ✨ Features

### Core Capabilities
- **📤 CSV File Upload** - Process raw CDR files (up to 10MB)
- **🔄 Smart Aggregation** - Groups 10-15 raw records into single call entries
- **📊 Interactive Dashboard** - Real-time charts and statistics
- **📅 Jalali Calendar** - Full Persian/Shamsi date support
- **🔍 Advanced Search** - Find calls by phone number
- **📱 Responsive Design** - Works on desktop and mobile

### Technical Highlights
- **Fast Processing** - 10,000 records in <5 seconds
- **Automatic Deduplication** - Prevents duplicate uploads
- **RESTful API** - Auto-generated documentation at `/docs`
- **Zero Configuration** - SQLite database auto-initializes
- **Comprehensive Tests** - 8/8 unit tests passing

## 📊 API Documentation

Once backend is running, visit: `http://localhost:8000/docs`

Interactive Swagger UI with all endpoints documented.

## 🧪 Testing

```bash
cd cdr-analyzer/backend
pip install pytest
pytest tests/ -v
```

All 8 tests passing ✅

## 📖 Documentation

- **[QUICKSTART.md](cdr-analyzer/QUICKSTART.md)** - Get started in 5 minutes
- **[DEPLOYMENT.md](cdr-analyzer/DEPLOYMENT.md)** - Production deployment guide
- **[OpenSpec Proposal](openspec/changes/add-cdr-analyzer-dashboard/proposal.md)** - Full technical specification

## 🏗️ Architecture

### Backend (Python/FastAPI)
- **Framework**: FastAPI for async REST API
- **Database**: SQLite with optimized indexes
- **Processing**: Pandas for CSV manipulation
- **Validation**: Pydantic for data models

### Frontend (HTML/JavaScript)
- **Styling**: Tailwind CSS (CDN)
- **Charts**: Chart.js for visualizations
- **Date**: jalaali-js + Persian DatePicker
- **Architecture**: Vanilla JS SPA (no build step)

### Data Flow
1. Upload CSV → 2. Parse & Group by UniqueID → 3. Detect Status → 4. Store in SQLite → 5. Serve via API → 6. Display in Dashboard

## 🔧 Development Workflow (OpenSpec)

This project follows the **OpenSpec** specification-driven development approach:

1. **Proposal Phase** - All changes start in `openspec/changes/`
2. **Specification** - Requirements defined with scenarios
3. **Implementation** - Code written to spec (38/38 tasks completed)
4. **Validation** - Tests ensure compliance
5. **Archive** - Completed changes moved to archive

See [openspec/AGENTS.md](openspec/AGENTS.md) for full workflow.

## 🛡️ Security Considerations

- File size limited to 10MB
- CSV format validation
- SQL injection prevented (parameterized queries)
- CORS configured for local development
- ⚠️ No authentication in v1.0 (internal network only)

## 📈 Performance

- **Processing**: 10,000 records in <5 seconds ✓
- **Dashboard Load**: <2 seconds ✓
- **Search**: <500ms response time ✓

## 🤝 Contributing

This project uses OpenSpec for change management:

1. Read `openspec/rules.md`
2. Create proposal in `openspec/changes/`
3. Get approval before implementing
4. Follow design guidelines
5. Write tests
6. Update documentation

## 📄 License

Internal use only

## 🎉 Status

**Current Version**: 1.0.0  
**Status**: ✅ Complete and Deployed  
**Last Updated**: 2024-12-10  
**Implementation**: 38/38 tasks completed  
**Tests**: 8/8 passing  

---

Built with ❤️ following Lich Architecture principles and OpenSpec workflow.
