import os
import time

import requests
from dotenv import load_dotenv
from tqdm import tqdm

from models.paper import Paper
from .base import BaseSearcher

load_dotenv()


class ScopusSearcher(BaseSearcher):
    BASE_URL = "https://api.elsevier.com/content/search/scopus"
    RETRIES = 5
    PAGE_SIZE = 200
    QUERY_BATCH_SIZE = 10

    def __init__(self):
        self.api_key = os.getenv("SCOPUS_API_KEY", "").strip()
        self.inst_token = os.getenv("SCOPUS_INST_TOKEN", "").strip()

    def request_with_retry(self, params, stop_event):
        headers = {
            "X-ELS-APIKey": self.api_key,
            "Accept": "application/json",
        }
        if self.inst_token:
            headers["X-ELS-Insttoken"] = self.inst_token

        for attempt in range(self.RETRIES):
            if stop_event.is_set():
                return None

            response = requests.get(
                self.BASE_URL,
                params=params,
                headers=headers,
                timeout=30,
            )

            if response.status_code == 429 or response.status_code in (
                500, 502, 503, 504
            ):
                retry_after = response.headers.get("Retry-After")
                try:
                    wait_time = float(retry_after) if retry_after else 2 ** attempt
                except ValueError:
                    wait_time = 2 ** attempt

                tqdm.write(
                    f"Scopus HTTP {response.status_code}. "
                    f"Waiting {wait_time:g}s..."
                )
                if stop_event.wait(wait_time):
                    return None
                continue

            response.raise_for_status()
            return response

        tqdm.write("Skipping query after repeated Scopus request failures.")
        return None

    @staticmethod
    def _text(value):
        if isinstance(value, dict):
            value = value.get("$", "")
        return value.strip() if isinstance(value, str) else ""

    @classmethod
    def _keywords(cls, value):
        if not value:
            return []

        if isinstance(value, dict):
            value = value.get("author-keyword", value.get("$", []))

        if isinstance(value, str):
            return [item.strip() for item in value.split("|") if item.strip()]

        if isinstance(value, list):
            return [
                keyword
                for item in value
                if (keyword := cls._text(item))
            ]

        return []

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
                combined_query = " OR ".join(
                    f"({query})" for query in batch
                )
                papers.extend(self.search(combined_query, stop_event))

        except KeyboardInterrupt:
            print(f"\nStopping {self.__class__.__name__}")
            stop_event.set()
            raise

        return papers

    def search(self, query: str, stop_event):
        if stop_event.is_set():
            return []

        if not self.api_key:
            raise ValueError("SCOPUS_API_KEY is not configured in the environment.")

        params = {
            "query": query,
            "count": self.PAGE_SIZE,
            "start": 0,
            "view": "STANDARD",
        }

        response = self.request_with_retry(params, stop_event)
        if response is None:
            return []

        entries = response.json().get("search-results", {}).get("entry", [])
        if isinstance(entries, dict):
            entries = [entries]

        papers = []
        for result in entries:
            title = self._text(result.get("dc:title"))
            if not title:
                continue

            creator = self._text(result.get("dc:creator"))
            cover_date = self._text(result.get("prism:coverDate"))
            try:
                year = int(cover_date[:4]) if len(cover_date) >= 4 else None
            except ValueError:
                year = None

            doi = self._text(result.get("prism:doi")) or None
            identifier = self._text(result.get("dc:identifier"))
            scopus_id = identifier.removeprefix("SCOPUS_ID:") or None

            try:
                citations = int(result.get("citedby-count"))
            except (TypeError, ValueError):
                citations = None

            papers.append(Paper(
                id=doi or scopus_id,
                title=title,
                authors=[creator] if creator else [],
                abstract=self._text(result.get("dc:description")) or None,
                year=year,
                doi=doi,
                venue=self._text(result.get("prism:publicationName")) or None,
                keywords=self._keywords(result.get("authkeywords")),
                publication_type=(
                    self._text(result.get("subtypeDescription")) or None
                ),
                citations=citations,
                url=self._text(result.get("prism:url")) or None,
                sources=["Scopus"],
            ))

        return papers