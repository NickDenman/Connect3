import numpy as np
import random
import connect
import math

env = connect.Connect(verbose=False)
Q = {}
setup_game()
print(Q)
Epsilon = 0.5
Alpha = 0.5


def setup_game():
    env.reset(first_player='o')
    env.act(action=2)
    start_grid = np.array_str(env.grid)
    for i in range(0, 5):
        Q[(start_grid, i)] = 0


def make_random_move(state):
    possible_moves = env.available_actions
    return random.choice(possible_moves)


def make_q_move(state):
    possible_moves = env.available_actions
    act = get_best_action(state, possible_moves)
    env.act(action=act)
    if (not check_win(state)):
        possible_moves_oponent = env.available_actions
        current_grid = env.grid
        add_poss_states_to_q(current_grid, possible_moves_oponent)
        update_q_table(state, act, current_grid, possible_moves_oponent)


def check_win(state, action):
    if (env.was_winning_move()):
        Q[(state, action)] = 1
        return True
    return False


def get_best_action(state, possible_moves):
    best = -math.inf
    action = -1
    l = len(possible_moves)
    for i in range(0, l):
        if (Q[(state, possible_moves(i))] >= best):
            best = Q[(state, possible_moves(i))]
            action = possible_moves(i)

    return action

# def add_poss_states_to_q(state):


# def update_q_table(state, action, reward):


# def play_game():


# while()