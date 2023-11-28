from random import random

from helpers import opposite_symbol
from tic_tac_toe import Board

class Player:
  def __init__(self, weights):
    self.weights = weights

  def play(self, board, symbol) -> Board:
    possible_boards = []
    for move in board.available_moves():
      possible_boards.append(board.play(symbol, move))
    return None if len(possible_boards) == 0 else sorted(possible_boards, key=lambda g: self._value(g, symbol))[-1]

  def update_weights(self, n, board, symbol, vtrain, training_weights):
    new_weights = self.weights.copy()
    for i in range(len(new_weights)):
      new_weights[i] = new_weights[i] + n * (vtrain  - self._value(board, symbol)) * training_weights[i]
    self.weights = new_weights

  def _value(self, board, symbol):
    if board.winner() == symbol:
      return 100
    elif board.winner() is not None:
      return -100

    return sum([
      self.weights[0],
      self.weights[1] * self.__center(board, symbol),
      self.weights[2] * self.__corners(board, symbol),
      self.weights[3] * self.__middles(board, symbol),
    ])

  def __center(self, board, symbol):
    return 1 if board.squares[1][1] == symbol else 0

  def __corners(self, board, symbol):
    return sum(
      map(
        lambda s: 1 if symbol == s else 0,
        [board.squares[0][0], board.squares[0][2], board.squares[2][0], board.squares[2][2]]
      )
    )

  def __middles(self, board, symbol):
    return sum(
      map(
        lambda s: 1 if symbol == s else 0,
        [board.squares[0][1], board.squares[1][0], board.squares[1][2], board.squares[2][1]]
      )
    )


class RandomPlayer(Player):
  def _value(self, board, symbol):
    return random() * 100
