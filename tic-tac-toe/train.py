from random import random
import matplotlib.pyplot as plt
import numpy as np

from helpers import opposite_symbol, CIRCLE, CROSS
from tic_tac_toe import Board
from player import Player, RandomPlayer


def play_game(player1, player2):
  game = Board()
  current_player = player1
  current_symbol = CROSS

  while not game.is_end():
    game = current_player.play(game, current_symbol)
    current_player = player2 if current_player == player1 else player1
    current_symbol = opposite_symbol(current_symbol)

  return game

def play_some_games(games, player1, player2):
  p1_wins = 0
  p2_wins = 0
  draws = 0

  for _ in range(games):
    game = play_game(player1, player2)
    if game.winner() == CROSS:
      p1_wins += 1
    elif game.winner() == CIRCLE:
      p2_wins += 1
    else:
      draws += 1

  return (p1_wins, p2_wins, draws)

WEIGHTS = [0.0, 10.0, 5.0, 1.0]
ETA = 0.01
TRAINING_AMOUNT = 100

MACHINE_WEIGHTS = [random(), random(), random(), random()]

def train(game, symbol, machine, other_player):
  if game.is_end():
    return

  successor_moves = game.successor_moves(symbol)
  if len(successor_moves) == 0:
    return

  vtrain = machine._value(
    sorted(successor_moves, key=lambda m: machine._value(m, opposite_symbol(symbol)))[-1], opposite_symbol(symbol)
  )
  machine.update_weights(ETA, game, symbol, vtrain, WEIGHTS)

  next_move = sorted(list(map(
    lambda move: game.play(symbol, move),
    game.available_moves()
  )), key=lambda g: other_player._value(g, symbol))[-1]

  train(next_move, opposite_symbol(symbol), machine, other_player)


fixed_player = Player(WEIGHTS)
machine = Player(MACHINE_WEIGHTS)
random_player = RandomPlayer(WEIGHTS)

test_player_wins = []
machine_wins = []
draws = []

player_to_learn = fixed_player
player_to_test = random_player

for i in range(TRAINING_AMOUNT):
  print("Run {} of {}".format(i + 1, TRAINING_AMOUNT))
  train(Board(), CROSS, machine, player_to_learn)

  test_player_wins_this_run = 0
  machine_wins_this_run = 0
  draws_this_run = 0
  games = 50

  p1, p2, d = play_some_games(games, player_to_test, machine)
  test_player_wins_this_run += p1
  machine_wins_this_run += p2
  draws_this_run += d

  p1, p2, d = play_some_games(games, machine, player_to_test)
  test_player_wins_this_run += p2
  machine_wins_this_run += p1
  draws_this_run += d

  test_player_wins.append((i, test_player_wins_this_run))
  machine_wins.append((i, machine_wins_this_run))
  draws.append((i, draws_this_run))

print(machine.weights)

x1, y1 = np.array(test_player_wins).T
x2, y2 = np.array(machine_wins).T
x3, y3 = np.array(draws).T

plt.plot(x1, y1, label='Other player wins')
plt.plot(x2, y2, label='Machine wins')
plt.plot(x3, y3, label='Draws')

plt.xlabel('Runs')
plt.title('Learning Tic-Tac-Toe')
plt.legend()
plt.show()
