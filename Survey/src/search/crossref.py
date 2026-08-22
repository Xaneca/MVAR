import requests

from models.paper import Paper
from .base import BaseSearcher


class CrossrefSearcher(BaseSearcher):

    BASE_URL = "https://api.crossref.org/works"

    def search(self, query: str):

        params = {
            "query": query,
            "rows": 10
        }

        response = requests.get(
            self.BASE_URL,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        papers = []

        for result in data["message"]["items"]:

            title = ""

            if result.get("title"):
                title = result["title"][0]

            authors = []

            for author in result.get("author", []):

                name = " ".join(filter(None, [
                    author.get("given"),
                    author.get("family")
                ]))

                authors.append(name)

            year = None

            if "published" in result:
                year = result["published"]["date-parts"][0][0]

            paper = Paper(
                title=title,
                authors=authors,
                abstract=result.get("abstract"),
                year=year,
                doi=result.get("DOI"),
                venue=result.get("container-title", [""])[0],
                source="Crossref"
            )

            papers.append(paper)

        return papers