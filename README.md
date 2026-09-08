# MVAR

## Survey

The first step of this project consists of a **systematic literature review** focused on papers and scientific articles regarding current state-of-the-art frameworks.

The objective of this initial phase is to:
* **Map current frameworks:** Identify the main architectures and methodologies recently used.
* **Analyze attack types:** Catalog and characterize the attack vectors, exploitation strategies, and threat scenarios tested in each framework.
* **Identify gaps:** Compare existing approaches to detect weaknesses, limitations, and opportunities for improvement.

This review will serve as the technical foundation to support the decisions and development of the subsequent phases of the project.

## Project Structure

```text
Survey/
│
├── src/
│   │
│   ├── main.py
│   ├── config_loader.py
│   │
│   ├── config/
│   │   ├── search.yaml
│   │   └── sources.yaml
│   │
│   ├── models/
│   │   └── paper.py
│   │
│   ├── search/
│   │   ├── base.py
│   │   ├── factory.py
│   │   ├── openalex.py
│   │   ├── semantic_scholar.py
│   │   └── crossref.py
│   │
│   ├── utils/
│   │   └── abstract.py
│   │
│   └── processing/
│       ├── deduplication.py
│       ├── merge.py
│       └── filtering.py
│
├── .env
├── .env.example
├── requirements.txt
└── README.md
```

## Files Description

* `main.py` - Main entry point that runs the complete pipeline.
* `config_loader.py` - Loads configuration files and environment variables.
* `config/search.yaml` - Defines search queries and keywords.
* `config/sources.yaml` - Defines enabled data sources.
* `models/paper.py` - Defines the common Paper data model.
* `search/base.py` - Defines the common searcher interface.
* `search/factory.py` - Creates searchers based on configuration.
* `search/openalex.py` - Retrieves papers from OpenAlex API.
* `search/semantic_scholar.py` - Retrieves papers from Semantic Scholar API.
* `search/crossref.py` - Retrieves bibliographic metadata from Crossref API.
* `utils/abstract.py` - Cleans and normalizes paper abstracts.
* `processing/deduplication.py` - Removes duplicate papers from different sources.
* `processing/merge.py` - Combines information from multiple sources.
* `processing/filtering.py` - Applies PRISMA inclusion and exclusion criteria.
* `.env` - Stores private environment variables and API keys.
* `.env.example` - Example environment configuration without sensitive data.
* `requirements.txt` - Lists project dependencies.

## Pipeline Overview

```text
Search Configuration
        |
        v
OpenAlex / Semantic Scholar / Crossref
        |
        v
Paper Objects
        |
        v
Deduplication
        |
        v
Merge & Enrichment
        |
        v
PRISMA Filtering
        |
        v
Final Paper Dataset
```

## Data Sources

* OpenAlex API
* Semantic Scholar API
* Crossref API

## Goal

Automatically identify and analyze research papers about adversarial robustness frameworks, adversarial attacks, and robustness evaluation of image-based machine learning models.