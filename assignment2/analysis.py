"""
Sales and Usage Analytics for Assignment Two.

Dataset choice:
This dataset models AI feature usage where each row represents a monetizable
transaction. It includes traditional sales fields (transaction_id, quantity,
unit_price_usd, session_revenue_usd) along with AI usage metrics like tokens used,
feedback score and response latency. This makes it suitable for grouping,
aggregation and functional-style queries.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Iterable, Callable, Tuple
from collections import defaultdict

@dataclass
class UsageRecord:
    transaction_id: str
    date: datetime
    user_segment: str
    feature_name: str
    quantity: int
    unit_price_usd: float
    session_revenue_usd: float
    tokens_used: int
    response_time_ms: int
    feedback_score: int
    country: str

def read_usage_csv(path: Path) -> List[UsageRecord]:
    """
    Read the CSV file and return a list of UsageRecord objects.
    """
    
    records: List[UsageRecord] = []

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(
                UsageRecord(
                    transaction_id=row["transaction_id"],
                    date=datetime.strptime(row["date"], "%Y-%m-%d"),
                    user_segment=row["user_segment"],
                    feature_name=row["feature_name"],
                    quantity=int(row["quantity"]),
                    unit_price_usd=float(row["unit_price_usd"]),
                    session_revenue_usd=float(row["session_revenue_usd"]),
                    tokens_used=int(row["tokens_used"]),
                    response_time_ms=int(row["response_time_ms"]),
                    feedback_score=int(row["feedback_score"]),
                    country=row["country"],
                )
            )

    return records

def total_revenue(records: Iterable[UsageRecord]) -> float:
    """ 
    Total revenue generated from all sessions. 
    """
    
    return sum(r.session_revenue_usd for r in records)

def group_by(records: Iterable[UsageRecord], key_func: Callable[[UsageRecord], str]) -> Dict[str, List[UsageRecord]]:
    """ 
    Group records using a key function.
    """
    
    groups: Dict[str, List[UsageRecord]] = defaultdict(list)
    for r in records:
        groups[key_func(r)].append(r)
    return groups

def revenue_by_user_segment(records: Iterable[UsageRecord]) -> Dict[str, float]:
    """ 
    Revenue grouped by user type. 
    """
    
    groups = group_by(records, lambda r: r.user_segment)
    return {segment: sum(r.session_revenue_usd for r in rows) for segment, rows in groups.items()}

def revenue_by_feature(records: Iterable[UsageRecord]) -> Dict[str, float]:
    """ 
    Revenue grouped by user type. 
    """
    
    groups = group_by(records, lambda r: r.feature_name)
    return {feature: sum(r.session_revenue_usd for r in rows) for feature, rows in groups.items()}

def avg_tokens_by_feature(records: Iterable[UsageRecord]) -> Dict[str, float]:
    """ 
    Average tokens used per feature. 
    """
        
    groups = group_by(records, lambda r: r.feature_name)
    return {feature: sum(r.tokens_used for r in rows) / len(rows) for feature, rows in groups.items()}

def top_n_features_by_revenue(records: Iterable[UsageRecord], n: int = 3) -> List[Tuple[str, float]]:
    """ 
    Top N AI features ranked by revenue. 
    """
    
    revenue_map = revenue_by_feature(records)
    return sorted(revenue_map.items(), key=lambda x: x[1], reverse=True)[:n]

def average_latency(records: Iterable[UsageRecord]) -> float:
    """ 
    Compute the overall average response time. 
    """
    
    if not records:
        return 0.0
    return sum(r.response_time_ms for r in records) / len(list(records))

def main() -> None:
    """ 
    Print analysis results for the reviewer. 
    """
    
    path = Path(__file__).with_name("sample_sales.csv")
    records = read_usage_csv(path)

    print("Total revenue:", total_revenue(records))

    print("\nRevenue by user segment:")
    for segment, value in revenue_by_user_segment(records).items():
        print(segment, round(value, 2))

    print("\nRevenue by feature:")
    for feature, value in revenue_by_feature(records).items():
        print(feature, round(value, 2))

    print("\nAverage tokens used per feature:")
    for feature, avg in avg_tokens_by_feature(records).items():
        print(feature, round(avg, 2))

    print("\nTop two revenue generating features:")
    for feature, value in top_n_features_by_revenue(records, 2):
        print(feature, round(value, 2))

    print("\nAverage response time (ms):", round(average_latency(records), 2))

if __name__ == "__main__":
    main()