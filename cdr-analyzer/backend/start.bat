@echo off
echo ========================================
echo CDR Analyzer - Starting Server
echo ========================================
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting FastAPI server...
echo Server will be available at: http://localhost:8000
echo.
python main.py
