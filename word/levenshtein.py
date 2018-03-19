# Calculates the levenshtein distance and the edits between two strings
def levenshtein(s1, s2, key=hash):
    rows = costmatrix(s1, s2, key)
    edits = backtrace(s1, s2, rows, key)

    return rows[-1][-1], edits


# Generate the cost matrix for the two strings
# Based on http://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
def costmatrix(s1, s2, key=hash):
    rows = []

    previous_row = xrange(len(s2) + 1)
    rows.append(list(previous_row))

    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (key(c1) != key(c2))
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

        rows.append(previous_row)

    return rows


# Trace back through the cost matrix to generate the list of edits
def backtrace(s1, s2, rows, key=hash):
    i, j = len(s1), len(s2)

    edits = []

    while (not (i == 0 and j == 0)):
        prev_cost = rows[i][j]

        neighbors = []

        if (i != 0 and j != 0):
            neighbors.append(rows[i - 1][j - 1])
        if (i != 0):
            neighbors.append(rows[i - 1][j])
        if (j != 0):
            neighbors.append(rows[i][j - 1])

        min_cost = min(neighbors)

        if (min_cost == prev_cost):
            i, j = i - 1, j - 1
            edits.append({'type': 'match', 'i': i, 'j': j})
        elif (i != 0 and j != 0 and min_cost == rows[i - 1][j - 1]):
            i, j = i - 1, j - 1
            edits.append({'type': 'substitution', 'i': i, 'j': j})
        elif (i != 0 and min_cost == rows[i - 1][j]):
            i, j = i - 1, j
            edits.append({'type': 'deletion', 'i': i, 'j': j})
        elif (j != 0 and min_cost == rows[i][j - 1]):
            i, j = i, j - 1
            edits.append({'type': 'insertion', 'i': i, 'j': j})

    edits.reverse()

    return edits