#!/usr/bin/env python
import time
import argparse

from tic.game import Game
from tic.ai import MinimaxAI, get_heuristic_ai_class
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
    parser.add_argument('--lines', '-l', dest='lines', type=int,
                        default=3, help="number of lines (default 3)")
    parser.add_argument('--columns', '-c', dest='columns', type=int,
                        default=3, help="number of columns (default 3)")
    parser.add_argument('--win', '-w', dest='win_count', type=int,
                        default=3, help="number of pieces on a straight line "
                                        "required to win (default 3)")
    args = parser.parse_args()

    if not (args.lines > 0 and args.columns > 0 and args.win_count > 0):
        print("Neither one of the parameters can be <= 0.")
        exit(1)

    game = Game(args.lines, args.columns, args.win_count)

    if args.lines*args.columns <= 12:
        ai_class = MinimaxAI
    else:
        ai_class = get_heuristic_ai_class(3)

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
    start_time = time.time()
    game.start(ai_class=ai_class, player_first=player_first)
    end_time = time.time()
    if not player_first:
        print("AI thought for {} seconds.".format(end_time - start_time))
    while not game.is_game_over():
        print_state(game.state)
        print("It's your move now. Enter line and column where you'd like "
              "to put your piece, counting from 1.")
        while True:
            try:
                line, column = map(int, input().split(' '))
            except ValueError as e:
                print("Couldn't parse your input :(")
                print(e)
                continue
            start_time = time.time()
            try:
                game.make_move(line, column)
            except IllegalMoveError as e:
                print("You've tried to make an illegal move.")
                print(e)
                continue
            end_time = time.time()
            print("AI thought for {} seconds.".format(end_time - start_time))
            break
    winner = game.get_winner()
    print_state(game.state)
    if winner is not None:
        print("And we have a winner")
        print(winner.upper(), "won!")
    else:
        print("It's a draw!")
