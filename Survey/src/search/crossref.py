import requests
import time

from models.paper import Paper
from .base import BaseSearcher
from utils.abstract import clean_abstract


class CrossrefSearcher(BaseSearcher):

    BASE_URL = "https://api.crossref.org/works"

    def search(self, query: str):

        params = {
            "query": query,
            "rows": 10,

        }

        headers = {
            "User-Agent": (
                "MVAR-Systematic-Review/1.0 "
                "(mailto:alexandramarques@student.dei.uc.pt )"
            )
        }

        response = requests.get(
            self.BASE_URL,
            params=params,
            headers=headers,
            timeout=30
        )

        time.sleep(1)

        response.raise_for_status()

        data = response.json()

        papers = []

        for result in data["message"]["items"]:

            title = None

            if result.get("title"):
                title = result["title"][0]
            if not title:
                continue

            authors = []

            for author in result.get("author", []):

                name = " ".join(
                    filter(
                        None,
                        [
                            author.get("given"),
                            author.get("family")
                        ]
                    )
                )

                authors.append(name)


            year = None

            issued = result.get("issued")

            if issued:

                date_parts = issued.get("date-parts")

                if date_parts:
                    year = date_parts[0][0]


            venue = None

            if result.get("container-title"):
                venue = result["container-title"][0]


            paper = Paper(
                id=result.get("DOI"),
                title=title,
                authors=authors,
                abstract=clean_abstract(result.get("abstract")),
                year=year,
                doi=result.get("DOI"),
                venue=venue,
                concepts=[],
                keywords=[],
                publication_type=result.get("type"),
                citations=result.get("is-referenced-by-count"),
                url=f"https://doi.org/{result.get('DOI')}" if result.get("DOI") else None,
                sources=["Crossref"]
            )

            papers.append(paper)

        return papers