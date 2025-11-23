"""
Unit tests for producer_consumer module.

Run with:
    pytest test_producer_consumer.py
"""

from typing import List
from producer_consumer import ProducerConsumer

def test_all_items_transferred_without_transform() -> None:
    source = [1, 2, 3, 4, 5]
    
    pipeline = ProducerConsumer(source_items=source)
    result: List[int] = pipeline.run()
        
    assert result == source

def test_all_items_transferred_with_transform() -> None:
    source = [1, 2, 3, 4]

    def double(x: int) -> int:
        return x * 2

    pipeline = ProducerConsumer(source_items=source, transform=double)
    result = pipeline.run()

    assert result == [2, 4, 6, 8]

def test_empty_source() -> None:
    source: list[int] = []
        
    pipeline = ProducerConsumer(source_items=source)
    result = pipeline.run()

    assert result == []

def test_queue_size_limit_does_not_block_forever() -> None:
    """
    This test makes sure the pipeline still works even when the queue size is very small.
    We are not testing speed or timing here. We only care that the pipeline finishes correctly and produces the expected output.
    """
    source = list(range(50))

    def square(x: int) -> int:
        return x * x

    pipeline = ProducerConsumer(source_items=source, transform=square, max_queue_size=3)
    result = pipeline.run()

    expected = [x * x for x in source]
    assert result == expected
    assert len(result) == len(source)