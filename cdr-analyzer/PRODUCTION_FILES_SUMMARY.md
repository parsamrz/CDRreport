# Production Deployment Files - Summary

This document lists all production-ready files created for Coolify deployment.

## Files Created

### 1. Docker Compose Configuration
- **File**: `docker-compose.prod.coolify.yml`
- **Purpose**: Production-ready Docker Compose configuration optimized for Coolify
- **Key Features**:
  - Bind mount volumes for persistent data
  - Resource limits (2 CPU, 2GB RAM)
  - Health checks configured
  - Logging configuration (JSON format)
  - Coolify labels for management
  - Production environment variables

### 2. Environment Configuration
- **File**: `.env.production`
- **Purpose**: Production environment variables
- **Contents**:
  - Core application settings
  - Database configuration
  - Security settings
  - Performance tuning parameters
  - Logging configuration
  - Resource limits

### 3. Deployment Documentation

#### Main Guides
- **File**: `COOLIFY_PRODUCTION_DEPLOYMENT.md`
  - Complete deployment guide for Coolify
  - Step-by-step instructions
  - Troubleshooting tips
  - Backup & recovery procedures
  - Maintenance tasks

- **File**: `COOLIFY_INTEGRATION.md`
  - Detailed Coolify platform integration guide
  - Monitoring and scaling instructions
  - Security best practices
  - Performance tuning
  - Rollback strategy

### 4. Deployment Scripts

#### Bash Script (Linux/Mac)
- **File**: `deploy-prod.sh`
- **Purpose**: Automate production deployment on Linux/macOS
- **Features**:
  - Docker daemon validation
  - Automatic backup creation
  - Git pull and build
  - Health check monitoring
  - Error handling

#### PowerShell Script (Windows)
- **File**: `deploy-prod.ps1`
- **Purpose**: Automate production deployment on Windows
- **Features**:
  - Same functionality as bash script
  - Windows-friendly paths
  - Optional parameters for customization

## Directory Structure for Production

```
Project Structure (Source Code):
CDRreport/ (project root)
└── cdr-analyzer/
    ├── backend/
    │   ├── Dockerfile          ← Build target
    │   ├── main.py
    │   ├── requirements.txt
    │   └── ...
    ├── frontend/
    ├── docker-compose.prod.coolify.yml  ← Build context: ./backend
    ├── .env.production
    └── ...

Production Server Data Directories:
/data/cdr-analyzer/
├── cdr-data/          # SQLite database volume
├── logs/              # Application logs
└── config/            # Configuration files

/backups/cdr-analyzer/
├── cdr.db.backup.*    # Database backups
└── logs-*.tar.gz      # Log archives
```

**Build Context**: The `docker-compose.prod.coolify.yml` uses `./backend` as the build context because:
- The compose file location: `cdr-analyzer/docker-compose.prod.coolify.yml`
- The Dockerfile location: `cdr-analyzer/backend/Dockerfile`
- Relative path: `./backend`

## Quick Start for Production

### On Linux/macOS:
```bash
cd cdr-analyzer
chmod +x deploy-prod.sh
./deploy-prod.sh
```

### On Windows:
```powershell
cd cdr-analyzer
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\deploy-prod.ps1
```

### Manual Deployment:
```bash
docker-compose -f docker-compose.prod.coolify.yml \
  --env-file .env.production up -d
```

## Production Checklist

Before deploying to production, ensure:

- [ ] Review and customize `.env.production`
- [ ] Create data directories: `/data/cdr-analyzer/{cdr-data,logs}`
- [ ] Configure reverse proxy (Nginx/Caddy)
- [ ] Set up SSL/TLS certificates
- [ ] Configure backup strategy
- [ ] Set up monitoring and alerts
- [ ] Test health checks
- [ ] Implement rate limiting
- [ ] Enable security headers
- [ ] Configure log aggregation
- [ ] Set up database backups
- [ ] Document deployment procedure

## Resource Requirements

- **Minimum**:
  - 2 CPU cores
  - 2GB RAM
  - 50GB disk space

- **Recommended**:
  - 4 CPU cores
  - 4GB RAM
  - 200GB+ disk space (for high-volume CDR processing)

## Coolify-Specific Features Used

1. **Bind Mounts**: Direct mounting of production directories
2. **Health Checks**: Built-in service availability monitoring
3. **Resource Limits**: CPU and memory constraints
4. **Logging**: JSON-formatted logs with rotation
5. **Labels**: Service identification and tracking
6. **Networks**: Isolated network for services

## Environment Variables Explained

| Variable | Purpose | Default |
|----------|---------|---------|
| `ENVIRONMENT` | Application environment | `production` |
| `DATABASE_PATH` | SQLite database location | `/app/data/cdr.db` |
| `PYTHONUNBUFFERED` | Python logging mode | `1` |
| `WORKERS` | Gunicorn worker processes | `4` |
| `WORKER_TIMEOUT` | Worker timeout in seconds | `120` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `LOG_FILE` | Log file location | `/app/logs/cdr-analyzer.log` |

## Monitoring & Alerts

### Health Check Endpoint
- **URL**: `http://localhost:8000/api/v1/calls`
- **Interval**: 30 seconds
- **Timeout**: 10 seconds
- **Max Retries**: 5

### Log Locations
- Application logs: `/data/cdr-analyzer/logs/cdr-analyzer.log`
- Container logs: `docker-compose logs cdr-analyzer`

### Metrics to Monitor
- CPU usage (target: <50%)
- Memory usage (target: <75%)
- Disk usage (alert: >90%)
- API response time (target: <500ms)
- Error rate (target: <0.1%)

## Support & References

- **Coolify Docs**: https://coolify.io/docs
- **Docker Compose**: https://docs.docker.com/compose
- **Project README**: See parent directory
- **Architecture**: See architecture.md
- **Design Guidelines**: See design-guidelines.md

## Version Information

- Created: December 10, 2025
- Docker Compose Version: 3.8
- Coolify Target: v3.x and above
- Python Version: 3.8+

