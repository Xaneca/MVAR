from config_loader import load_search, load_sources
from search.factory import create_searchers
from models.paper import Paper
from pprint import pprint


def main():

    sources = load_sources()
    search = load_search()

    searchers = create_searchers(sources)

    queries = search['search']["queries"]

    for searcher in searchers:

        papers = searcher.search_all(queries)

        print(f"\nFound {len(papers)} papers\n")

        for paper in papers:
            print(f"{paper.year} - {paper.title}")
    
    for paper in papers[:5]:
        print("-" * 50)
        print(paper)
        

if __name__ == "__main__":
    main()