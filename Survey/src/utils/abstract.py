def reconstruct_abstract(inverted_index):

    if not inverted_index:
        return None

    words = []

    for word, positions in inverted_index.items():

        for position in positions:
            words.append((position, word))

    words.sort()

    abstract = " ".join(
        word
        for _, word in words
    )

    return abstract