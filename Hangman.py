# import time to auto exit/close the program at the end of a game
import time
# English alphabet for game (used global)
abc = "abcdefghijklmnopqrstuvwxyz"
# after 6 wrong tries the game is over
MAX_TRIES = 6

def hangman_game_start_logo():
    """
        :return: The opening screen of game
        """
    HANGMAN_ASCII_ART = (""" _    _                                         
| |  | |                                        
| |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
|  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
| |  | | (_| | | | | (_| | | | | | | (_| | | | |
|_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                     __/ |
                    |___/\n""")
    # input("Welcome! press 'Enter' to start the game!")

    print(HANGMAN_ASCII_ART, MAX_TRIES)

def choose_word(file_path, index):
    """
    :param file_path: path to the file  with words
    :param index: index of word in the file
    :return: tuple of two options:
    1. number of words in file, without duplicated words
    2. word in the index that we choice
    * chose from index 1 and not 0
    * if index bigger then words in text, start count over
    """
    word_file = open(file_path, "r")
    words = word_file.read()
    # list of words
    words = words.split(' ')
    # check no duplicated words in file
    no_dup_words = []
    for x in words:
        if x not in no_dup_words:
            no_dup_words.append(x)

    word_count = (len(words))
    while index == 0:
        index = int(input("Enter index again, starts from 1 :"))
    while index > word_count:
        index = index - word_count
    word_file.close()
    # return how much not duplicated words in file and the word we chose (not for game)
    result_tuple_no_duplicated_words = (len(no_dup_words), str(words[index-1]))
    # return the choisen word
    result_tuple = (str(words[index - 1]))
    return result_tuple

def print_hangman(num_of_tries):
    """
    :param num_of_tries: number of failed attempts
    :return: one of 7 pictures
    """

    try_zero = ("x-------x\n")
    try_one = ("""x-------x
|
|
|
|
|\n""")
    try_two = ("""x-------x
|       |
|       0
|
|
|\n""")
    try_three = ("""x-------x
|       |
|       0
|       |
|
|\n""")
    try_four = ("""x-------x
|       |
|       0
|      /|\\
|
|\n""")
    try_five = ("""x-------x
|       |
|       0
|      /|\\
|      /
|\n""")
    try_six = ("""x-------x
|       |
|       0
|      /|\\
|      / \\
|\n""")

    HANGMAN_PHOTOS = {0: try_zero, 1: try_one, 2: try_two, 3: try_three, 4: try_four, 5: try_five, 6: try_six}
    print(HANGMAN_PHOTOS[num_of_tries])

def check_valid_input(letter_quessed, old_letters_guessed):
    """
    :param letter_quessed: input letter from user
    :param old_letters_guessed: all letter that user guessed in past
    :return: True if it's new, only one english letter,
             False if it's more than one english letter, non english letter or sign
    """
    global abc

    if letter_quessed in old_letters_guessed:
        return False
    elif len(letter_quessed) > 1:
        return False
    elif letter_quessed not in abc:
        return False
    elif letter_quessed in abc and len(letter_quessed) == 1:
        return True
    elif letter_quessed == '':
        return False

def try_update_letter_guessed(letter_quessed, old_letters_guessed):
    """

    :param letter_quessed: input letter from user
    :param old_letters_guessed: all letter that user guessed in past
    :return: True if it's a new, only one english letter, else it's False

    """

    letter_quessed = letter_quessed.lower()
    global abc
    # abc = "abcdefghijklmnopqrstuvwxyz"

    already_guessted = letter_quessed in old_letters_guessed
    no_english_letter = letter_quessed not in abc
    more_than_one_letter = len(letter_quessed) > 1
    blank_letter = letter_quessed == ''

    if already_guessted:
        added_old_letters = (' -> '.join(sorted(old_letters_guessed)))
        print("X")
        print(added_old_letters)
        return False
    elif no_english_letter or more_than_one_letter or blank_letter:
        added_old_letters = (' -> '.join(sorted(old_letters_guessed)))
        print("X")
        print(added_old_letters)
        return False
    elif letter_quessed in abc and len(letter_quessed) == 1:
        old_letters_guessed = old_letters_guessed.append(letter_quessed)
        return True

def show_hidden_word(secret_word, old_letters_guessed):
    """
    :param secret_word: word that we need to gess
    :param old_letters_guessed: all letters that gussed
    :return: word whit under lines and letter if guessed
    """
    result = []
    for x in secret_word:
        if x in old_letters_guessed:
            result.append(x)
        else:
            result.append("_")
    result = " ".join(result)
    return result

def check_win(secret_word, old_letters_guessed):
    """
    :param secret_word: word that we need to gess
    :param old_letters_guessed: all letters that gussed
    :return: word whit under lines and letter if guessed
    """

    result = []
    for x in secret_word:
        if x in old_letters_guessed:
            result.append(x)
        else:
            result.append("_")
    result = " ".join(result)
    return "_" not in result

def new_letter_incorrect(new_letter, secret_word):
    """
    :param new_letter: users letter inputed
    :param secret_word: word that user must to guess
    :return: if wrong letter return sad smile, else "good guess"
    """
    if new_letter not in secret_word:
        print(":(")
        return False
    else:
        return True



def main():
    """
    User must to guess word by guessing letter by letter.
    each wrong guess will print picture of hangman step by step till it's done and game will be over.
    Or user will guess the word and win the game.
    Good luck !
    """

    # variable for pictures of hangman, start from 0 to 6 used in function print_hangman
    num_of_tries = 0
    # all letters that user guesses
    old_letters_guessed = []
    # print welcome screen

    hangman_game_start_logo()

    # ask from user to enter file path with words + index to choose word
    file_path = input("Enter file path:")
    index = int(input("Enter index (only numbers):"))
    # will chose word from file
    secret_word = choose_word(file_path, index)
    len_word = len(secret_word)
    # create secret word of like that: _ _ _ _
    guess = ("_ " * len_word)

    print("\nLet's start!\n")
    print_hangman(num_of_tries)
    print(guess)

    while check_win(secret_word, old_letters_guessed) is False:
        letter_guess = input("\nGuess a letter:")
        letter_guess = letter_guess.lower()

        # check if it's correct input
        if check_valid_input(letter_guess, old_letters_guessed) is False:
            try_update_letter_guessed(letter_guess, old_letters_guessed)

        else:
            if try_update_letter_guessed(letter_guess, old_letters_guessed) is False:
                pass
            else:
                if new_letter_incorrect(letter_guess, secret_word) is False:
                    num_of_tries += 1
                    print_hangman(num_of_tries)
                print(show_hidden_word(secret_word, old_letters_guessed))

        if MAX_TRIES == num_of_tries:
            print("LOSE")
            break

    if check_win(secret_word, old_letters_guessed) is True:
        print("\nWIN!")

    # After the game is finished, ask if user want to play more
    answer = input("\nplay again ? input 'yes' or 'Enter key' to Exit:")
    if answer == "yes" or answer == "y":
        main()
    else:
        print("\n*** GAME OVER *** ")
    time.sleep(3)


if __name__ == '__main__':
    main()
