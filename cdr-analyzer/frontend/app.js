// Configuration
const API_BASE_URL = 'http://localhost:8000/api/v1';

// State
let currentPage = 1;
let pageSize = 50;
let currentFilters = {
    fromDate: null,
    toDate: null,
    search: null
};

// Charts
let dailyChart = null;
let extensionChart = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeDatePickers();
    setDefaultDateRange();
    loadDashboard();
});

// Initialize Persian Date Pickers
function initializeDatePickers() {
    $('#fromDate').persianDatepicker({
        format: 'YYYY/MM/DD',
        initialValue: false,
        autoClose: true,
        calendar: {
            persian: {
                locale: 'fa'
            }
        }
    });
    
    $('#toDate').persianDatepicker({
        format: 'YYYY/MM/DD',
        initialValue: false,
        autoClose: true,
        calendar: {
            persian: {
                locale: 'fa'
            }
        }
    });
}

// Set default date range (last 7 days)
function setDefaultDateRange() {
    const today = new Date();
    const lastWeek = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000);
    
    currentFilters.fromDate = lastWeek.toISOString();
    currentFilters.toDate = today.toISOString();
    
    // Set Persian dates in inputs
    const todayJalali = toJalali(today);
    const lastWeekJalali = toJalali(lastWeek);
    
    $('#fromDate').val(lastWeekJalali);
    $('#toDate').val(todayJalali);
}

// Convert Date to Jalali string
function toJalali(date) {
    const jDate = jalaali.toJalaali(date.getFullYear(), date.getMonth() + 1, date.getDate());
    return `${jDate.jy}/${String(jDate.jm).padStart(2, '0')}/${String(jDate.jd).padStart(2, '0')}`;
}

// Convert Jalali string to Gregorian ISO
function jalaliToGregorian(jalaliStr) {
    const parts = jalaliStr.split('/');
    const gDate = jalaali.toGregorian(parseInt(parts[0]), parseInt(parts[1]), parseInt(parts[2]));
    return new Date(gDate.gy, gDate.gm - 1, gDate.gd).toISOString();
}

// Convert number to Persian numerals
function toPersianNumber(num) {
    const persianDigits = '۰۱۲۳۴۵۶۷۸۹';
    return String(num).replace(/\d/g, digit => persianDigits[digit]);
}

