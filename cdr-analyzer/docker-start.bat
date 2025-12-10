@echo off
echo ========================================
echo CDR Analyzer - Docker Deployment
echo ========================================
echo.
echo Building and starting Docker containers...
echo.
docker-compose up -d --build
echo.
echo ========================================
echo Deployment complete!
echo ========================================
echo.
echo Access the application at:
echo   http://localhost:8000
echo.
echo View logs:
echo   docker-compose logs -f
echo.
echo Stop containers:
echo   docker-compose down
echo.
pause
