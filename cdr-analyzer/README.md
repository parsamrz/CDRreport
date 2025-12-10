# CDR Analyzer

A unified FastAPI application for analyzing Call Detail Records (CDR) from telephony systems.

![Version](https://img.shields.io/badge/version-2.0-blue)
![Status](https://img.shields.io/badge/status-production%20ready-green)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 🎯 Features

### Web Interface
- ✅ **Upload CDR Files** - Drag & drop CSV upload
- ✅ **Real-time Statistics** - View call metrics instantly
- ✅ **Interactive Charts** - Daily trends and performance
- ✅ **Advanced Filtering** - Date range & phone search
- ✅ **Persian Support** - VazirMatn font & Jalali calendar
- ✅ **Database Management** - Clear data with safety confirmations

### Call Processing
- ✅ **Smart Filtering** - Only counts incoming calls
- ✅ **Multi-format Support** - Mobile, landline, international
- ✅ **Duplicate Handling** - Groups by UniqueID
- ✅ **Auto-detection** - Identifies call direction automatically

### Architecture
- ✅ **Unified Service** - Single FastAPI application
- ✅ **REST API** - Full API with documentation
- ✅ **Template Engine** - Jinja2 for dynamic pages
- ✅ **SQLite Database** - Lightweight and portable
- ✅ **Docker Support** - Production-ready containers

---

## 🚀 Quick Start

### Method 1: Local Development

```bash
# Navigate to backend
cd cdr-analyzer/backend

# Install dependencies
pip install -r requirements.txt

# Start server
python main.py
```

### Method 2: Docker (Recommended)

```bash
# Navigate to project root
cd cdr-analyzer

# Start with Docker Compose
docker-compose up -d
```

### Access the Application

```
http://localhost:8000
```

---

## 📊 Supported Phone Formats

| Type | Format | Example | Count Mode |
|------|--------|---------|------------|
| **Mobile (National)** | 9XXXXXXXXX | 9121234567, 09121234567 | ✅ Counted |
| **Mobile (International)** | 98XXXXXXXXXX | +989121234567, 989121234567 | ✅ Counted |
| **Landline** | 0XXXXXXXXX | 01144514792, 044367838 | ✅ Counted |
| **Extensions** | XXX | 101, 102, 110 | ❌ Filtered (outgoing) |

---

## 🔌 API Endpoints

### Web Interface
- `GET /` - Main dashboard

### Call Management
- `POST /api/v1/upload` - Upload CDR file
- `GET /api/v1/calls` - List calls (paginated)
- `GET /api/v1/calls/search?phone={number}` - Search calls

### Statistics
- `GET /api/v1/stats` - Get call statistics

### Administration
- `DELETE /api/v1/clear-database` - Clear all data

### Documentation
- `GET /docs` - Swagger UI (interactive API docs)
- `GET /redoc` - ReDoc (alternative API docs)

---

## 🐳 Docker Deployment

### Development

```bash
cd cdr-analyzer
docker-compose up -d
```

### Production

```bash
cd cdr-analyzer
docker-compose -f docker-compose.prod.yml up -d
```

### Docker Commands

```bash
# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart
docker-compose restart
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **QUICK_START.md** | Get started in 3 steps |
| **DOCKER_GUIDE.md** | Complete Docker deployment guide |
| **DOCKER_DEPLOYMENT_SUMMARY.md** | Docker changes summary |
| **FASTAPI_INTEGRATION_GUIDE.md** | Technical architecture details |
| **INTEGRATION_SUMMARY.md** | FastAPI + Jinja2 integration |
| **FEATURE_VAZIRMATN_AND_CLEAR_DB.md** | New features documentation |
| **COMPLETE_SOLUTION_REPORT.md** | Full project report |

---

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_PATH` | `data/cdr.db` | SQLite database location |
| `HOST` | `0.0.0.0` | Server host |
| `PORT` | `8000` | Server port |

---

## 🚧 Troubleshooting

### Port Already in Use

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Module Not Found

```bash
pip install -r requirements.txt
```

### Docker Issues

```bash
# Rebuild containers
docker-compose build --no-cache
docker-compose up -d
```

---

## 🔄 Updates & Changelog

### Version 2.0 (Current)
- ✅ Unified FastAPI + Jinja2 service
- ✅ VazirMatn Persian font
- ✅ Clear database functionality
- ✅ Improved Docker setup (single service)
- ✅ Enhanced call filtering (mobile + landline + international)
- ✅ Production-ready Docker configuration

### Version 1.0
- Initial release
- Separate frontend/backend
- Basic call processing

---

## 📄 License

MIT License - See LICENSE file for details

---

## 📞 Support

For issues, questions, or suggestions:

- Check documentation in project root
- Review troubleshooting section
- Open an issue on GitHub

---

**Version:** 2.0  
**Last Updated:** December 9, 2024  
**Status:** Production Ready

---

**Quick Commands:**

```bash
# Local development
cd backend && python main.py

# Docker development
docker-compose up -d

# Docker production
docker-compose -f docker-compose.prod.yml up -d
```

**Access:** http://localhost:8000

🎉 **Enjoy analyzing your call records!**
