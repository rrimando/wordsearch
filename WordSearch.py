#!/usr/bin/python
""" 
    Word Search
"""
import os, argparse

results = []

def find_word (wordsearch, word):
    """Trys to find word in wordsearch and prints result"""
    # Store first character positions in array
    start_pos = []
    first_char = word[0]
    for i in range(0, len(wordsearch)):
        for j in range(0, len(wordsearch[i])):
            if (wordsearch[i][j] == first_char):
                start_pos.append([i,j])
    # Check all starting positions for word
    for p in start_pos:
        if check_start(wordsearch, word, p):
            # Word found
            return
    # Word not found

def check_start (wordsearch, word, start_pos):
    """Checks if the word starts at the startPos. Returns True if word found"""
    directions = [[-1,1], [0,1], [1,1], [-1,0], [1,0], [-1,-1], [0,-1], [1,-1]]
    # Iterate through all directions and check each for the word
    for d in directions:
        if (check_dir(wordsearch, word, start_pos, d)):
            return True

def check_dir (wordsearch, word, start_pos, dir):
    """Checks if the word is in a direction dir from the start_pos position in the wordsearch. Returns True and prints result if word found"""
    found_chars = [word[0]] # Characters found in direction. Already found the first character
    current_pos = start_pos # Position we are looking at
    pos = [start_pos] # Positions we have looked at
    while (chars_match(found_chars, word)):
        coordinates = []
        if (len(found_chars) == len(word)):
            # Store Coordinates
            for x in range(0, len(wordsearch)):
                line = "";
                for y in range(0, len(wordsearch[x])):
                    is_pos = False
                    for z in pos:
                        if (z[0] == x) and (z[1] == y):
                            is_pos = True
                    if (is_pos):
                        coordinates.append(('{},{}').format(x, y))

            results.append(coordinates)
            return True;

        # Have not found enough letters so look at the next one
        current_pos = [current_pos[0] + dir[0], current_pos[1] + dir[1]]
        pos.append(current_pos)
        if (is_valid_index(wordsearch, current_pos[0], current_pos[1])):
            found_chars.append(wordsearch[current_pos[0]][current_pos[1]])
        else:
            # Reached edge of wordsearch and not found word
            return

def chars_match (found, word):
    """Checks if the leters found are the start of the word we are looking for"""
    index = 0
    for i in found:
        if (i != word[index]):
            return False
        index += 1
    return True

def is_valid_index (wordsearch, line_num, col_num):
    """Checks if the provided line number and column number are valid"""
    if ((line_num >= 0) and (line_num < len(wordsearch))):
        if ((col_num >= 0) and (col_num < len(wordsearch[line_num]))):
            return True
    return False

"""
    SCRIPT
"""

parser = argparse.ArgumentParser(description='A simple word search utility')
   
parser.add_argument('--puzzle', required=True)
parser.add_argument('--output', required=False)

args = parser.parse_args()

puzzle_content = open(args.puzzle).read()
puzzle = puzzle_content.split("\n\n")

word_search = puzzle[0].splitlines()
search_words = puzzle[1].splitlines()

file_output = args.output if args.output else args.puzzle.split('.')[0] + '.out'
try:
    os.remove(file_output)
except FileNotFoundError:
    pass
file_handler = open(file_output, "a") 

"""
    Empty File 
"""

for word in search_words:
    results = []
    word = word.strip()

    if (word == 'q'):
        break;
    else:
        find_word(word_search, word)

    if(results):
        line = "{}({})({})\n".format(word, results[0][0], results[0][-1])
    else:
        line = "{} not found:\n".format(word)

    print(line)
    file_handler.write(line)

file_handler.close()


# EOF