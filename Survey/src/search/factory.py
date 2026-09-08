import os
from .openalex import OpenAlexSearcher
from .semantic_scholar import SemanticScholarSearcher
from .crossref import CrossrefSearcher


def create_searchers(sources_config):

    searchers = []

    sources = sources_config["sources"]

    if sources["openalex"]["enabled"]:
        searchers.append(OpenAlexSearcher())

    if sources["semantic_scholar"]["enabled"]:
        api_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
        searchers.append(SemanticScholarSearcher(api_key))

    if sources["crossref"]["enabled"]:
        searchers.append(CrossrefSearcher())

    return searchers