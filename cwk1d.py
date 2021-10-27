from bisect import bisect_left


def find_words(board, words, x, y, prefix, path):
    ' Find words that can be generated starting at position x, y '

    # Base case
    # find if current word prefix is in list of words
    found = bisect_left(words, prefix)  # can use binary search since words are sorted
    if found >= len(words):
        return

    if words[found] == prefix:
        yield prefix, path  # Prefix in list of words

    # Give up on path if what we found is not even a prefixx
    # (there is no point in going further)
    if len(words[found]) < len(prefix) or words[found][:len(prefix)] != prefix:
        return

    # Extend path by one letter in boarde
    # Since can only go right and down
    # No need to worry about same cell occurring multiple times in a given path
    for adj_x, adj_y in [(0, 1), (1, 0)]:
        x_new, y_new = x + adj_x, y + adj_y
        if x_new < len(board) and y_new < len(board[0]):
            yield from find_words(board, words, x_new, y_new, \
                                  prefix + board[x_new][y_new], \
                                  path + [(x_new, y_new)])


def check_all_starts(board, words):
    ' find all possilble paths through board for generating words '
    # check each starting point in board
    for x in range(len(board)):
        for y in range(len(board[0])):
            yield from find_words(board, words, x, y, board[x][y], [(x, y)])


def find_non_overlapping(choices, path):
    ' Find set of choices with non-overlapping paths '
    if not choices:
        # Base case
        yield path
    else:
        word, options = choices[0]

        for option in options:
            set_option = set(option)

            if any(set_option.intersection(p) for w, p in path):
                # overlaps with path
                continue
            else:
                yield from find_non_overlapping(choices[1:], path + [(word, option)])


def solve(board, words):
    ' Solve for path through board to create words '
    words.sort()

    # Get choice of paths for each word
    choices = {}
    for word, path in check_all_starts(board, words):
        choices.setdefault(word, []).append(path)

    # Find non-intersecting paths (i.e. no two words should have a x, y in common)
    if len(choices) == len(words):
        return next(find_non_overlapping(list(choices.items()), []), None)
    # Instead of returning None
    # This because your if function has to return something when the conditions are not met.
    # So in this case,when the character is not found, we ask the program to return None
    # Then just after that, we ask the program to return a string instead of 'None'
    # Just like the instruction
    return "Not Found!"


from pprint import pprint as pp

# This line is for you to simply run the text that needs to be found on the table
# words = [ "YEM"]

# This line is for you to simply ask the user for an input text that needs to be found on the table
words = [input("Enter words: ")]
board = [['R', 'U', 'N', 'A', 'R', 'O', 'U', 'N', 'D', 'D', 'L'],
['E', 'D', 'C', 'I', 'T', 'O', 'A', 'H', 'C', 'Y', 'V'],
['Z', 'Y', 'U', 'W', 'S', 'W', 'E', 'D', 'Z', 'Y', 'A'],
['A', 'K', 'O', 'T', 'C', 'O', 'N', 'V', 'O', 'Y', 'V'],
['L', 'S', 'B', 'O', 'S', 'E', 'V', 'R', 'U', 'C', 'I'],
['B', 'O', 'B', 'L', 'L', 'C', 'G', 'L', 'P', 'B', 'D'],
['L', 'K', 'T', 'E', 'E', 'N', 'A', 'G', 'E', 'D', 'L'],
['I', 'S', 'T', 'R', 'E', 'W', 'Z', 'L', 'C', 'G', 'Y'],
['A', 'U', 'R', 'A', 'P', 'L', 'E', 'B', 'A', 'Y', 'G'],
['R', 'D', 'A', 'T', 'Y', 'T', 'B', 'I', 'W', 'R', 'A'],
['T', 'E', 'Y', 'E', 'M', 'R', 'O', 'F', 'I', 'N', 'U']]

pp(solve(board, words))