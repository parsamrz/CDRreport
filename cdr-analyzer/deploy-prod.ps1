# CDR Analyzer - Production Deployment Script for Coolify (Windows)
# This script automates the deployment process on Windows

param(
    [switch]$SkipBackup = $false,
    [switch]$SkipGitPull = $false,
    [switch]$Force = $false
)

# Configuration
$COMPOSE_FILE = "docker-compose.prod.coolify.yml"
$ENV_FILE = ".env.production"
$BACKUP_DIR = "C:\backups\cdr-analyzer"
$DATA_DIR = "D:\cdr-analyzer"  # Adjust to your production drive
$PROJECT_ROOT = Get-Location

# Function to log messages
function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Green
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
    exit 1
}

function Write-Warn {
    param([string]$Message)
    Write-Host "[WARN] $Message" -ForegroundColor Yellow
}

Write-Host "=== CDR Analyzer Production Deployment (Windows) ===" -ForegroundColor Yellow
Write-Host ""

# Check if Docker is running
Write-Info "Checking Docker daemon..."
try {
    docker info > $null 2>&1
    Write-Info "Docker is running"
} catch {
    Write-Error "Docker daemon is not running"
}

# Check if Docker Compose file exists
if (-not (Test-Path $COMPOSE_FILE)) {
    Write-Error "Docker Compose file not found: $COMPOSE_FILE"
}
Write-Info "Docker Compose file found: $COMPOSE_FILE"

# Check if .env.production exists
if (-not (Test-Path $ENV_FILE)) {
    Write-Warn ".env.production not found. Creating from template..."
    if (Test-Path ".env.production.example") {
        Copy-Item ".env.production.example" $ENV_FILE
        Write-Warn "Please edit $ENV_FILE with your production settings"
    } else {
        Write-Error ".env.production.example not found"
    }
}

# Create necessary directories
Write-Info "Creating data directories..."
if (-not (Test-Path "$DATA_DIR\cdr-data")) {
    New-Item -ItemType Directory -Path "$DATA_DIR\cdr-data" -Force | Out-Null
}
if (-not (Test-Path "$DATA_DIR\logs")) {
    New-Item -ItemType Directory -Path "$DATA_DIR\logs" -Force | Out-Null
}
if (-not (Test-Path "$BACKUP_DIR")) {
    New-Item -ItemType Directory -Path "$BACKUP_DIR" -Force | Out-Null
}

# Create backup
if (-not $SkipBackup) {
    Write-Info "Creating backup..."
    $TIMESTAMP = Get-Date -Format "yyyyMMdd_HHmmss"

    $ContainerRunning = docker-compose -f $COMPOSE_FILE ps | Select-String "cdr-analyzer"
    if ($ContainerRunning) {
        Write-Info "Backing up existing database..."
        docker-compose -f $COMPOSE_FILE exec -T cdr-analyzer `
            cmd /c copy "C:\app\data\cdr.db" "C:\app\data\cdr.db.backup.$TIMESTAMP" | Out-Null

        Write-Info "Stopping existing container..."
        docker-compose -f $COMPOSE_FILE down
    }
}

# Pull latest changes (if in git repo)
if (-not $SkipGitPull) {
    if (Test-Path ".git") {
        Write-Info "Pulling latest changes from git..."
        git pull origin main | Out-Null
        if ($LASTEXITCODE -ne 0) {
            Write-Warn "Could not pull from git"
        }
    }
}

# Build image
Write-Info "Building Docker image..."
docker-compose -f $COMPOSE_FILE build --no-cache
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to build Docker image"
}

# Start services
Write-Info "Starting services..."
docker-compose -f $COMPOSE_FILE --env-file $ENV_FILE up -d
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to start services"
}

# Wait for service to be healthy
Write-Info "Waiting for service to be healthy..."
$MAX_ATTEMPTS = 30
$ATTEMPT = 0

while ($ATTEMPT -lt $MAX_ATTEMPTS) {
    $Status = docker-compose -f $COMPOSE_FILE ps | Select-String "healthy"
    if ($Status) {
        Write-Info "Service is healthy"
        break
    }

    if ($ATTEMPT -eq 0) {
        Write-Info "Waiting for health check..."
    }

    $ATTEMPT++
    Start-Sleep -Seconds 2
}

if ($ATTEMPT -eq $MAX_ATTEMPTS) {
    Write-Warn "Service did not become healthy after $MAX_ATTEMPTS attempts"
    Write-Info "Checking logs..."
    docker-compose -f $COMPOSE_FILE logs cdr-analyzer | Select-Object -Last 20
} else {
    Write-Info "Service is running and healthy"
}

# Display status
Write-Info "Deployment complete!"
Write-Host ""
Write-Host "Service Status:" -ForegroundColor Green
docker-compose -f $COMPOSE_FILE ps

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Green
Write-Host "  1. Test the service:"
Write-Host "     curl http://localhost:8000/api/v1/calls"
Write-Host ""
Write-Host "  2. View logs:"
Write-Host "     docker-compose -f $COMPOSE_FILE logs -f cdr-analyzer"
Write-Host ""
Write-Host "  3. Stop the service:"
Write-Host "     docker-compose -f $COMPOSE_FILE down"

