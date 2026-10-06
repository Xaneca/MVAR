import csv
import re
from pathlib import Path

def _paper_text(paper):
    fields = [
        paper.title,
        paper.abstract,
        " ".join(paper.keywords),
        " ".join(paper.concepts),
    ]
    return " ".join(field or "" for field in fields).lower()

def _contains_term(text, term):
    return re.search(rf"\b{re.escape(term.lower())}\b", text) is not None


def _clean_csv_text(value):
    if not value:
        return ""

    return re.sub(r"\s+", " ", str(value).replace("\\n", " ")).strip()

def filter_metadata(papers, config):

    filtered = []

    for paper in papers:

        if paper.year and paper.year < config["min_year"]:
            continue

        if config["require_abstract"]:
            if not paper.abstract:
                continue

        filtered.append(paper)

    return filtered

def filter_papers(papers, config):

    relevance = config["relevance"]
    required = config["keywords"]["required"]
    weights = relevance["weights"]
    minimum_score = relevance["minimum_score"]
    filtered = []

    for paper in papers:
        text = _paper_text(paper)
        missing_required = [
            term
            for term in required
            if not _contains_term(text, term)
        ]

        if missing_required:
            continue

        paper.score = sum(
            weight
            for term, weight in weights.items()
            if _contains_term(text, term)
        )

        if paper.score >= minimum_score:
            filtered.append(paper)

    return filtered


def create_screening_csv(papers, path, stage="title_abstract"):
    path = Path(path)
    existing = {}

    if path.exists():
        with path.open("r", encoding="utf-8", newline="") as file:
            for row in csv.DictReader(file):
                existing[row["paper_id"]] = row

    rows = []
    for paper in papers:
        paper_id = paper.doi or paper.id or paper.title
        row = existing.get(str(paper_id), {})
        row.update({
            "paper_id": str(paper_id),
            "score": paper.score,
            "title": _clean_csv_text(paper.title),
            "year": paper.year or "",
            "abstract": _clean_csv_text(paper.abstract),
            "stage": row.get("stage") or stage,
            "decision": _clean_csv_text(row.get("decision", "")),
            "reason": _clean_csv_text(row.get("reason", "")),
            "notes": _clean_csv_text(row.get("notes", "")),
        })
        rows.append(row)

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "paper_id",
                "score",
                "title",
                "year",
                "abstract",
                "stage",
                "decision",
                "reason",
                "notes",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)