import re


def normalize_title(title):

    if not title:
        return ""

    title = title.lower()

    title = re.sub(
        r"[^a-z0-9\s]",
        "",
        title
    )

    title = " ".join(
        title.split()
    )

    return title

def normalize_doi(doi):

    if not doi:
        return None

    doi = doi.lower().strip()

    doi = doi.replace(
        "https://doi.org/", # https
        ""
    )

    doi = doi.replace(
        "http://doi.org/",  # http
        ""
    )

    return doi

def merge_papers(existing, new):
    if not existing.abstract and new.abstract:
        existing.abstract = new.abstract

    if not existing.venue and new.venue:
        existing.venue = new.venue

    if not existing.year and new.year:
        existing.year = new.year

    if not existing.doi and new.doi:
        existing.doi = new.doi

    if not existing.url and new.url:
        existing.url = new.url

    if not existing.publication_type and new.publication_type:
        existing.publication_type = new.publication_type

    existing.authors = list(
        dict.fromkeys(
            existing.authors + new.authors
        )
    )

    existing.concepts = list(
        dict.fromkeys(
            existing.concepts + new.concepts
        )
    )

    existing.keywords = list(
        dict.fromkeys(
            existing.keywords + new.keywords
        )
    )

    existing.citations = max(
        existing.citations or 0,
        new.citations or 0
    )

    for source in new.sources:
        if source not in existing.sources:

            existing.sources.append(source)

def deduplicate_papers(papers):

    unique = {}
    duplicates = 0

    for paper in papers:

        key = None

        # Primeiro tenta DOI
        if paper.doi:
            key = normalize_doi(paper.doi)
        # Se não tiver DOI usa título
        else:
            key = normalize_title(paper.title)

        if key not in unique:
            unique[key] = paper
        else:
            existing = unique[key]
            duplicates += 1

            merge_papers(
                unique[key],
                paper
            )
    print(f"Duplicates merged: {duplicates}")

    return list(unique.values())