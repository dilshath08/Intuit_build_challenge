# Intuit Build Challenge - Python Solution  
Author: Dilshath Shaik  

## Overview

This repo has complete solution for the Intuit Build Challenge. There are two assignments:

- **Assignment 1**: Producer-consumer pipeline with thread synchronization
- **Assignment 2**: Functional-style data analysis on CSV sales data

Both assignments have working code, unit tests, sample data, and console outputs included.

---

## Getting Started

### Requirements

- Python 3.9+
- pytest for running tests

### Setup

Clone this repo:

```bash
git clone https://github.com/yourusername/intuit-build-challenge.git
cd intuit-build-challenge
```

Using a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

Install pytest:

```bash
pip install pytest
```

---

## Assignment 1 - Producer and Consumer Pipeline

### The Problem

Build a producer-consumer system using threads. One thread produces items and puts them in a queue, another thread consumes items from that queue. The challenge is getting them to work together without race conditions or deadlocks.

### How to solve

Use Python's built-in `queue.Queue` which handles thread safety automatically. The key decisions:

**Sentinel for shutdown**: Instead of using timeouts or killing threads, send a special sentinel value when production is done. This guarantees the consumer processes every item before exiting.

**Bounded queue**: The queue has a max size (set it to 5 in the example, but it's configurable). When the queue fills up, the producer blocks. This prevents memory issues if the producer is way faster than the consumer.

Here's how the flow works:
1. Producer reads from source list
2. Puts each item in the queue
3. Consumer takes items from queue
4. Applies the transform (if provided)
5. Stores result in destination list
6. When done, producer sends sentinel
7. Consumer sees sentinel and exits
8. Main thread waits for both to finish

### Running Assignment - 1

```bash
cd assignment1
python producer_consumer.py
```

#### Output:

```
Source items: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
Destination items: [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

Each number gets squared: 0→0, 1→1, 2→4, 3→9, etc.


### Tests

```bash
pytest test_producer_consumer.py -v
```

Contains 4 tests covering:
- Basic transfer without any transformation
- Transfer with transformation (squaring)
- Edge case: empty source
- Stress test: tiny queue (3 items) with 50 items of data

That last one is important - it makes sure the system doesn't deadlock when the queue is much smaller than the data.

#### Expected output:

```
============================= test session starts plugins: anyio-3.5.0, xdoctest-1.1.5
collected 4 items                                                              

test_producer_consumer.py::test_all_items_transferred_without_transform PASSED [ 25%]
test_producer_consumer.py::test_all_items_transferred_with_transform PASSED [ 50%]
test_producer_consumer.py::test_empty_source PASSED                      [ 75%]
test_producer_consumer.py::test_queue_size_limit_does_not_block_forever PASSED [100%]

============================== 4 passed in 0.03s ===============================

```

### Technical Details

The synchronization happens through these queue methods:
- `queue.put()` - blocks if queue is full
- `queue.get()` - blocks if queue is empty
- `queue.task_done()` - marks item as processed
- `queue.join()` - waits until all items are processed

Use three joins to ensure clean shutdown:
1. Wait for producer to finish
2. Wait for queue to be empty
3. Wait for consumer to exit

---

## Assignment 2 - Sales Data Analysis

### The Problem

This assignment performs functional-style grouping and aggregation operations on CSV sales data. The program reads data from a CSV file and executes multiple analytical queries using functional programming paradigms.

### Dataset Choice

Create a dataset that models a SaaS product with AI features. Each row is a billable API call. Here's why this works well:

- It has both money metrics (revenue, pricing) and technical metrics (tokens, latency)
- Supports interesting grouping (by user tier, by feature, by country)
- Represents a real business scenario
- Makes the analysis results actually meaningful

The CSV has 10 transactions with these fields:

| Field | Type | What It Is |
|-------|------|------------|
| transaction_id | string | Unique ID like "T1001" |
| date | date | When it happened (YYYY-MM-DD) |
| user_segment | string | "free" or "premium" |
| feature_name | string | Which AI feature: smart_reply, translation, data_extraction, document_summary |
| quantity | int | Always 1 here |
| unit_price_usd | float | Price per call |
| session_revenue_usd | float | Total revenue (qty × price) |
| tokens_used | int | Computational cost |
| response_time_ms | int | How long it took |
| feedback_score | int | User rating 1-5 |
| country | string | US, CA, UK, IN |

### What the Analysis Does

Implement 6 different analyses:

1. **Total revenue** - sum everything
2. **Revenue by user segment** - free vs premium
3. **Revenue by feature** - which features make money
4. **Average tokens per feature** - computational cost
5. **Top N features** - ranked by revenue
6. **Average response time** - performance metric

All of these use functional programming - lambdas, map/filter concepts, grouping operations. Wrote a reusable `group_by` function that takes a key function, so we can group by any field without repeating code.

### Running Assignment - 2

```bash
cd assignment2
python analysis.py
```

#### Output:

```
Total revenue: 40.0

Revenue by user segment:
free 0.0
premium 40.0

Revenue by feature:
smart_reply 10.0
data_extraction 10.0
translation 0.0
document_summary 20.0

Average tokens used per feature:
smart_reply 132.5
data_extraction 815.0
translation 190.0
document_summary 1000.0

Top two revenue generating features:
document_summary 20.0
smart_reply 10.0

Average response time (ms): 638.0
```

### What These Numbers Mean

**Total: $40** - Only premium users generate revenue. Free users pay nothing.

**By segment**: All revenue comes from premium tier. Free tier is 40% of usage but $0 revenue. Classic freemium model.

**By feature**: `document_summary` is the winner at $20. It's priced at $10/call vs $5/call for other features. `translation` made nothing because only free users tried it.

**Token usage**: Shows computational cost per feature:
- `document_summary`: 1000 tokens (expensive to run)
- `data_extraction`: 815 tokens
- `translation`: 190 tokens  
- `smart_reply`: 132.5 tokens (cheapest)

So `document_summary` makes the most money but also costs the most to provide.


### Tests

```bash
pytest test_analysis.py -v
```

Contains 7 tests covering:
- CSV parsing works correctly
- Revenue calculations are accurate
- Grouping by segment works
- Grouping by feature works
- Averages are computed right
- Top N ranking works
- Latency calculation is correct

#### Expected output:

```
============================= test session starts ==============================
plugins: anyio-3.5.0, xdoctest-1.1.5
collected 7 items                                                              

test_analysis.py::test_read_usage_csv_loads_all_rows PASSED              [ 14%]
test_analysis.py::test_total_revenue PASSED                              [ 28%]
test_analysis.py::test_revenue_by_user_segment PASSED                    [ 42%]
test_analysis.py::test_revenue_by_feature PASSED                         [ 57%]
test_analysis.py::test_avg_tokens_by_feature PASSED                      [ 71%]
test_analysis.py::test_top_n_features_by_revenue PASSED                  [ 85%]
test_analysis.py::test_average_latency PASSED                            [100%]

============================== 7 passed in 0.03s ===============================```

## Running All Tests

From the repo root:

```bash
pytest -v
```

This runs both test suites.

---

## Project Structure

```
Intuit_build_challenge/
    assignment1/
        producer_consumer.py      # Main implementation
        test_producer_consumer.py # Tests

    assignment2/
        sample_sales.csv          # Dataset (10 rows)
        analysis.py               # Main implementation
        test_analysis.py          # Tests

    README.md
```

---