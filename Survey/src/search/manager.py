from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
import os
from threading import Event

stop_event = Event()

def run_search(searcher, queries):
    return searcher.search_all(queries, stop_event)

def search_all_sources(searchers, queries):

    all_papers = []
    executor = ThreadPoolExecutor(
        max_workers=len(searchers)
    )

    try:
        futures = [
            executor.submit(
                run_search,
                searcher,
                queries
            )
            for searcher in searchers
        ]

        pending = set(futures)
        while pending:
            done, pending = wait(
                pending,
                timeout=0.2,
                return_when=FIRST_COMPLETED
            )

            for future in done:
                all_papers.extend(future.result())

    except KeyboardInterrupt:

        print("\nSearch interrupted by user.", flush=True)
        stop_event.set()

        for future in futures:
            future.cancel()

        executor.shutdown(wait=False, cancel_futures=True)
        os._exit(130)

    executor.shutdown(wait=True)

    return all_papers