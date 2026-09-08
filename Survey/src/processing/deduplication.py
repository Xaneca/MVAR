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



def deduplicate_papers(papers):

    unique = {}

    for paper in papers:

        key = None


        # Primeiro tenta DOI
        if paper.doi:
            key = paper.doi.lower()


        # Se não tiver DOI usa título
        else:
            key = normalize_title(
                paper.title
            )


        if key not in unique:

            unique[key] = paper


        else:

            existing = unique[key]

            # guardar fontes
            for source in paper.sources:

                if source not in existing.sources:
                    existing.sources.append(source)


    return list(unique.values())