#!/bin/bash

# CDR Analyzer - Production Deployment Script for Coolify
# This script automates the deployment process

set -e

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
COMPOSE_FILE="docker-compose.prod.coolify.yml"
ENV_FILE=".env.production"
BACKUP_DIR="/backups/cdr-analyzer"
DATA_DIR="/data/cdr-analyzer"

echo -e "${YELLOW}=== CDR Analyzer Production Deployment ===${NC}"

# Function to log messages
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# Check if Docker is running
log_info "Checking Docker daemon..."
docker info > /dev/null 2>&1 || log_error "Docker daemon is not running"
log_info "Docker is running"

# Check if Docker Compose file exists
if [ ! -f "$COMPOSE_FILE" ]; then
    log_error "Docker Compose file not found: $COMPOSE_FILE"
fi
log_info "Docker Compose file found: $COMPOSE_FILE"

# Check if .env.production exists
if [ ! -f "$ENV_FILE" ]; then
    log_warn ".env.production not found. Creating from template..."
    cp .env.production.example "$ENV_FILE" 2>/dev/null || log_error ".env.production.example not found"
    log_warn "Please edit $ENV_FILE with your production settings"
fi

# Create necessary directories
log_info "Creating data directories..."
mkdir -p "$DATA_DIR"/{cdr-data,logs,config}
chmod 755 "$DATA_DIR"

# Create backup
log_info "Creating backup..."
mkdir -p "$BACKUP_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

if docker-compose -f "$COMPOSE_FILE" ps | grep -q cdr-analyzer; then
    log_info "Backing up existing database..."
    docker-compose -f "$COMPOSE_FILE" exec -T cdr-analyzer \
        cp /app/data/cdr.db /app/data/cdr.db.backup.$TIMESTAMP || log_warn "Could not backup database"

    log_info "Stopping existing container..."
    docker-compose -f "$COMPOSE_FILE" down
fi

# Pull latest changes (if in git repo)
if [ -d ".git" ]; then
    log_info "Pulling latest changes from git..."
    git pull origin main || log_warn "Could not pull from git"
fi

# Build image
log_info "Building Docker image..."
docker-compose -f "$COMPOSE_FILE" build --no-cache || log_error "Failed to build Docker image"

# Start services
log_info "Starting services..."
docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" up -d || log_error "Failed to start services"

# Wait for service to be healthy
log_info "Waiting for service to be healthy..."
MAX_ATTEMPTS=30
ATTEMPT=0

while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
    if docker-compose -f "$COMPOSE_FILE" ps | grep -q "healthy"; then
        log_info "Service is healthy"
        break
    fi

    if [ $ATTEMPT -eq 0 ]; then
        log_info "Waiting for health check..."
    fi

    ATTEMPT=$((ATTEMPT + 1))
    sleep 2
done

if [ $ATTEMPT -eq $MAX_ATTEMPTS ]; then
    log_warn "Service did not become healthy after $MAX_ATTEMPTS attempts"
    log_info "Checking logs..."
    docker-compose -f "$COMPOSE_FILE" logs cdr-analyzer | tail -20
else
    log_info "Service is running and healthy"
fi

# Display status
log_info "Deployment complete!"
log_info ""
log_info "Service Status:"
docker-compose -f "$COMPOSE_FILE" ps

log_info ""
log_info "Test the service:"
log_info "  curl http://localhost:8000/api/v1/calls"
log_info ""
log_info "View logs:"
log_info "  docker-compose -f $COMPOSE_FILE logs -f cdr-analyzer"
log_info ""
log_info "Stop the service:"
log_info "  docker-compose -f $COMPOSE_FILE down"

