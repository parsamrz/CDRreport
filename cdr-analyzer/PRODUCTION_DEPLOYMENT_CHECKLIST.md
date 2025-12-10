# Production Deployment Checklist for CDR Analyzer with Coolify

Use this checklist before deploying to production to ensure all requirements are met.

## Pre-Deployment Planning

- [ ] **Team Alignment**
  - [ ] Inform stakeholders of deployment date/time
  - [ ] Schedule maintenance window
  - [ ] Identify on-call support

- [ ] **Infrastructure Readiness**
  - [ ] Production server has minimum resources (2 CPU, 2GB RAM, 50GB disk)
  - [ ] Network connectivity verified
  - [ ] Coolify instance is running and accessible
  - [ ] DNS records are prepared

- [ ] **Data Preparation**
  - [ ] Existing data is backed up
  - [ ] Migration scripts tested (if any)
  - [ ] Database integrity verified

## Configuration Review

- [ ] **Environment Variables** (`.env.production`)
  - [ ] `ENVIRONMENT=production` is set
  - [ ] `DATABASE_PATH` points to correct location
  - [ ] `LOG_LEVEL=INFO` (not DEBUG)
  - [ ] `WORKERS=4` or appropriate for your hardware
  - [ ] All required variables are defined
  - [ ] No sensitive data is hardcoded

- [ ] **Docker Compose Configuration** (`docker-compose.prod.coolify.yml`)
  - [ ] File paths use absolute paths from project root
  - [ ] Volume mounts point to `/data/cdr-analyzer/*`
  - [ ] Resource limits are appropriate
  - [ ] Health check endpoint is correct
  - [ ] Restart policy is `always`

- [ ] **Paths Verification**
  - [ ] `/data/cdr-analyzer/cdr-data` exists and is writable
  - [ ] `/data/cdr-analyzer/logs` exists and is writable
  - [ ] Backup directory (`/backups/cdr-analyzer`) exists
  - [ ] Permissions are correctly set (755 for directories)

## Security Configuration

- [ ] **Network Security**
  - [ ] Firewall rules are configured
  - [ ] Only necessary ports are exposed (8000 for API)
  - [ ] Reverse proxy (Nginx/Caddy) is configured
  - [ ] HTTPS/TLS is enabled with valid certificate

- [ ] **Application Security**
  - [ ] `SECURE_COOKIES=true`
  - [ ] `CSRF_ENABLED=true`
  - [ ] Session timeout is configured appropriately
  - [ ] Input validation is in place

- [ ] **Secret Management**
  - [ ] No secrets in git repository
  - [ ] Secrets are stored in Coolify secret management
  - [ ] API keys and passwords are strong
  - [ ] Secrets are not logged

## Monitoring & Alerting

- [ ] **Health Checks**
  - [ ] Health check endpoint is accessible
  - [ ] Expected HTTP status code is 200
  - [ ] Response time is acceptable (<1s)

- [ ] **Logging**
  - [ ] Log aggregation tool is configured
  - [ ] Log rotation is enabled
  - [ ] Critical error alerts are set up
  - [ ] Log files have appropriate permissions

- [ ] **Monitoring**
  - [ ] CPU usage monitoring is configured
  - [ ] Memory usage monitoring is configured
  - [ ] Disk usage monitoring is configured (alert at 80%)
  - [ ] API response time monitoring is configured
  - [ ] Error rate monitoring is configured

- [ ] **Alerting**
  - [ ] Alert for service down/restart
  - [ ] Alert for health check failures
  - [ ] Alert for resource exhaustion
  - [ ] Alert channels are verified (email, Slack, etc.)

## Backup & Disaster Recovery

- [ ] **Backup Strategy**
  - [ ] Automated daily backups are configured
  - [ ] Backup retention policy is defined (e.g., 30 days)
  - [ ] Backup storage is verified and accessible
  - [ ] Backup test restore has been performed

- [ ] **Recovery Procedures**
  - [ ] RTO (Recovery Time Objective) is defined
  - [ ] RPO (Recovery Point Objective) is defined
  - [ ] Rollback procedure is documented
  - [ ] Rollback has been tested

## Load Balancing & Scaling

- [ ] **Single Instance** (if applicable)
  - [ ] Resource limits are sufficient
  - [ ] Scaling plan exists for future growth

- [ ] **Multiple Instances**
  - [ ] Load balancer is configured
  - [ ] Session persistence is configured
  - [ ] Database sharing strategy is implemented
  - [ ] Load distribution is balanced

