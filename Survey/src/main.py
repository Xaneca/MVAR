from config_loader import load_search, load_sources
from search.factory import create_searchers
from models.paper import Paper
from pprint import pprint
from dotenv import load_dotenv
from processing.deduplication import deduplicate_papers
from cache.manager import (create_hash, load_cache, save_cache)


def main():

    #####################################
    # EXTRACTION OF PAPERS FROM SOURCES #
    #####################################

    load_dotenv()

    sources = load_sources()
    search = load_search()

    queries = search["search"]["queries"]


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

        all_papers = []

        for searcher in searchers:

            print("-" * 50)
            print(
                f"\nSearching with {searcher.__class__.__name__}:\n"
            )
            print("-" * 50)

            papers = searcher.search_all(queries)

            all_papers.extend(papers)


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