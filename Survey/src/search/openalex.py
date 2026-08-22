import requests
from models.paper import Paper
from utils.abstract import reconstruct_abstract

from .base import BaseSearcher


class OpenAlexSearcher(BaseSearcher):

    BASE_URL = "https://api.openalex.org/works"

    def search(self, query: str):

        params = {
            "search": query,
            "per-page": 10
        }

        response = requests.get(
            self.BASE_URL,
            params=params,
            timeout=30
        )

        response.raise_for_status()

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
            j

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
                source="OpenAlex"
            )

            papers.append(paper)

        return papers