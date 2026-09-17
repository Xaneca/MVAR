def filter_metadata(papers, config):

    filtered = []

    for paper in papers:

        if paper.year < config["min_year"]:
            continue

        if config["require_abstract"]:
            if not paper.abstract:
                continue

        filtered.append(paper)

    return filtered




def filter_papers(papers, config):

    

    return papers