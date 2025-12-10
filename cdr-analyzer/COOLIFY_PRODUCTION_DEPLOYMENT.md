# CDR Analyzer - Production Deployment with Coolify

## Overview

This guide provides step-by-step instructions for deploying the CDR Analyzer to production using Coolify and Docker Compose.

## Prerequisites

- Coolify installed and running
- Docker and Docker Compose installed on the production server
- At least 4GB RAM and 2 CPU cores
- 50GB disk space for CDR data

## Directory Structure

```
Project Root (CDRreport/)
├── cdr-analyzer/               # This directory (contains docker-compose)
│   ├── backend/                # Backend source code
│   │   ├── Dockerfile          # Backend container image
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   └── ...
│   ├── frontend/
│   ├── docker-compose.prod.coolify.yml
│   ├── .env.production
│   └── ...
└── ...

Production Server Data Directories:
/data/cdr-analyzer/
├── cdr-data/          # Persistent database volume
├── logs/              # Application logs
└── config/            # Configuration files
```

**Important**: The `docker-compose.prod.coolify.yml` file is located in the `cdr-analyzer/` directory and uses `./backend` as the build context to correctly reference the backend source code.

## Deployment Steps

### 1. Prepare the Production Server

```bash
# Create necessary directories with proper permissions
sudo mkdir -p /data/cdr-analyzer/{cdr-data,logs,config}
sudo chown -R 1000:1000 /data/cdr-analyzer/
sudo chmod -R 755 /data/cdr-analyzer/
```

### 2. Configure Environment Variables

Create `.env.production` in the `cdr-analyzer` directory:

```bash
cp .env.production.example .env.production
# Edit .env.production with your production values
nano .env.production
```

### 3. Deploy with Coolify

#### Option A: Using Coolify UI

1. Log into Coolify dashboard
2. Create a new service
3. Select "Docker Compose"
4. Upload `docker-compose.prod.coolify.yml`
5. Set environment file to `.env.production`
6. Deploy

#### Option B: Using Docker Compose CLI

```bash
cd /path/to/cdr-analyzer
docker-compose -f docker-compose.prod.coolify.yml --env-file .env.production up -d
```

### 4. Verify Deployment

```bash
# Check container status
docker-compose -f docker-compose.prod.coolify.yml ps

# Check logs
docker-compose -f docker-compose.prod.coolify.yml logs -f cdr-analyzer

# Test health endpoint
curl http://localhost:8000/api/v1/calls
```

## Production Best Practices

### Security

- [ ] Use HTTPS/TLS with reverse proxy (Nginx/Caddy)
- [ ] Implement rate limiting
- [ ] Enable authentication/authorization
- [ ] Use secrets management (Coolify Secrets)
- [ ] Regular security updates

### Monitoring

- [ ] Set up log aggregation (ELK, Loki)
- [ ] Configure alerts for failed health checks
- [ ] Monitor CPU and memory usage
- [ ] Track API response times

### Backup & Recovery

```bash
# Backup database
docker-compose -f docker-compose.prod.coolify.yml exec cdr-analyzer \
  cp /app/data/cdr.db /app/data/cdr.db.backup.$(date +%Y%m%d)

# Backup logs
tar -czf /backups/cdr-analyzer-logs-$(date +%Y%m%d).tar.gz /data/cdr-analyzer/logs/
```

### Scaling

For horizontal scaling:
- Use load balancer (HAProxy, Nginx)
- Deploy multiple instances
- Use shared storage for data
- Implement database replication

## Coolify-Specific Configuration

### Volume Mounting

The `docker-compose.prod.coolify.yml` uses bind mounts for better integration with Coolify:

```yaml
volumes:
  cdr-data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /data/cdr-analyzer/cdr-data
```

### Labels for Coolify

Coolify-managed services are labeled for better tracking:

```yaml
labels:
  - "coolify.managed=true"
  - "service=cdr-analyzer"
  - "environment=production"
```

### Resource Management

- **CPU Limit**: 2 cores (adjust based on workload)
- **Memory Limit**: 2GB (adjust based on data volume)
- **Reserved Resources**: 1 CPU core, 1GB memory

## Troubleshooting

### Container fails to start

```bash
docker-compose -f docker-compose.prod.coolify.yml logs cdr-analyzer
```

### Health check failing

```bash
docker-compose -f docker-compose.prod.coolify.yml exec cdr-analyzer \
  curl -v http://localhost:8000/api/v1/calls
```

### High memory usage

1. Check active sessions: `docker stats`
2. Reduce `WORKERS` in `.env.production`
3. Increase memory limit if data volume is large

### Database locked

```bash
# Restart the container
docker-compose -f docker-compose.prod.coolify.yml restart cdr-analyzer
```

## Maintenance

### Regular Tasks

- **Daily**: Monitor logs and health status
- **Weekly**: Review resource usage and performance metrics
- **Monthly**: Backup database and logs
- **Quarterly**: Security updates and dependency updates

### Updating the Application

```bash
cd /path/to/cdr-analyzer

# Pull latest changes
git pull origin main

# Rebuild image
docker-compose -f docker-compose.prod.coolify.yml build --no-cache

# Redeploy
docker-compose -f docker-compose.prod.coolify.yml up -d
```

## Support & Documentation

- Coolify Docs: https://coolify.io/docs
- Docker Compose Docs: https://docs.docker.com/compose
- Project Repo: See README.md in project root

