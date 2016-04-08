#!/usr/bin/env python
import argparse

from tic.game import Game
from tic.exceptions import IllegalMoveError


def print_state(state):
    for row in state:
        print(row)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
CLI of the tic-tac-toe game.
Displays current position of the board after each move. To make a move, you
should type a pair of numbers, which will represent a line and a column, where
you want to place your piece, counting from 1."""
    )
    parser.parse_args()

    game = Game(3, 3)
    while True:
        choice = input("Would you like to make first move? (Y/n)")
        choice = choice.lower()
        if choice in ['', 'y', 'n']:
            break
    player_first = choice != 'n'
    print("You're playing with {player_pieces} pieces, and your opponent - "
          "{ai_pieces}".format(player_pieces=game.player_piece,
                               ai_pieces=game.ai_piece)
          )
    game.start(player_first=player_first)
    while True:
        winner = game.get_winner()
        if winner:
            break
        print_state(game.state)
        print("It's your move now. Enter line and column where you'd like"
              "to put your piece, counting from 1.")
        while True:
            try:
                line, column = map(int, input().split(' '))
            except ValueError as e:
                print("Couldn't parse your input :(")
                print(e)
                continue
            try:
                game.make_move(line, column)
            except IllegalMoveError as e:
                print("You've tried to make an illegal move.")
                print(e)
                continue
            break
    print_state(game.state)
    print("And we have a winner")
    print(winner, "won!")
