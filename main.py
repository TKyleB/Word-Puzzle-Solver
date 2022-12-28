from pathlib import Path
import re
import csv
FILE_PATH = Path(__file__).with_name("word_list.csv")

def get_puzzle_input():
    print("Please type the puzzle input. Use '.' for unknown characters. Seperate words with a space. Non-case Sensitive.")
    user_input = input()
    if all(c.isalpha() or c.isspace() or c == "." for c in user_input):
        return user_input.lower().split(" ")
    else:
        print("Invalid Input.")
        get_puzzle_input()
    

PUZZLE_INPUT = get_puzzle_input()
POTENTIAL_SOLUTIONS = []

def load_word_list():
    word_list = {}
    with open(FILE_PATH) as file:
        reader = csv.DictReader(file)
        for row in reader:
            word_list[row["LEMMA"]] = row["FREQUENCY"] # LEMMA header contains the root word FREQUENCY is a usage rating
            if row["INFLECTIONS"]:
                for word in row["INFLECTIONS"].replace(",", "").split(" "): # INFLECTIONS are plurals of the root words
                    word_list[word] = row["FREQUENCY"]
    return word_list

WORD_LIST = load_word_list()
    
for section in PUZZLE_INPUT:
    # Using "." for unknown characters is important for the regex comparision
    pattern = re.compile(section)
    # Checks the input against the word list checking for length and matching characters
    matches = {word:ranking for word, ranking in WORD_LIST.items() if len(word) == len(section) and re.match(pattern, word)}
    # Sorts results by their usage rating
    ranked_matches = dict(sorted(matches.items(), key=lambda item: int(item[1]), reverse=True))
    POTENTIAL_SOLUTIONS.append(ranked_matches)


with open("solution.csv", mode="w") as result_file:
    writer = csv.writer(result_file)
    writer.writerow(["Word #", "Word Result", "Score"])
    for count, solution in enumerate(POTENTIAL_SOLUTIONS):
        for key, value in solution.items():
            writer.writerow([f"Word {count + 1}", key, value])
        writer.writerow("")
    print("Solution Generated in solution.csv")
        
