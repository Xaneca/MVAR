import os

import requests
from dotenv import load_dotenv
from tqdm import tqdm

from models.paper import Paper
from .base import BaseSearcher

from pprint import pprint


load_dotenv()

class IEEESearcher(BaseSearcher):
    QUERY_BATCH_SIZE = 10

    BASE_URL = "https://ieeexploreapi.ieee.org/api/v1/search/articles"

    def __init__(self):
        self.api_key = os.getenv("IEEE_API_KEY", "").strip()
        self.disabled = False

    def search_all(self, queries, stop_event):
        papers = []

        try:
            for start in tqdm(
                range(0, len(queries), self.QUERY_BATCH_SIZE),
                desc=self.__class__.__name__,
                position=self.position,
                leave=True,
            ):
                if stop_event.is_set():
                    break

                batch = queries[start:start + self.QUERY_BATCH_SIZE]
                combined_query = " OR ".join(f"({query})" for query in batch)
                papers.extend(self.search(combined_query, stop_event))

        except KeyboardInterrupt:
            print(f"\nStopping {self.__class__.__name__}")
            stop_event.set()
            raise

        return papers

    def request_with_retry(
        self,
        params,
        stop_event,
        retries=5
    ):

        for attempt in range(retries):

            if stop_event.is_set():
                return None

            response = requests.get(
                self.BASE_URL,
                params=params,
                timeout=30
            )

            if response.status_code == 429:
                wait_time = 2 ** attempt
                tqdm.write(
                    f"IEEE rate limit. Waiting {wait_time}s..."
                )

                if stop_event.wait(wait_time):
                    return None

                continue

            if response.status_code in (401, 403):
                tqdm.write(
                    "IEEE API rejected IEEE_API_KEY (HTTP "
                    f"{response.status_code}). IEEE search disabled."
                )
                self.disabled = True
                return None

            response.raise_for_status()
            return response

        tqdm.write("Skipping query due to repeated IEEE rate limits.")
        return None

    def search(self, query: str, stop_event):

        if self.disabled or stop_event.is_set():
            return []

        if not self.api_key:
            raise ValueError(
                "IEEE_API_KEY is not configured in the environment."
            )

        params = {
            "apikey": self.api_key,
            "querytext": query,
            "max_records": 200,
            "start_record": 1,
        }

        response = self.request_with_retry(
            params=params,
            stop_event=stop_event
        )

        if response is None:
            return []

        data = response.json()
        
        papers = []

        for result in data.get("articles", []):
            authors = []
            for author in result.get("authors", []):
                if isinstance(author, str):
                    name = author.strip()
                elif isinstance(author, dict):
                    name = author.get("full_name") or author.get("name") or ""
                    name = name.strip() if isinstance(name, str) else ""
                else:
                    continue

                if name:
                    authors.append(name)

            index_terms = result.get("index_terms") or {}
            keywords = []

            for group in (
                index_terms.get("author_terms", []),
                index_terms.get("ieee_terms", []),
            ):
                for term in group:
                    if isinstance(term, str):
                        keyword = term.strip()
                    elif isinstance(term, dict):
                        keyword = term.get("term", "")
                        keyword = keyword.strip() if isinstance(keyword, str) else ""
                    else:
                        continue

                    if keyword:
                        keywords.append(keyword)

            doi = result.get("doi")
            article_number = result.get("article_number")

            papers.append(Paper(
                id=doi or article_number,
                title=result.get("title", ""),
                authors=authors,
                abstract=result.get("abstract"),
                year=result.get("publication_year"),
                doi=doi,
                venue=result.get("publication_title"),
                keywords=keywords,
                publication_type=result.get("content_type"),
                citations=result.get("citing_paper_count"),
                url=result.get("html_url") or result.get("pdf_url"),
                sources=["IEEE"]
            ))

        return papers
