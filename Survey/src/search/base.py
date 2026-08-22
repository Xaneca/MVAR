from abc import ABC, abstractmethod


class BaseSearcher(ABC):
    """Base class for all search engines."""

    @abstractmethod
    def search(self, query: str):
        """
        Search papers.

        Returns
        -------
        list
            List of papers.
        """
        raise NotImplementedError
    
    def search_all(self, queries: list[str]):
        """Search using multiple queries."""

        papers = []

        for query in queries:
            print(f"Searching: {query}")
            papers.extend(self.search(query))

        return papers