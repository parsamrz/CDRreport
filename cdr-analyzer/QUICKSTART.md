# Quick Start Guide - CDR Analyzer

## 🚀 Fast Setup (5 minutes)

### Step 1: Install Dependencies

Open terminal in `cdr-analyzer/backend` folder:

```bash
pip install fastapi uvicorn pydantic pandas python-multipart
```

### Step 2: Verify Setup

```bash
python verify_setup.py
```

You should see all checkmarks (✓). If any issues, install missing packages.

### Step 3: Start Backend

```bash
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
✅ Database initialized successfully
```

Keep this terminal open!

### Step 4: Open Frontend

Open `cdr-analyzer/frontend/index.html` directly in your browser, or:

```bash
# In a new terminal
cd cdr-analyzer/frontend
python -m http.server 8080
```

Then navigate to: `http://localhost:8080`

### Step 5: Test with Sample Data

1. In the dashboard, click "آپلود" (Upload)
2. Select `backend/test_sample.csv`
3. Click upload button
4. You should see: "Processed 12 records, 4 unique calls added"
5. Dashboard will update with charts and call list

## 🎯 Usage

### Upload Your CDR File
- Must be CSV format
- Maximum 10MB
- Required columns: UniqueID, Source, Date, Status, Duration

### Filter by Date
- Click on date fields to open Jalali calendar
- Select date range
- Click "اعمال فیلتر" (Apply Filter)

### Search Calls
- Type phone number in search box
- Results update automatically

### View Statistics
- Total calls, answered, missed
- Daily trend chart
- Extension performance chart

## 📊 API Documentation

Once backend is running, visit: `http://localhost:8000/docs`

Interactive API documentation with ability to test all endpoints.

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is already in use
netstat -an | findstr :8000  # Windows
lsof -i :8000                # Linux/Mac

# Use different port
uvicorn main:app --port 8001
```

### Frontend can't connect to backend
- Check backend is running on port 8000
- Check CORS settings in `main.py`
- Update `API_BASE_URL` in `frontend/app.js` if needed

### CSV upload fails
- Verify CSV has required columns
- Check file size < 10MB
- Ensure CSV is properly formatted (UTF-8 encoding)

### Charts not showing
- Open browser console (F12)
- Check for JavaScript errors
- Verify Chart.js loaded: `typeof Chart !== 'undefined'`

### Dates not in Persian
- Check jalaali-js library loaded
- Verify Persian DatePicker initialized
- Check browser console for errors

## 📝 Sample CSV Format

```csv
UniqueID,Source,Date,Status,Duration,Dst.Channel
1234.56,09121234567,2024-12-09 14:30:00,ANSWERED,145,SIP/209-001
1234.57,09129876543,2024-12-09 14:35:00,NO ANSWER,0,
```

## ✅ Success Checklist

- [ ] Backend running on port 8000
- [ ] Frontend opens in browser
- [ ] Can upload test_sample.csv
- [ ] See 4 calls in the list
- [ ] Charts display data
- [ ] Can filter by date
- [ ] Search works
- [ ] Pagination works

## 🆘 Need Help?

Check logs:
- Backend: Console where `python main.py` is running
- Frontend: Browser console (F12)
- Database: Check if `cdr.db` file created

Common fixes:
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Reset database
rm cdr.db
python main.py  # Will recreate database
```

## 🎓 Next Steps

1. Upload your actual CDR files
2. Explore API documentation
3. Customize frontend styles
4. Set up regular imports
5. Read DEPLOYMENT.md for production setup
