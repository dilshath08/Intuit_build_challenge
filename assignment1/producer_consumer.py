"""
Producer consumer implementation using threads and a thread safe queue.

This module demonstrates:
* Thread synchronization
* Communication between producer and consumer
* Clean shutdown using a sentinel
"""

from __future__ import annotations
from queue import Queue
from threading import Thread
from typing import Iterable, List, Callable, Any, Optional

class ProducerConsumer:
    """
    Simple producer consumer pipeline using a shared queue.

    source_items: items to be produced
    transform: optional function to apply to each item before storing it in the destination
    max_queue_size: upper bound on queue size to avoid unbounded growth
    """

    # Sentinel object which is used to signal completion
    _SENTINEL = object()

    def __init__(
        self,
        source_items: Iterable[Any],
        transform: Optional[Callable[[Any], Any]] = None,
        max_queue_size: int = 100,
    ) -> None:
        self.source_items = list(source_items)
        self.transform = transform
        self.queue: Queue = Queue(maxsize=max_queue_size)
        self.destination: List[Any] = []

        self._producer_thread: Optional[Thread] = None
        self._consumer_thread: Optional[Thread] = None

    def _producer(self) -> None:
        """
        Reads from source_items and places items into the shared queue.
        Once done, puts a sentinel to notify the consumer that production is complete.
        """
        
        for item in self.source_items:
            self.queue.put(item)
        # Signal that production is complete
        self.queue.put(self._SENTINEL)

    def _consumer(self) -> None:
        """
        Reads items from the shared queue and stores them in destination.
        Stops when sentinel is received.
        """
        
        while True:
            item = self.queue.get()
            try:
                if item is self._SENTINEL:
                    return
                if self.transform is not None:
                    item = self.transform(item)
                self.destination.append(item)
            finally:
                self.queue.task_done()

    def run(self) -> List[Any]:
        """
        Starts producer and consumer threads, waits for them to finish,
        and returns the destination container.
        """
        
        self._producer_thread = Thread(target=self._producer, name="Producer", daemon=False)
        self._consumer_thread = Thread(target=self._consumer, name="Consumer", daemon=False)

        self._producer_thread.start()
        self._consumer_thread.start()

        self._producer_thread.join()

        self.queue.join()

        self._consumer_thread.join()

        return self.destination


def main() -> None:
    """
    Example
    """
    
    source = list(range(10))

    def square(x: int) -> int:
        return x * x

    pipeline = ProducerConsumer(source_items=source, transform=square, max_queue_size=5)
    result = pipeline.run()

    print("Source items:", source)
    print("Destination items:", result)


if __name__ == "__main__":
    main()