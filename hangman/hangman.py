import dataclasses
from typing import List, Tuple
from copy import deepcopy
import string

@dataclasses.dataclass
class GameState:
    word: str
    char_guessed: List[str]
    char_allowed: List[str]=dataclasses.field(default_factory=lambda: list(string.ascii_lowercase))
    char_free: List[str]=dataclasses.field(default_factory=lambda: list(string.punctuation + string.whitespace))


def make_state(word: str) -> GameState:
    return GameState(word=word, char_guessed=[])


def guess(state: GameState, guess: str) -> Tuple[GameState, int]:
    assert len(guess) == 1, 'Must guess a single character'
    guess = guess.lower()
    if guess not in state.char_allowed:
        raise ValueError(f'You guessed {guess}. Allowed values are {state.char_allowed}')
    if guess in state.char_guessed:
        return state, 0
    if guess in state.char_free:
        return state, 0
    number_occurances = len([c for c in state.word.lower() if c==guess])
    state = deepcopy(state)
    state.char_guessed.append(guess)
    return state, number_occurances


def display_word(state: GameState) -> str:
    def display_char(c):
        if c in state.char_free:
            return c
        if c.lower() in state.char_guessed:
            return c
        return '_'
    return ''.join([display_char(c) for c in state.word])
    

def display_board(state: GameState) -> str:
    word = display_word(state)
    wrong_guesses = [c for c in state.char_guessed if c.lower() not in state.word.lower()]
    used = " ".join(wrong_guesses)
    board = (f"{word}\n\nWrong guesses: {len(wrong_guesses)}\n\t{used}\n")
    return board


def is_game_over(state) -> bool:
    covered = set(state.char_guessed + state.char_free)
    return len(set(state.word.lower()) - covered) == 0


def game():
    state = make_state("Hello world!")
    while (is_game_over(state)==False):
        print(display_board(state))
        curr_guess = input("Please give a character to guess: ")
        state, num = guess(state, curr_guess)
        print(f"\n\nYour guess has uncovered {num} letters\n")
    
    print(display_board(state))
    print("Congratulations!!")


if __name__=='__main__':
    game()