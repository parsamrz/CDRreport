# Coolify Working Directory Configuration Guide

## Problem

By default, Coolify clones the entire repository to `/artifacts/[container-id]/` directory. When using Docker Compose, it needs to know the correct working directory context for finding files and resolving relative paths.

## Solution

Set the **working directory** to `cdr-analyzer/` so that all relative paths in the compose files are resolved correctly.

## How to Configure in Coolify UI

### Step 1: Create or Edit Service in Coolify

1. Go to **Services** → Select your CDR Analyzer service
2. Navigate to **Service Settings**
3. Look for **Docker Compose** configuration section

### Step 2: Set Working Directory

In the Coolify UI, you need to specify:

```
Working Directory: cdr-analyzer
```

Or in the service configuration, set:

```
Project Directory: cdr-analyzer
```

**Alternative Field Names (depending on Coolify version)**:
- Working Directory
- Project Directory  
- Compose Working Directory
- Service Directory

### Step 3: Set Docker Compose File Path

The compose file path should be relative to the working directory:

```
Docker Compose File: docker-compose.prod.coolify.yml
```

**Full path from repository root**: `cdr-analyzer/docker-compose.prod.coolify.yml`

### Step 4: Verify Configuration

The final resolved paths should be:

| Item | Full Path | Relative to Working Dir |
|------|-----------|--------------------------|
| Repository Root | `/artifacts/[id]/` | - |
| Working Directory | `/artifacts/[id]/cdr-analyzer/` | `.` or `cdr-analyzer/` |
| Compose File | `/artifacts/[id]/cdr-analyzer/docker-compose.prod.coolify.yml` | `docker-compose.prod.coolify.yml` |
| Backend Context | `/artifacts/[id]/cdr-analyzer/backend/` | `./backend` |
| Dockerfile | `/artifacts/[id]/cdr-analyzer/backend/Dockerfile` | `./backend/Dockerfile` |

## Directory Resolution in Docker Compose

When Docker Compose executes with `cdr-analyzer/` as working directory:

```yaml
services:
  cdr-analyzer:
    build:
      context: ./backend          # Resolves to: /artifacts/[id]/cdr-analyzer/backend/
      dockerfile: Dockerfile      # Resolves to: /artifacts/[id]/cdr-analyzer/backend/Dockerfile
    volumes:
      - cdr-data:/app/data       # Named volume
      - ./backend:/app            # Resolves to: /artifacts/[id]/cdr-analyzer/backend/
```

## Coolify Command Line Equivalent

If deploying via CLI, the equivalent command would be:

```bash
cd /artifacts/[container-id]/cdr-analyzer

docker-compose \
  -f docker-compose.prod.coolify.yml \
  --env-file .env.production \
  build --pull

docker-compose \
  -f docker-compose.prod.coolify.yml \
  --env-file .env.production \
  up -d
```

## Configuration in Coolify YAML (if applicable)

If your Coolify setup uses YAML configuration files, you may need to set:

```yaml
services:
  cdr-analyzer:
    source:
      type: git
      repo: https://github.com/parsamrz/CDRreport.git
      branch: main
    docker:
      composeFile: cdr-analyzer/docker-compose.prod.coolify.yml
      workingDirectory: cdr-analyzer
      env: cdr-analyzer/.env.production
```

## Troubleshooting Working Directory Issues

### Error: "unable to prepare context: path X not found"

**Cause**: Working directory is not set or set incorrectly.

**Solution**:
1. Verify working directory is set to `cdr-analyzer`
2. Check that compose file exists at: `cdr-analyzer/docker-compose.prod.coolify.yml`
3. Verify backend directory exists at: `cdr-analyzer/backend/`
4. Ensure Dockerfile exists at: `cdr-analyzer/backend/Dockerfile`

### Error: "Dockerfile not found"

**Cause**: Build context is wrong because working directory wasn't set.

**Solution**:
1. Set working directory to `cdr-analyzer`
2. Compose will then correctly find `./backend/Dockerfile`

### Test Locally

To verify your setup works, from the project root:

```bash
# Navigate to cdr-analyzer directory
cd cdr-analyzer

# Run the exact same command Coolify would run
docker-compose -f docker-compose.prod.coolify.yml build --pull

# If successful, try running it
docker-compose -f docker-compose.prod.coolify.yml up -d

# Check logs
docker-compose logs -f cdr-analyzer

# Test API
curl http://localhost:8000/api/v1/calls
```

## Path Reference Summary

```
Repository Structure:
CDRreport/
├── cdr-analyzer/                                ← Working Directory
│   ├── backend/                                 ← build context: ./backend
│   │   ├── Dockerfile                           ← dockerfile: Dockerfile
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   └── ...
│   ├── docker-compose.prod.coolify.yml         ← Compose file
│   ├── .env.production                          ← Environment file
│   └── ...
└── ...
```

## Key Points

1. **Always set working directory to `cdr-analyzer`** in Coolify settings
2. **All relative paths in compose files** are resolved from `cdr-analyzer/`
3. **`./backend` resolves to `cdr-analyzer/backend/`** when working directory is `cdr-analyzer`
4. **Test locally first** by running `cd cdr-analyzer && docker-compose -f docker-compose.prod.coolify.yml build`

## Verification Checklist

Before deploying to Coolify:

- [ ] Working directory is set to `cdr-analyzer`
- [ ] Docker Compose file path is `docker-compose.prod.coolify.yml`
- [ ] Environment file path is `.env.production`
- [ ] Backend directory exists at `cdr-analyzer/backend/`
- [ ] Dockerfile exists at `cdr-analyzer/backend/Dockerfile`
- [ ] Local build test succeeds: `cd cdr-analyzer && docker-compose -f docker-compose.prod.coolify.yml build`
- [ ] All relative paths in compose file use `./` prefix for directories

## Support

If you still encounter issues after setting the working directory:

1. Check Coolify logs for the exact error message
2. Verify file paths in the error message
3. Test locally from `cdr-analyzer/` directory
4. Check that Coolify cloned the repo completely (includes all files)

