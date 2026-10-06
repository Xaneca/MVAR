from itertools import product


def build_queries(groups, templates):

    queries = []

    for template in templates:

        variables = [
            part.strip("{}")
            for part in template.split()
            if part.startswith("{")
        ]

        values = [
            groups[var]
            for var in variables
        ]

        for combination in product(*values):

            query = template

            for key, value in zip(variables, combination):
                query = query.replace(
                    f"{{{key}}}",
                    value
                )

            queries.append(query)

    # queries = queries[:2]

    return queries