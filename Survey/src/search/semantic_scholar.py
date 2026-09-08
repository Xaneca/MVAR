import requests
import time

from models.paper import Paper
from .base import BaseSearcher

class SemanticScholarSearcher(BaseSearcher):

    BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

    def __init__(self, api_key=None):
        self.api_key = api_key

    def request_with_retry(self, url, params, headers, retries=5):

        for attempt in range(retries):

            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=30
            )

            if response.status_code == 429:

                wait_time = 2 ** attempt

                print(
                    f"Semantic Scholar rate limit. "
                    f"Waiting {wait_time}s..."
                )

                time.sleep(wait_time)

                continue

            response.raise_for_status()
            return response
        
        print("Skipping query due to repeated rate limits.")
        return None

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


        headers = {}

        if self.api_key:
            headers["x-api-key"] = self.api_key


        time.sleep(2)

        response = self.request_with_retry(
            self.BASE_URL,
            headers=headers,
            params=params,
            retries=5
        )

        if response is None:
            return []

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
                abstract=result.get("abstract"),
                year=result.get("year"),
                doi=doi,
                venue=result.get("venue"),
                citations=result.get("citationCount"),
                sources=["Semantic Scholar"]
            )

            papers.append(paper)

        return papers