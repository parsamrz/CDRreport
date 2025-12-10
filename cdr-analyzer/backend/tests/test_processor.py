"""
Unit tests for CDR processor
"""
import pytest
from processor import parse_extension, parse_duration, process_cdr_file
from io import BytesIO

def test_parse_extension():
    """Test extension extraction from channel strings"""
    assert parse_extension("SIP/209-000012ec") == "209"
    assert parse_extension("PJSIP/210-00001234") == "210"
    assert parse_extension("SIP/305-abc") == "305"
    assert parse_extension(None) is None
    assert parse_extension("") is None

def test_parse_duration():
    """Test duration parsing"""
    assert parse_duration("45s") == 45
    assert parse_duration("2min 30s") == 150
    assert parse_duration("145") == 145
    assert parse_duration("1min") == 60
    assert parse_duration(None) == 0

def test_process_empty_csv():
    """Test processing empty CSV"""
    csv_content = b"UniqueID,Source,Date,Status,Duration\n"
    records, total, unique = process_cdr_file(csv_content)
    assert total == 0
    assert unique == 0
    assert len(records) == 0

def test_process_single_call():
    """Test processing CSV with single call"""
    csv_content = b"""UniqueID,Source,Date,Status,Duration,Dst.Channel
1234.56,09121234567,2024-12-09 14:30:00,ANSWERED,45s,SIP/209-001
"""
    records, total, unique = process_cdr_file(csv_content)
    assert total == 1
    assert unique == 1
    assert len(records) == 1
    assert records[0]['status'] == 'ANSWERED'
    assert records[0]['duration'] == 45
    assert records[0]['extension'] == '209'

def test_process_grouped_records():
    """Test that multiple records with same UniqueID are grouped"""
    csv_content = b"""UniqueID,Source,Date,Status,Duration,Dst.Channel
1234.56,09121234567,2024-12-09 14:30:00,RINGING,0,
1234.56,09121234567,2024-12-09 14:30:05,ANSWERED,45s,SIP/209-001
1234.56,09121234567,2024-12-09 14:30:05,ANSWERED,45s,SIP/210-002
"""
    records, total, unique = process_cdr_file(csv_content)
    assert total == 3
    assert unique == 1  # Should create only 1 record
    assert records[0]['status'] == 'ANSWERED'

def test_answered_vs_missed():
    """Test call status detection"""
    # Answered call
    csv_answered = b"""UniqueID,Source,Date,Status,Duration
1234.56,09121234567,2024-12-09 14:30:00,ANSWERED,45
"""
    records, _, _ = process_cdr_file(csv_answered)
    assert records[0]['status'] == 'ANSWERED'
    
    # Missed call
    csv_missed = b"""UniqueID,Source,Date,Status,Duration
1234.57,09121234567,2024-12-09 14:30:00,NO ANSWER,0
"""
    records, _, _ = process_cdr_file(csv_missed)
    assert records[0]['status'] == 'MISSED'

def test_zero_duration_answered():
    """Test that ANSWERED with duration=0 is treated as MISSED"""
    csv_content = b"""UniqueID,Source,Date,Status,Duration
1234.56,09121234567,2024-12-09 14:30:00,ANSWERED,0
"""
    records, _, _ = process_cdr_file(csv_content)
    assert records[0]['status'] == 'MISSED'

def test_missing_columns():
    """Test error handling for missing required columns"""
    csv_content = b"""UniqueID,Source,Date
1234.56,09121234567,2024-12-09 14:30:00
"""
    with pytest.raises(ValueError) as exc_info:
        process_cdr_file(csv_content)
    assert "missing required columns" in str(exc_info.value).lower()

def test_ring_group_one_answers():
    """Test ring group scenario: one extension answers, others NO ANSWER"""
    csv_content = b"""UniqueID,Source,Date,Status,Duration,Dst.Channel
1234.56,09121234567,2024-12-09 14:30:00,RINGING,0,
1234.56,09121234567,2024-12-09 14:30:02,NO ANSWER,0,SIP/201-001
1234.56,09121234567,2024-12-09 14:30:02,NO ANSWER,0,SIP/202-002
1234.56,09121234567,2024-12-09 14:30:05,ANSWERED,180,SIP/203-003
"""
    records, total, unique = process_cdr_file(csv_content)
    assert total == 4
    assert unique == 1
    assert records[0]['status'] == 'ANSWERED'
    assert records[0]['extension'] == '203'
    assert records[0]['duration'] == 180

def test_ring_group_all_no_answer():
    """Test ring group scenario: all extensions NO ANSWER"""
    csv_content = b"""UniqueID,Source,Date,Status,Duration,Dst.Channel
1234.57,09131112222,2024-12-09 14:35:00,RINGING,0,
1234.57,09131112222,2024-12-09 14:35:05,NO ANSWER,0,SIP/201-001
1234.57,09131112222,2024-12-09 14:35:05,NO ANSWER,0,SIP/202-002
1234.57,09131112222,2024-12-09 14:35:05,NO ANSWER,0,SIP/203-003
"""
    records, total, unique = process_cdr_file(csv_content)
    assert total == 4
    assert unique == 1
    assert records[0]['status'] == 'MISSED'

def test_phone_number_float_cleanup():
    """Test that phone numbers with .0 suffix are cleaned"""
    csv_content = b"""UniqueID,Source,Date,Status,Duration
1234.56,9121234567.0,2024-12-09 14:30:00,ANSWERED,45
1234.57,9129876543,2024-12-09 14:35:00,ANSWERED,60
"""
    records, _, _ = process_cdr_file(csv_content)
    # Phone number with .0 should have it removed
    assert records[0]['caller_number'] == '9121234567'
    # Phone number without .0 should remain unchanged
    assert records[1]['caller_number'] == '9129876543'

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
