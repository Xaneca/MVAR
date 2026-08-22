import requests

from models.paper import Paper
from .base import BaseSearcher


class SemanticScholarSearcher(BaseSearcher):

    BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

    def search(self, query: str):

        params = {
            "query": query,
            "limit": 10,
            "fields": "title,authors,year,abstract,venue,externalIds"
        }

        response = requests.get(
            self.BASE_URL,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        papers = []

        for result in data.get("data", []):

            doi = None

            if result.get("externalIds"):
                doi = result["externalIds"].get("DOI")

            paper = Paper(
                title=result.get("title"),
                authors=[
                    author["name"]
                    for author in result.get("authors", [])
                ],
                abstract=result.get("abstract"),
                year=result.get("year"),
                doi=doi,
                venue=result.get("venue"),
                source="Semantic Scholar"
            )

            papers.append(paper)

        return papers