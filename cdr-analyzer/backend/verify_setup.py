"""
Verify CDR Analyzer setup and dependencies
"""
import sys

def check_dependencies():
    """Check if all required dependencies are installed"""
    missing = []
    
    try:
        import fastapi
        print("✓ FastAPI installed:", fastapi.__version__)
    except ImportError:
        print("✗ FastAPI not installed")
        missing.append("fastapi")
    
    try:
        import uvicorn
        print("✓ Uvicorn installed:", uvicorn.__version__)
    except ImportError:
        print("✗ Uvicorn not installed")
        missing.append("uvicorn")
    
    try:
        import pydantic
        print("✓ Pydantic installed:", pydantic.__version__)
    except ImportError:
        print("✗ Pydantic not installed")
        missing.append("pydantic")
    
    try:
        import pandas
        print("✓ Pandas installed:", pandas.__version__)
    except ImportError:
        print("✗ Pandas not installed")
        missing.append("pandas")
    
    return missing

def check_files():
    """Check if required files exist"""
    import os
    
    required_files = [
        'main.py',
        'models.py',
        'database.py',
        'processor.py',
        'routes/upload.py',
        'routes/calls.py',
        'routes/stats.py',
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} missing")
            missing_files.append(file)
    
    return missing_files

def test_database():
    """Test database initialization"""
    try:
        from database import init_db
        init_db()
        print("✓ Database initialized successfully")
        return True
    except Exception as e:
        print(f"✗ Database initialization failed: {e}")
        return False

def main():
    print("=" * 60)
    print("CDR Analyzer - Setup Verification")
    print("=" * 60)
    print()
    
    print("Checking Python version...")
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("⚠ Warning: Python 3.10+ recommended")
    print()
    
    print("Checking dependencies...")
    missing_deps = check_dependencies()
    print()
    
    print("Checking required files...")
    missing_files = check_files()
    print()
    
    print("Testing database...")
    db_ok = test_database()
    print()
    
    print("=" * 60)
    if not missing_deps and not missing_files and db_ok:
        print("✅ All checks passed! Ready to run.")
        print()
        print("Start the server with:")
        print("  python main.py")
        print()
        print("API will be available at: http://localhost:8000")
        print("API docs at: http://localhost:8000/docs")
        return 0
    else:
        print("❌ Setup incomplete. Please fix the issues above.")
        if missing_deps:
            print()
            print("Install missing dependencies:")
            print(f"  pip install {' '.join(missing_deps)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