// Format datetime to Persian
function formatPersianDateTime(isoDate) {
    const date = new Date(isoDate);
    const jalali = toJalali(date);
    const time = `${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
    return toPersianNumber(`${jalali} - ${time}`);
}

// Load complete dashboard
async function loadDashboard() {
    await Promise.all([
        loadStatistics(),
        loadDailyChart(),
        loadExtensionChart(),
        loadCalls()
    ]);
}

// Upload file
async function uploadFile() {
    const fileInput = document.getElementById('csvFile');
    const file = fileInput.files[0];
    
    if (!file) {
        showUploadStatus('لطفاً یک فایل انتخاب کنید', 'error');
        return;
    }
    
    if (!file.name.endsWith('.csv')) {
        showUploadStatus('فقط فایل‌های CSV پذیرفته می‌شوند', 'error');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    showUploadStatus('در حال آپلود...', 'loading');
    
    try {
        const response = await fetch(`${API_BASE_URL}/upload`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'خطا در آپلود فایل');
        }
        
        const result = await response.json();
        showUploadStatus(result.message, 'success');
        
        // Reload dashboard
        setTimeout(() => {
            loadDashboard();
        }, 1000);
        
    } catch (error) {
        showUploadStatus(error.message, 'error');
    }
}

// Show upload status
function showUploadStatus(message, type) {
    const statusDiv = document.getElementById('uploadStatus');
    const colors = {
        success: 'bg-green-100 text-green-800 border-green-300',
        error: 'bg-red-100 text-red-800 border-red-300',
        loading: 'bg-blue-100 text-blue-800 border-blue-300'
    };
    
    statusDiv.innerHTML = `
        <div class="p-4 rounded-lg border ${colors[type]}">
            ${message}
        </div>
    `;
}

// Apply date filter
function applyDateFilter() {
    const fromDateJalali = $('#fromDate').val();
    const toDateJalali = $('#toDate').val();
    
    if (fromDateJalali && toDateJalali) {
        currentFilters.fromDate = jalaliToGregorian(fromDateJalali);
        currentFilters.toDate = jalaliToGregorian(toDateJalali);
        
        currentPage = 1;
        loadDashboard();
    }
}

// Load statistics
async function loadStatistics() {
    try {
        const params = new URLSearchParams({
            from_date: currentFilters.fromDate,
            to_date: currentFilters.toDate
        });
        
        const response = await fetch(`${API_BASE_URL}/stats/daily?${params}`);
        const stats = await response.json();
        
        let totalCalls = 0;
        let answeredCalls = 0;
        let missedCalls = 0;
        
        stats.forEach(day => {
            totalCalls += day.total;
            answeredCalls += day.answered;
            missedCalls += day.missed;
        });
        
        const answerRate = totalCalls > 0 ? Math.round((answeredCalls / totalCalls) * 100) : 0;
        
        document.getElementById('totalCalls').textContent = toPersianNumber(totalCalls);
        document.getElementById('answeredCalls').textContent = toPersianNumber(answeredCalls);
        document.getElementById('missedCalls').textContent = toPersianNumber(missedCalls);
        document.getElementById('answerRate').textContent = toPersianNumber(answerRate) + '%';
        
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

// Load daily chart
async function loadDailyChart() {
    try {
        const params = new URLSearchParams({
            from_date: currentFilters.fromDate,
            to_date: currentFilters.toDate
        });
        
        const response = await fetch(`${API_BASE_URL}/stats/daily?${params}`);
        const stats = await response.json();
        
        const labels = stats.map(s => toJalali(new Date(s.date)));
        const answeredData = stats.map(s => s.answered);
        const missedData = stats.map(s => s.missed);
        
        const ctx = document.getElementById('dailyChart').getContext('2d');
        
        if (dailyChart) {
            dailyChart.destroy();
        }
        
        dailyChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'پاسخ داده شده',
                        data: answeredData,
                        borderColor: 'rgb(34, 197, 94)',
                        backgroundColor: 'rgba(34, 197, 94, 0.1)',
                        tension: 0.3
                    },
                    {
                        label: 'از دست رفته',
                        data: missedData,
                        borderColor: 'rgb(239, 68, 68)',
                        backgroundColor: 'rgba(239, 68, 68, 0.1)',
                        tension: 0.3
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
        
    } catch (error) {
        console.error('Error loading daily chart:', error);
    }
}

// Load extension chart
async function loadExtensionChart() {
    try {
        const params = new URLSearchParams({
            from_date: currentFilters.fromDate,
            to_date: currentFilters.toDate
        });
        
        const response = await fetch(`${API_BASE_URL}/stats/extensions?${params}`);
        const stats = await response.json();
        
        const labels = stats.map(s => `داخلی ${s.extension}`);
        const data = stats.map(s => s.call_count);
        
        const ctx = document.getElementById('extensionChart').getContext('2d');
        
        if (extensionChart) {
            extensionChart.destroy();
        }
        
        extensionChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'تعداد تماس',
                    data: data,
                    backgroundColor: 'rgba(37, 99, 235, 0.8)',
                    borderColor: 'rgb(37, 99, 235)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
        
    } catch (error) {
        console.error('Error loading extension chart:', error);
    }
}

// Load calls table
async function loadCalls() {
    try {
        const params = new URLSearchParams({
            page: currentPage,
            limit: pageSize
        });
        
        if (currentFilters.fromDate) params.append('from_date', currentFilters.fromDate);
        if (currentFilters.toDate) params.append('to_date', currentFilters.toDate);
        
        const endpoint = currentFilters.search 
            ? `${API_BASE_URL}/calls/search?phone=${currentFilters.search}&${params}`
            : `${API_BASE_URL}/calls?${params}`;
        
        const response = await fetch(endpoint);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (!result.calls || !Array.isArray(result.calls)) {
            throw new Error('Invalid response format');
        }
        
        renderCallsTable(result.calls);
        updatePagination(result);
        
    } catch (error) {
        console.error('Error loading calls:', error);
        document.getElementById('callsTable').innerHTML = `
            <tr><td colspan="5" class="text-center py-8 text-red-500">خطا در بارگذاری داده‌ها: ${error.message}</td></tr>
        `;
    }
}

// Render calls table
function renderCallsTable(calls) {
    const tbody = document.getElementById('callsTable');
    
    if (!calls || calls.length === 0) {
        tbody.innerHTML = `
            <tr><td colspan="5" class="text-center py-8 text-gray-500">تماسی یافت نشد</td></tr>
        `;
        return;
    }
    
    try {
        tbody.innerHTML = calls.map(call => {
            const statusBadge = call.status === 'ANSWERED'
                ? '<span class="px-2 py-1 bg-green-100 text-green-800 rounded text-xs">پاسخ داده شده</span>'
                : '<span class="px-2 py-1 bg-red-100 text-red-800 rounded text-xs">از دست رفته</span>';
            
            // Clean caller number (remove .0 suffix if present)
            let callerNumber = call.caller_number || '-';
            if (callerNumber.endsWith('.0')) {
                callerNumber = callerNumber.slice(0, -2);
            }
            
            return `
                <tr class="border-b hover:bg-gray-50">
                    <td class="px-6 py-4 persian-number">${formatPersianDateTime(call.timestamp)}</td>
                    <td class="px-6 py-4 persian-number">${callerNumber}</td>
                    <td class="px-6 py-4 persian-number">${call.extension || '-'}</td>
                    <td class="px-6 py-4">${statusBadge}</td>
                    <td class="px-6 py-4 persian-number">${toPersianNumber(call.duration)}</td>
                </tr>
            `;
        }).join('');
    } catch (error) {
        console.error('Error rendering calls table:', error);
        tbody.innerHTML = `
            <tr><td colspan="5" class="text-center py-8 text-red-500">خطا در نمایش داده‌ها</td></tr>
        `;
    }
}

// Update pagination
function updatePagination(result) {
    const totalPages = Math.ceil(result.total / pageSize);
    const start = (currentPage - 1) * pageSize + 1;
    const end = Math.min(currentPage * pageSize, result.total);
    
    document.getElementById('paginationInfo').textContent = 
        toPersianNumber(`نمایش ${start} تا ${end} از ${result.total} تماس`);
    
    document.getElementById('prevBtn').disabled = currentPage === 1;
    document.getElementById('nextBtn').disabled = currentPage >= totalPages;
}

// Pagination functions
function previousPage() {
    if (currentPage > 1) {
        currentPage--;
        loadCalls();
    }
}

function nextPage() {
    currentPage++;
    loadCalls();
}

function changePageSize() {
    pageSize = parseInt(document.getElementById('pageSize').value);
    currentPage = 1;
    loadCalls();
}

// Search calls
let searchTimeout = null;
function searchCalls() {
    clearTimeout(searchTimeout);
    
    searchTimeout = setTimeout(() => {
        const searchValue = document.getElementById('searchPhone').value.trim();
        currentFilters.search = searchValue || null;
        currentPage = 1;
        loadCalls();
    }, 500); // Debounce 500ms
}
