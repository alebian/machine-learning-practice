import copy

from helpers import opposite_symbol

class Board:
  def __init__(self, squares=None):
    if squares is None:
      self.squares = [
        [None, None, None],
        [None, None, None],
        [None, None, None]
      ]
    else:
      self.squares = squares
    self.available_moves_list = None

  def __str__(self):
    return "{}\n{}\n{}\n".format(self.squares[0], self.squares[1], self.squares[2])

  def available_moves(self):
    if self.available_moves_list is not None:
      return self.available_moves_list

    moves = []
    for i in range(3):
      for j in range(3):
        if self.squares[i][j] is None:
          moves.append((i, j))

    self.available_moves_list = moves
    return moves

  def successor_moves(self, symbol):
    moves = []
    for first_move in self.available_moves():
      first_board = self.play(symbol, first_move)
      for second_move in first_board.available_moves():
        moves.append(first_board.play(opposite_symbol(symbol), second_move))
    return moves

  def is_end(self):
    return len(self.available_moves()) == 0 or self.winner() is not None

  def play(self, symbol, move):
    squares = copy.deepcopy(self.squares)
    squares[move[0]][move[1]] = symbol
    return Board(squares=squares)

  def winner(self):
    for row in range(3):
      if self.squares[row][0] is not None and self.squares[row][0] == self.squares[row][1] == self.squares[row][2]:
        return self.squares[row][0]

    for column in range(3):
      if self.squares[0][column] is not None and self.squares[0][column] == self.squares[1][column] == self.squares[2][column]:
        return self.squares[0][column]

    if self.squares[0][0] is not None and self.squares[0][0] == self.squares[1][1] == self.squares[2][2]:
      return self.squares[0][0]

    if self.squares[0][2] is not None and self.squares[0][2] == self.squares[1][1] == self.squares[2][0]:
      return self.squares[0][2]
