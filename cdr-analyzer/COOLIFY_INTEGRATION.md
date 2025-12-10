# Coolify Integration Guide

## Overview

This guide explains how to deploy and manage the CDR Analyzer in a Coolify environment for production use.

## What is Coolify?

Coolify is a modern hosting platform that simplifies Docker deployments. It provides:
- One-click deployments
- Automatic SSL/TLS certificates
- Built-in monitoring and logging
- Database backups
- Load balancing support

## Prerequisites

- Coolify instance running (v3.x or later)
- Access to Coolify dashboard
- Git repository with project code
- Docker knowledge (basic)

## Coolify Configuration

### Step 1: Create a New Service in Coolify

1. Log into Coolify dashboard
2. Navigate to **Services** → **New Service**
3. Select **Docker Compose**
4. Choose your Git repository

### Step 2: Configure Docker Compose

1. Set the Docker Compose file path: `cdr-analyzer/docker-compose.prod.coolify.yml`
2. Set the environment file: `cdr-analyzer/.env.production`
3. Configure resource limits (as per compose file)

### Step 3: Set Environment Variables

Create environment variables in Coolify:

```
ENVIRONMENT=production
DATABASE_PATH=/app/data/cdr.db
LOG_LEVEL=INFO
WORKERS=4
```

Or use the `.env.production` file approach (recommended).

### Step 4: Configure Volumes

The compose file uses bind mounts that should be created:

```bash
# On the Coolify server
sudo mkdir -p /data/cdr-analyzer/{cdr-data,logs,config}
sudo chown 1000:1000 /data/cdr-analyzer
sudo chmod 755 /data/cdr-analyzer
```

### Step 5: Deploy

1. Click **Deploy** in Coolify UI
2. Monitor deployment progress
3. Verify service is healthy

## Monitoring in Coolify

### Health Checks

The compose file includes health checks:
- Endpoint: `http://localhost:8000/api/v1/calls`
- Interval: 30 seconds
- Timeout: 10 seconds
- Retries: 5

### Logs

Access logs in Coolify:
1. Dashboard → Service → Logs
2. Real-time streaming
3. JSON formatted for better parsing

### Metrics

Monitor in Coolify:
- CPU usage
- Memory usage
- Network I/O
- Container status

## Reverse Proxy Setup (Nginx in Coolify)

For production, configure a reverse proxy:

```nginx
upstream cdr-analyzer {
    server localhost:8000;
}

server {
    listen 80;
    server_name api.example.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.example.com;

    ssl_certificate /etc/ssl/certs/api.example.com.crt;
    ssl_certificate_key /etc/ssl/private/api.example.com.key;

    location / {
        proxy_pass http://cdr-analyzer;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

## Backup Strategy in Coolify

### Automatic Backups

Configure in Coolify dashboard:
1. Service → Settings → Backups
2. Set backup frequency (daily recommended)
3. Configure storage location
4. Enable versioning

### Manual Backup

```bash
# SSH into Coolify server
docker-compose -f docker-compose.prod.coolify.yml exec cdr-analyzer \
    tar -czf /app/data/backup-$(date +%Y%m%d).tar.gz /app/data/cdr.db
```

## Scaling in Coolify

### Vertical Scaling

1. Dashboard → Service → Settings
2. Update resource limits
3. Redeploy

### Horizontal Scaling

For multiple instances:
1. Create load balancer in Coolify
2. Deploy multiple service instances
3. Configure shared volume for data

Example with HAProxy:
```
frontend cdr-api
    bind *:80
    default_backend cdr-servers

backend cdr-servers
    balance roundrobin
    server cdr1 localhost:8001
    server cdr2 localhost:8002
    server cdr3 localhost:8003
```

## Troubleshooting in Coolify

### Service won't start

1. Check logs: Dashboard → Service → Logs
2. Verify environment variables are set
3. Check disk space: `df -h`
4. Review resource limits

### Health check failing

```bash
# SSH into server
curl -v http://localhost:8000/api/v1/calls
```

### High memory usage

1. Reduce WORKERS in environment
2. Check for memory leaks: `docker stats`
3. Increase memory limit if needed

### Database issues

```bash
# Check database integrity
docker-compose -f docker-compose.prod.coolify.yml exec cdr-analyzer \
    sqlite3 /app/data/cdr.db ".tables"
```

## Updates & Maintenance in Coolify

### Update Process

1. Push changes to git repository
2. Coolify auto-detects (if webhook configured)
3. Or manually trigger redeploy:
   - Dashboard → Service → Redeploy
4. Monitor deployment progress
5. Verify health checks pass

### Database Migrations

```bash
# Before deployment
docker-compose -f docker-compose.prod.coolify.yml exec cdr-analyzer \
    python /app/database.py migrate
```

## Security Considerations

### SSL/TLS

- Use Coolify's automatic SSL certificates (Let's Encrypt)
- Enable HTTPS only
- Set HSTS headers

### Network Security

- Use Coolify's firewall rules
- Restrict access to admin endpoints
- Enable IP whitelisting if needed

### Secret Management

Use Coolify's secret management:
1. Dashboard → Settings → Secrets
2. Set production secrets
3. Reference in environment

Example:
```yaml
environment:
  - API_KEY=${COOLIFY_SECRET_API_KEY}
  - DB_PASSWORD=${COOLIFY_SECRET_DB_PASSWORD}
```

## Performance Tuning

### Connection Pooling

In `.env.production`:
```
MAX_CONNECTIONS=100
CONNECTION_TIMEOUT=30
```

### Caching

- Enable browser caching for static content
- Use Redis for session storage (future enhancement)

### Database Optimization

- Regular VACUUM: `sqlite3 cdr.db VACUUM`
- Index frequently queried columns
- Monitor query performance

## Rollback Strategy

### Automatic Rollback

Configure in Coolify:
1. Service → Settings → Rollback Policy
2. Set to rollback on health check failure
3. Keep previous images for quick rollback

### Manual Rollback

```bash
# View available versions
docker images | grep cdr-analyzer

# Rollback to previous version
docker-compose -f docker-compose.prod.coolify.yml down
docker-compose -f docker-compose.prod.coolify.yml up -d
```

## Additional Resources

- Coolify Documentation: https://coolify.io/docs
- Docker Compose Reference: https://docs.docker.com/compose/compose-file
- SQLite Best Practices: https://www.sqlite.org/bestpractice.html
- CDR Analyzer Project: See main README.md

