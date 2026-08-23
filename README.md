# MVAR

## Survey

The first step of this project consists of a **systematic literature review** focused on papers and scientific articles regarding current state-of-the-art frameworks.

The objective of this initial phase is to:
* **Map current frameworks:** Identify the main architectures and methodologies recently used.
* **Analyze attack types:** Catalog and characterize the attack vectors, exploitation strategies, and threat scenarios tested in each framework.
* **Identify gaps:** Compare existing approaches to detect weaknesses, limitations, and opportunities for improvement.

This review will serve as the technical foundation to support the decisions and development of the subsequent phases of the project.

Survey/
│
├── search.py          # pesquisa nas APIs
├── filter.py          # remove duplicados e filtra
├── classify.py        # classifica por tema
├── prisma_stats.py    # gera números para o PRISMA
├── papers.csv
├── selected.csv
└── figures/
    └── prisma.png

src/
│
├── models/
│   └── paper.py
│
├── search/
│   ├── base.py
│   ├── openalex.py
│   ├── semantic_scholar.py
│   └── crossref.py
│
├── filters/
│   ├── year.py
│   └── keywords.py
│
├── utils/
│   ├── abstract.py
│   └── text.py
│
└── main.py


---------

**Target Pipeline:**
    Config
        ↓
    OpenAlex
    Semantic Scholar
    Crossref
    IEEE
    ACM
        ↓
    All papers
        ↓
    Normalization (Paper)
        ↓
    Remove Duplicates
        ↓
    Filters
        ↓
    CSV