cdr-analyzer/backend## Common Build Errors and Solutions

### Error: "unable to prepare context: path X not found"

**Root Cause**: The Docker build context path is incorrect or doesn't exist when Coolify clones the repository.

**Example Error**:
```
unable to prepare context: path "/artifacts/yc88g4wwo0gcss84c808s0c8/backend" not found
```

**Solution**:

1. **Verify your directory structure** matches the project layout:
   ```
   Project Root (CDRreport)/
   └── cdr-analyzer/
       ├── backend/              ← Backend source code (build context)
       │   ├── Dockerfile
       │   ├── main.py
       │   ├── requirements.txt
       │   └── ...
       ├── frontend/
       ├── docker-compose.prod.coolify.yml
       ├── .env.production
       └── ...
   ```

2. **Check the build context in docker-compose.prod.coolify.yml**:
   - The compose file is in `cdr-analyzer/` directory
   - Backend source is in `cdr-analyzer/backend/`
   - Use `./backend` as the build context:
   
   ```yaml
   # Correct for cdr-analyzer/docker-compose.prod.coolify.yml:
   services:
     cdr-analyzer:
       build:
         context: ./backend     # Relative to where this compose file is
         dockerfile: Dockerfile  # Relative to the context
   ```

3. **Verify Dockerfile exists** at the correct location:
   ```bash
   ls -la cdr-analyzer/backend/Dockerfile
   ```

4. **Test locally before pushing to Coolify**:
   ```bash
   # From project root (CDRreport/)
   cd cdr-analyzer
   docker-compose -f docker-compose.prod.coolify.yml build
   ```

---

### Error: "Dockerfile not found for service X"

**Root Cause**: The Dockerfile path is incorrect or missing the `Dockerfile` file.

**Solution**:

1. **Check Dockerfile location**:
   ```bash
   # Should exist at:
   backend/Dockerfile
   ```

2. **If Dockerfile doesn't exist**, create it. Example:
   ```dockerfile
   FROM python:3.9-slim

   WORKDIR /app

   # Copy requirements
   COPY requirements.txt .
   RUN pip install -r requirements.txt

   # Copy application code
   COPY . .

   # Set environment
   ENV PYTHONUNBUFFERED=1

   # Expose port
   EXPOSE 8000

   # Health check
   HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
     CMD curl -f http://localhost:8000/api/v1/calls || exit 1

   # Run application
   CMD ["python", "main.py"]
   ```

3. **Verify the dockerfile path** in docker-compose file:
   ```yaml
   build:
     context: ./backend
     dockerfile: Dockerfile  # Must exist at ./backend/Dockerfile
   ```

---

### Error: "git clone" or "git pull" failures

**Root Cause**: Git authentication issues or incorrect repository configuration.

**Solution**:

1. **Ensure repository is public or** Coolify has proper credentials
2. **Verify branch exists**:
   ```bash
   git branch -a | grep main
   ```

3. **Check repository URL**:
   ```bash
   git remote -v
   ```

---

### Error: "exit status 1" with no clear message

**Root Cause**: Generic docker build failure, often due to file not found.

**Debug Steps**:

1. **Check the full build output** in Coolify logs
2. **Verify all file paths** referenced in docker-compose file
3. **Test build locally**:
   ```bash
   # Navigate to project root
   cd /path/to/CDRreport
   
   # Try the same build command
   docker-compose -f cdr-analyzer/docker-compose.prod.coolify.yml build --pull
   ```

4. **Check for missing dependencies** in requirements.txt:
   ```bash
   cat backend/requirements.txt
   ```

5. **Verify environment variables** are properly set in .env.production:
   ```bash
   cat cdr-analyzer/.env.production
   ```

---

## Coolify-Specific Configuration Issues

### Issue: Dockerfile not found in logs

**Logs show**:
```
Dockerfile not found for service cdr-analyzer at backend/Dockerfile, skipping ARG injection.
```

**This is NOT necessarily an error** if:
- Your Dockerfile is a relative path (e.g., `./Dockerfile`)
- The build context is correct

**To avoid this**, ensure:
1. The build context path is correct relative to compose file location
2. Dockerfile exists at the specified path
3. Both context and dockerfile are specified in compose file

---

### Issue: Service won't start after successful build

**Logs show build succeeded but container won't run**:

1. **Check health check endpoint**:
   ```bash
   # In the Coolify server, test manually:
   docker exec cdr-analyzer curl -v http://localhost:8000/api/v1/calls
   ```

2. **Check application logs**:
   ```bash
   docker logs cdr-analyzer
   ```

3. **Verify environment variables are loaded**:
   ```bash
   docker exec cdr-analyzer env | grep DATABASE_PATH
   ```

4. **Check volume mounts**:
   ```bash
   docker inspect cdr-analyzer | grep -A 20 Mounts
   ```

---

## Fix Checklist

Before rebuilding in Coolify:

- [ ] Repository is cloned correctly to `/artifacts/...`
- [ ] Backend directory exists at `cdr-analyzer/backend/`
- [ ] Dockerfile exists at `cdr-analyzer/backend/Dockerfile`
- [ ] docker-compose.prod.coolify.yml has correct build context path: `./backend`
- [ ] Build context is relative to compose file location
- [ ] All environment variables are set in `.env.production`
- [ ] Volumes directories exist and are writable
- [ ] Tested build locally from cdr-analyzer directory: `docker-compose -f docker-compose.prod.coolify.yml build`

---

## Manual Build Test

Run this from the cdr-analyzer directory to simulate what Coolify does:

```bash
# Navigate to cdr-analyzer directory
cd /path/to/CDRreport/cdr-analyzer

# Test the build with exact compose file path
docker-compose -f docker-compose.prod.coolify.yml build --pull

# If build succeeds, test running it
docker-compose \
  -f docker-compose.prod.coolify.yml \
  --env-file .env.production \
  up -d

# Check status
docker ps | grep cdr-analyzer

# View logs
docker logs -f cdr-analyzer

# Test health endpoint
curl http://localhost:8000/api/v1/calls
```

---

## Path Reference Table

| Location | Purpose | Build Context |
|----------|---------|---|
| `cdr-analyzer/backend/Dockerfile` | Application image | `./backend` (from cdr-analyzer/) |
| `cdr-analyzer/backend/main.py` | Entry point | Included in build context |
| `cdr-analyzer/backend/requirements.txt` | Python dependencies | Included in build context |
| `cdr-analyzer/docker-compose.prod.coolify.yml` | Compose definition | N/A (file location) |
| `cdr-analyzer/.env.production` | Environment vars | N/A (config file) |
| `/data/cdr-analyzer/cdr-data/` | Database volume | Mounted at runtime |

---

## Still Having Issues?

1. **Enable debug logging** in Coolify:
   - Dashboard → Settings → Debug mode
   - Restart and check detailed logs

2. **Check Git configuration**:
   - Verify branch name is correct (usually `main`)
   - Ensure repository URL is correct
   - Check access token/SSH keys

3. **Validate JSON in docker-compose.prod.coolify.yml**:
   - YAML syntax must be perfect
   - Use online YAML validators

4. **Contact support with**:
   - Full error message from Coolify
   - Git commit hash
   - docker-compose file content
   - Directory structure output: `find . -type f -name "Dockerfile" -o -name "docker-compose*"`

