import os

from .scopus import ScopusSearcher
from .openalex import OpenAlexSearcher
from .semantic_scholar import SemanticScholarSearcher
from .crossref import CrossrefSearcher
from .ieee import IEEESearcher


def create_searchers(sources_config):

    searchers = []

    sources = sources_config["sources"]

    if sources["openalex"]["enabled"]:
        searchers.append(OpenAlexSearcher())

    if sources["semantic_scholar"]["enabled"]:
        searchers.append(SemanticScholarSearcher())

    if sources["crossref"]["enabled"]:
        searchers.append(CrossrefSearcher())

    if sources["ieee"]["enabled"]:
        searchers.append(IEEESearcher())
        
    if sources["scopus"]["enabled"]:
        searchers.append(ScopusSearcher())

    # if sources["acm"]["enabled"]:
        # searchers.append(ACMSearcher())

    return searchers