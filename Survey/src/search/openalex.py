import os
import requests
import tqdm
from models.paper import Paper
from utils.abstract import reconstruct_abstract
import time
from .base import BaseSearcher
from dotenv import load_dotenv

load_dotenv()


class OpenAlexSearcher(BaseSearcher):

    BASE_URL = "https://api.openalex.org/works"

    def __init__(self):
        self.api_key = os.getenv("OPEN_ALEX_API_KEY")

    def request_with_retry(
        self,
        url,
        params,
        stop_event,
        retries=5
    ):

        for attempt in range(retries):

            response = requests.get(
                url,
                params=params,
                timeout=30
            )


            if response.status_code == 429:
                retry_after = response.headers.get(
                    "Retry-After"
                )

                if retry_after:
                    wait_time = int(retry_after)
                else:
                    wait_time = 2 ** attempt

                tqdm.write(
                    f"OpenAlex rate limit. "
                    f"Waiting {wait_time}s..."
                )

                if stop_event.wait(wait_time):
                    return None

                continue


            response.raise_for_status()

            return response

        tqdm.write(
            "Skipping query due to repeated OpenAlex rate limits."
        )

        return None

    def search(self, query: str, stop_event):

        params = {
            "search": query,
            "per-page": 10,
            "api-key": self.api_key,
        }

        response = self.request_with_retry(
            self.BASE_URL,
            params=params,
            stop_event=stop_event,
            retries=5
        )

        if response is None:
            return []

        data = response.json()

        papers = []

        for result in data["results"]:

            authors = [
                author["author"]["display_name"]
                for author in result.get("authorships", [])
                if author.get("author")
            ]

            # Venue
            venue = None
            if result.get("primary_location"):
                if result["primary_location"].get("source"):
                    venue = result["primary_location"]["source"].get("display_name")

            # Concepts
            concepts = [
                concept["display_name"]
                for concept in result.get("concepts", [])
            ]

            # Keywords
            keywords = [
                keyword["display_name"]
                for keyword in result.get("keywords", [])
            ]

            # Publication type
            publication_type = result.get("type")

            # Abstract reconstruction
            abstract = reconstruct_abstract(
                result.get("abstract_inverted_index")
            )

            paper = Paper(
                id = result.get("id"),
                title=result.get("display_name"),
                authors=authors,
                abstract=abstract,
                year=result.get("publication_year"),
                doi=result.get("doi"),
                venue=venue,
                concepts=concepts,
                keywords=keywords,
                publication_type=publication_type,
                citations=result.get("cited_by_count"),
                url=result.get("id"),
                sources=["OpenAlex"]
            )

            papers.append(paper)

        return papers