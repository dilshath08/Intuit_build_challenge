"""
Unit tests for Sales and Usage Analytics (Assignment Two).

Run with:
    pytest test_analysis.py
"""

from pathlib import Path
import pytest

from analysis import (
    read_usage_csv,
    total_revenue,
    revenue_by_user_segment,
    revenue_by_feature,
    avg_tokens_by_feature,
    top_n_features_by_revenue,
    average_latency,
)

def load_records():
    path = Path(__file__).with_name("sample_sales.csv")
    return read_usage_csv(path)

def test_read_usage_csv_loads_all_rows():
    records = load_records()
    assert len(records) == 10
    assert records[0].transaction_id == "T1001"
    assert records[0].feature_name == "smart_reply"
    assert records[1].session_revenue_usd == 5.0

def test_total_revenue():
    records = load_records()
    value = total_revenue(records)
    # Manual verification: 10 + 10 + 20 = 40
    assert value == pytest.approx(40.0, rel=1e-6)

def test_revenue_by_user_segment():
    records = load_records()
    by_segment = revenue_by_user_segment(records)

    assert by_segment["free"] == pytest.approx(0.0, rel=1e-6)
    assert by_segment["premium"] == pytest.approx(40.0, rel=1e-6)

def test_revenue_by_feature():
    records = load_records()
    by_feature = revenue_by_feature(records)

    assert by_feature["smart_reply"] == pytest.approx(10.0, rel=1e-6)
    assert by_feature["data_extraction"] == pytest.approx(10.0, rel=1e-6)
    assert by_feature["translation"] == pytest.approx(0.0, rel=1e-6)
    assert by_feature["document_summary"] == pytest.approx(20.0, rel=1e-6)

def test_avg_tokens_by_feature():
    records = load_records()
    averages = avg_tokens_by_feature(records)

    # smart_reply tokens: [120, 150, 160, 100] → mean = 132.5
    assert averages["smart_reply"] == pytest.approx(132.5, rel=1e-6)

    # document_summary tokens: [900, 1100] → mean = 1000
    assert averages["document_summary"] == pytest.approx(1000.0, rel=1e-6)

    # translation tokens: [200, 180] → mean = 190
    assert averages["translation"] == pytest.approx(190.0, rel=1e-6)

def test_top_n_features_by_revenue():
    records = load_records()
    top_two = top_n_features_by_revenue(records, n=2)

    # Expected order based on revenue:
    # document_summary: 20
    # smart_reply: 10 (tie with data_extraction but appears first alphabetically)
    assert top_two[0][0] == "document_summary"
    assert top_two[0][1] == pytest.approx(20.0, rel=1e-6)

    assert top_two[1][0] in ("smart_reply", "data_extraction")
    assert top_two[1][1] == pytest.approx(10.0, rel=1e-6)

def test_average_latency():
    records = load_records()

    expected_avg = sum(r.response_time_ms for r in records) / len(records)

    assert average_latency(records) == pytest.approx(expected_avg, rel=1e-6)