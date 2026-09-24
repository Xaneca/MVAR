from abc import ABC, abstractmethod
import time
from tqdm import tqdm


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
    
    def search_all(self, queries: list[str], stop_event):
        """Search using multiple queries."""

        papers = []

        # for query in queries:
        #     print(f"Searching: {query}")
        #     papers.extend(self.search(query))

        try:

            for query in tqdm(
                queries,
                desc=self.__class__.__name__,
                position=self.position,
                leave=True
            ):

                if stop_event.is_set():
                    break


                papers.extend(
                    self.search(query, stop_event)
                )

        except KeyboardInterrupt:

            print(
                f"\nStopping {self.__class__.__name__}"
            )

            stop_event.set()

            raise

        return papers