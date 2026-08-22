from dataclasses import dataclass, field

@dataclass
class Paper:

    id: str | None = None
    title: str = ""
    authors: list[str] = field(default_factory=list)
    abstract: str | None = None
    year: int | None = None
    doi: str | None = None                              # for deduplication
    venue: str | None = None                            # final analysis
    keywords: list[str] = field(default_factory=list)   # filter relevance
    concepts: list[str] = field(default_factory=list)   # filter area
    publication_type: str | None = None
    citations: int | None = None                        # literature review
    url: str | None = None
    source: str | None = None