from concurrent.futures import ThreadPoolExecutor

def run_search(searcher, queries):

    return searcher.search_all(queries)


def search_all_sources(searchers, queries):

    all_papers = []

    with ThreadPoolExecutor(
        max_workers=len(searchers)
    ) as executor:

        futures = [
            executor.submit(
                run_search,
                searcher,
                queries
            )
            for searcher in searchers
        ]

        for future in futures:
            all_papers.extend(
                future.result()
            )

    return all_papers