import os
import signal
from re import search

from config_loader import load_search, load_sources
from search.factory import create_searchers
from models.paper import Paper
from pprint import pprint
from dotenv import load_dotenv
from processing.deduplication import deduplicate_papers
from cache.manager import (create_hash, load_cache, save_cache)
from search.manager import search_all_sources # threads - run api queries at same time
from search.query_builder import build_queries

def stop_on_interrupt(signum, frame):
    print("\nExecution interrupted by user.", flush=True)
    os._exit(130)


def main():

    signal.signal(signal.SIGINT, stop_on_interrupt)

    #####################################
    # EXTRACTION OF PAPERS FROM SOURCES #
    #####################################

    load_dotenv()

    sources = load_sources()
    search = load_search()

    # queries 
    groups = search["search"]["groups"]
    templates = search["search"]["templates"]
    queries = build_queries(
        groups,
        templates
    )


    ### CACHE MANAGEMENT ###

    cache_config = {
        "search": search,
        "sources": sources
    }

    cache_key = create_hash(cache_config)

    cached = load_cache(cache_key, folder="raw")


    if cached is not None:

        print("Loading papers from cache")

        all_papers = [
            Paper.from_dict(paper)
            for paper in cached
        ]

    else:

        print("Searching APIs")

        searchers = create_searchers(sources)
        for i, searcher in enumerate(searchers):    # progress bar position for each searcher
            searcher.position = i
        
        # parallel search using threads
        all_papers = search_all_sources(
            searchers,
            queries
        )

        save_cache(
            cache_key,
            [
                paper.to_dict()
                for paper in all_papers
            ], folder="raw"
        )


    print(f"\nFound {len(all_papers)} papers\n")

    for paper in all_papers[:10]:

        print(
            f"{paper.year} - {paper.title}"
        )
    
    #############################
    # DEDUPLICATION AND MERGING #
    #############################
    unique_papers = deduplicate_papers(
        all_papers
    )

    print(f"Before: {len(all_papers)}")
    print(f"After: {len(unique_papers)}")

    save_cache(
        cache_key,
        [
            paper.to_dict()
            for paper in unique_papers
        ], folder="processed"
    )


    ####################################
    # FILTERING AND RELEVANCE CHECKING #
    ####################################
    
        

if __name__ == "__main__":
    main()