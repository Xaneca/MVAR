import re
from html import unescape

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

def clean_abstract(abstract):

    if not abstract:
        return None

    # Remove XML/HTML tags
    abstract = re.sub(
        "<[^>]+>",
        "",
        abstract
    )

    # convert HTML entities
    abstract = unescape(abstract)

    # Clean spaces
    abstract = " ".join(
        abstract.split()
    )

    return abstract