## Testing

- [ ] **Functionality Testing**
  - [ ] API endpoints are responding
  - [ ] Data processing works correctly
  - [ ] Reports generation works
  - [ ] All critical features are tested

- [ ] **Performance Testing**
  - [ ] Response times meet SLA
  - [ ] Database queries are optimized
  - [ ] Memory usage is stable
  - [ ] No memory leaks detected

- [ ] **Stress Testing**
  - [ ] System handles expected load
  - [ ] Graceful degradation under peak load
  - [ ] No crashes under sustained load

- [ ] **Security Testing**
  - [ ] Common vulnerabilities are checked
  - [ ] Authentication/Authorization works
  - [ ] HTTPS enforced
  - [ ] No sensitive data in logs

## Coolify Configuration

- [ ] **Coolify Setup**
  - [ ] Service is registered in Coolify
  - [ ] Git webhook is configured
  - [ ] Auto-deployment is configured (optional)
  - [ ] Service labels are correct

- [ ] **Coolify Integration**
  - [ ] Docker image builds successfully
  - [ ] Container runs and stays healthy
  - [ ] Volume mounts work correctly
  - [ ] Environment variables are loaded
  - [ ] Logs are accessible in Coolify dashboard

## Documentation

- [ ] **Runbooks**
  - [ ] Deployment procedure documented
  - [ ] Startup/shutdown procedure documented
  - [ ] Scaling procedure documented
  - [ ] Emergency shutdown procedure documented

- [ ] **Troubleshooting Guide**
  - [ ] Common issues documented
  - [ ] Resolution steps provided
  - [ ] Support contact information included

- [ ] **Architecture Documentation**
  - [ ] System architecture documented
  - [ ] Component relationships documented
  - [ ] Data flow documented

## Sign-Off

- [ ] **Development Team**
  - [ ] Code quality reviewed
  - [ ] Performance acceptable
  - [ ] All unit tests passed

- [ ] **QA Team**
  - [ ] Functional testing completed
  - [ ] Regression testing completed
  - [ ] No critical issues remain

- [ ] **Operations Team**
  - [ ] Infrastructure ready
  - [ ] Monitoring configured
  - [ ] Backup strategy verified
  - [ ] Runbooks reviewed

- [ ] **Security Team** (if applicable)
  - [ ] Security review completed
  - [ ] Vulnerabilities addressed
  - [ ] Compliance requirements met

## Post-Deployment

- [ ] **Verification**
  - [ ] Service is running
  - [ ] Health checks pass
  - [ ] API responds correctly
  - [ ] Data is accessible

- [ ] **Monitoring**
  - [ ] Monitor logs for errors
  - [ ] Check resource usage
  - [ ] Verify performance metrics
  - [ ] Monitor for 24 hours initially

- [ ] **Documentation Updates**
  - [ ] Update deployment record
  - [ ] Document any issues encountered
  - [ ] Update runbooks if needed
  - [ ] Notify stakeholders

## Rollback Plan

If issues are detected:

1. **Immediate Actions**
   - [ ] Alert on-call team
   - [ ] Notify stakeholders
   - [ ] Assess severity

2. **Rollback Procedure**
   - [ ] Stop current deployment
   - [ ] Restore from backup if needed
   - [ ] Deploy previous version
   - [ ] Verify services are operational

3. **Post-Rollback**
   - [ ] Root cause analysis
   - [ ] Fix identified issues
   - [ ] Re-test before re-deployment
   - [ ] Schedule new deployment

## Useful Commands

### Deployment
```bash
./deploy-prod.sh                    # Linux/macOS
.\deploy-prod.ps1                   # Windows
```

### Verification
```bash
docker-compose -f docker-compose.prod.coolify.yml ps
docker-compose -f docker-compose.prod.coolify.yml logs -f cdr-analyzer
curl http://localhost:8000/api/v1/calls
```

### Backup
```bash
docker-compose -f docker-compose.prod.coolify.yml exec cdr-analyzer \
  cp /app/data/cdr.db /app/data/cdr.db.backup.$(date +%Y%m%d)
```

### Rollback
```bash
docker-compose -f docker-compose.prod.coolify.yml down
git checkout <previous-version>
docker-compose -f docker-compose.prod.coolify.yml up -d
```

---

**Deployment Date**: _______________  
**Deployed By**: _______________  
**Approved By**: _______________  
**Issues Encountered**: _______________  
**Notes**: _______________

