"""Week 03 lab solutions: Mad Libs and Number Guessing Game.

Implementations of `generate_mad_lib` and `guessing_game` used by the
test suite in `week03/tests/test_lab03.py`.
"""
import random


def generate_mad_lib(adjective, noun, verb):
    """
    Generate a short Mad Libs-style story using three words.

    Parameters
    ----------
    adjective : str
        An adjective to use in the story (e.g., "silly").
    noun : str
        A noun to use in the story (e.g., "cat").
    verb : str
        A past-tense verb to use in the story (e.g., "jumped").

    Returns
    -------
    str
        A formatted story string that incorporates all three input words.

    Notes
    -----
    - Uses f-string formatting
    - Does not use input() so it is testable by pytest
    """
    # Build a creative story that uses all three parameters
    story = (
        f"On a bright morning, the {adjective} {noun} quietly {verb} through "
        "the bustling market, surprising vendors and curious passersby alike."
    )
    return story


def guessing_game():
    """
    Play a number guessing game with the user.

    Behavior
    --------
    - Chooses a secret integer between 1 and 100 (inclusive).
    - Prompts the user repeatedly until the correct number is guessed.
    - Prints feedback: "Too low! Try again.", "Too high! Try again.", and a
      congratulatory message showing the number of attempts when guessed.
    - Uses `input()` to collect guesses and `print()` for feedback, so tests
      can mock those built-ins.
    """
    secret = random.randint(1, 100)
    attempts = 0

    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")

    while True:
        user_input = input("Enter your guess: ")
        attempts += 1

        try:
            guess = int(user_input)
        except ValueError:
            print("Please enter a valid integer.")
            continue

        if guess < secret:
            print("Too low! Try again.")
        elif guess > secret:
            print("Too high! Try again.")
        else:
            print(f"Congratulations! You guessed it in {attempts} attempts!")
            break


if __name__ == '__main__':
    guessing_game()
