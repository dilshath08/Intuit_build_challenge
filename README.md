# Intuit Build Challenge - Python Solution  
Author: Dilshath Shaik  

## 1. Overview

This repository contains complete solutions for the Intuit Build Challenge. The challenge consists of two assignments:

- Assignment 1: Implement a thread-synchronized producer–consumer pipeline using a blocking queue.
- Assignment 2: Perform functional-style grouping and aggregation on CSV sales data.

Both assignments include complete source code, unit tests, datasets, instructions, and sample console output.

---

## 2. Assignment 1 - Producer and Consumer Pipeline

### 2.1 Problem Summary

This assignment implements a producer-consumer system using Python threads.  
A producer thread places items into a shared queue, and a consumer thread retrieves and processes them.

A sentinel value is used to signal the consumer when all production is finished. This is the cleanest approach for terminating worker threads without busy waiting or timeouts.

### 2.2 How It Works

- Producer reads items, applies an optional transform, and places items into a `queue.Queue()`.
- Consumer reads items until it encounters the sentinel, then exits cleanly.
- A destination list collects processed items.

### 2.3 Directory Structure

```
assignment1/
    producer_consumer.py
    test_producer_consumer.py
```

### 2.4 Running Assignment 1

```
cd assignment1
python producer_consumer.py
```

### 2.5 Sample Output

```
Source items: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
Destination items: [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

### 2.6 Running Unit Tests

```
pytest test_producer_consumer.py
```

Expected:

```
============================= test session starts ==============================
platform darwin -- Python 3.9.12, pytest-7.1.1, pluggy-1.0.0
rootdir: /Intuit_build_challenge/assignment1
plugins: anyio-3.5.0, xdoctest-1.1.5
collected 4 items                                                              

test_producer_consumer.py ....                                           [100%]

============================== 4 passed in 0.03s ===============================

```

---

## 3. Assignment 2 - Sales Data Analysis (Functional Programming)

### 3.1 Dataset Description

The dataset `sample_sales.csv` models AI feature usage transactions. Each row represents a monetizable session and includes:

- transaction_id  
- date  
- user_segment  
- feature_name  
- quantity  
- unit_price_usd  
- session_revenue_usd  
- tokens_used  
- response_time_ms  
- feedback_score  
- country  

This dataset supports grouping, aggregation, and stream-based transformations.

### 3.2 Analyses Implemented

- Total revenue  
- Revenue by user segment  
- Revenue by feature  
- Average tokens per feature  
- Top N revenue-generating features  
- Average response latency  

### 3.3 Directory Structure

```
assignment2/
    sample_sales.csv
    analysis.py
    test_analysis.py
```

### 3.4 Running Assignment 2

```
cd assignment2
python analysis.py
```

### 3.5 Sample Output

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

### 3.6 Running Unit Tests

```
pytest test_analysis.py
```

Expected:

```
============================= test session starts ==============================
platform darwin -- Python 3.9.12, pytest-7.1.1, pluggy-1.0.0
rootdir: /Intuit_build_challenge/assignment2
plugins: anyio-3.5.0, xdoctest-1.1.5
collected 7 items                                                              

test_analysis.py .......                                                 [100%]

============================== 7 passed in 0.05s ===============================

```

---

## 4. Deliverables Checklist

- Public GitHub repository URL  
- Complete source code for both assignments  
- Unit tests for all analysis methods  
- README with setup instructions and sample outputs  
- Console outputs included in documentation  

---

## 5. Repository Structure

```
Intuit_build_challenge/
    assignment1/
        producer_consumer.py
        test_producer_consumer.py

    assignment2/
        sample_sales.csv
        analysis.py
        test_analysis.py

    README.md
```

---

## 6. Notes

- Assignment 1 demonstrates thread synchronization, queue-based communication, and safe shutdown using a sentinel.
- Assignment 2 demonstrates functional aggregation, grouping, and analysis techniques on structured CSV data.
- All components include complete unit test coverage.
