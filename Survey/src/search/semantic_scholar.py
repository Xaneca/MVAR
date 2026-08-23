import requests
import time

from models.paper import Paper
from .base import BaseSearcher

def request_with_retry(url, params, retries=5):

    for attempt in range(retries):

        response = requests.get(
            url,
            params=params,
            timeout=30
        )

        if response.status_code == 429:
            wait_time = 10 * (attempt + 1)

            print(
                f"Semantic Scholar rate limit. Waiting {wait_time}s..."
            )

            time.sleep(wait_time)

            continue

        response.raise_for_status()

        return response

    raise Exception(
        "Semantic Scholar unavailable after retries"
    )


class SemanticScholarSearcher(BaseSearcher):

    BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

    def search(self, query: str):

        params = {
            "query": query,
            "limit": 10,
            "fields": (
                "title,"
                "authors,"
                "year,"
                "abstract,"
                "venue,"
                "externalIds,"
                "citationCount"
            )
        }

        response = request_with_retry(
            self.BASE_URL,
            params
        )

        print(response.status_code)
        print(response.text[:500]) 
        response.raise_for_status()

        data = response.json()

        papers = []

        for result in data.get("data", []):

            authors = [
                author["name"]
                for author in result.get("authors", [])
            ]

            doi = None

            external_ids = result.get("externalIds")

            if external_ids:
                doi = external_ids.get("DOI")

            paper = Paper(
                title=result.get("title"),
                authors=authors,
                # abstract=result.get("abstract"),
                year=result.get("year"),
                doi=doi,
                venue=result.get("venue"),
                citations=result.get("citationCount"),
                sources=["Semantic Scholar"]
            )

            papers.append(paper)

        return papers