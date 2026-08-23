from config_loader import load_search, load_sources
from search.factory import create_searchers
from models.paper import Paper
from pprint import pprint



def main():

    #####################################
    # EXTRACTION OF PAPERS FROM SOURCES #
    ######################################

    sources = load_sources()
    search = load_search()

    searchers = create_searchers(sources)

    queries = search["search"]["queries"]

    all_papers = []

    for searcher in searchers:
        print("-" * 50)
        print(f"\nSearching with {searcher.__class__.__name__}:\n")
        print("-" * 50)

        papers = searcher.search_all(queries)

        all_papers.extend(papers)

    print(f"\nFound {len(all_papers)} papers\n")

    for paper in all_papers[:10]:
        print(f"{paper.year} - {paper.title}")

    print("\nDETAILS\n")

    for paper in all_papers[:5]:
        print("-" * 50)
        print(paper)
    
    #############################
    # DEDUPLICATION AND MERGING #
    #############################


    ####################################
    # FILTERING AND RELEVANCE CHECKING #
    ####################################
        

if __name__ == "__main__":
    main()