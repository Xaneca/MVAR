# MVAR

## Survey

The first step of this project consists of a **systematic literature review** focused on papers and scientific articles regarding current state-of-the-art frameworks.

The objective of this initial phase is to:
* **Map current frameworks:** Identify the main architectures and methodologies recently used.
* **Analyze attack types:** Catalog and characterize the attack vectors, exploitation strategies, and threat scenarios tested in each framework.
* **Identify gaps:** Compare existing approaches to detect weaknesses, limitations, and opportunities for improvement.

This review will serve as the technical foundation to support the decisions and development of the subsequent phases of the project.

## Project Structure

Survey/
│
├── src/
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


## Files Description

main.py  
Main entry point that runs the paper collection pipeline.

config_loader.py  
Loads configuration files and environment variables.

config/search.yaml  
Defines search queries and keyword configurations.

config/sources.yaml  
Controls which external databases are enabled.

models/paper.py  
Defines the common Paper data structure used by all APIs.

search/base.py  
Defines the common interface for all search engines.

search/factory.py  
Creates searcher instances according to configuration.

search/openalex.py  
Retrieves papers and metadata from OpenAlex API.

search/semantic_scholar.py  
Retrieves papers and metadata from Semantic Scholar API.

search/crossref.py  
Retrieves bibliographic metadata from Crossref API.

utils/abstract.py  
Cleans and normalizes paper abstracts.

processing/deduplication.py  
Removes duplicate papers collected from different sources.

processing/merge.py  
Combines information from multiple sources into a single paper record.

processing/filtering.py  
Applies PRISMA-based inclusion and exclusion criteria.

.env  
Stores private environment variables such as API keys.

.env.example  
Example environment configuration without sensitive information.

requirements.txt  
Lists all Python dependencies required by the project.


## Pipeline Overview

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


## Data Sources

- OpenAlex API
- Semantic Scholar API
- Crossref API


## Goal

Automatically identify and analyze research papers about adversarial robustness frameworks, adversarial attacks, and robustness evaluation of image-based machine learning models.