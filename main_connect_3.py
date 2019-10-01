import numpy as np
import random
import connect
import math
import matplotlib.pyplot as plt


env = connect.Connect(verbose=False)
Q = {}
epsilon = 0.2
alpha = 0.5
games_won = []
random_games_won = []
k_played = []


# Sets up the game setting the first player to 'o' and playing in the middle column. 
# State-action pairs are added to the Q table.
def setup_game():
    global k_played
    global games_won
    global random_games_won
    global Q
    Q = {}
    k_played = []
    games_won = []
    random_games_won = []
    env.reset(first_player='o')
    env.act(action = 2)
    start_grid = np.array_str(env.grid)
    for i in range(0, 5):
        Q[(start_grid, i)] = 0
    
    
# Returns a random move from the actions available at that state
def make_random_move(state):
    possible_moves = env.available_actions
    return random.choice(possible_moves)


# Returns the best action according to the Q table. Sometimes returns a random choice
# according to the value of epsilon so as to explore the game. 
def get_best_action(state, possible_moves):
    best = -math.inf
    action = -1
    l = len(possible_moves)
    if(random.random() < (epsilon * (1/len(Q)))):
        return random.choice(possible_moves)
    choices = []
    for i in range(0, l):
        move = possible_moves[i]
        qval = Q[(state, move)]
        if(qval > best):
            choices = []
            choices.append(move)
            best = qval
        elif(qval == best):
            choices.append(move)
    return random.choice(choices)


# Adds new state-action pairs to the Q table
def add_states_to_q():
    s = np.array_str(env.grid)
    poss_moves = env.available_actions
    l = len(poss_moves)
    for i in range(0, l):
        if(not ((s, poss_moves[i]) in Q)):
            Q[(s, poss_moves[i])] = 0

            
# Updates Q values according to formula after action has been taken
def update_q_table(s, a):
    Q[(s,a)] = Q[(s,a)] + alpha * (get_max_reward() - Q[(s,a)])
    

# Returns the best reward expected from the current game state.
def get_max_reward():
    s = np.array_str(env.grid)
    poss_moves = env.available_actions
    l = len(poss_moves)
    best = -math.inf
    for i in range(0,l):
        if(Q[(s, poss_moves[i])] > best):
            best = Q[(s, poss_moves[i])]
    return best

    
# Completes 'n' interactions with the game, then plays 'm' games with 'a' agents and repeats 'k' times
def play_game(n, m, k, a):
    amount = 0
    while(amount < k):
        count = 0
        while(count < n):
            play_move()
            count+=1
            
        agents = 0
        graph_array = np.zeros(a)
        random_graph_array = np.zeros(a)
        while(agents < a):
            num = 0
            total = 0
            random_total = 0
            while(num < m):
                total += play_full_game()
                random_total += play_random_game()
                num+=1
            graph_array[agents] = total
            random_graph_array[agents] = random_total
            agents+=1
        games_won.append(np.average(graph_array))
        random_games_won.append(np.average(random_graph_array))
        k_played.append((amount+1)*n)
        amount += 1
        

# Plays a game where both agents choose actions randomly. Stops when win, draw or loss occurs.
def play_random_game():
    env.reset(first_player='o')
    env.act(action = 2)
    while(True):
        env.change_turn()
        env.act(action = make_random_move(env.grid))
        if(env.was_winning_move()):
            env.reset(first_player='o')
            env.act(action = 2)
            return 1
        env.change_turn()
        env.act(action = make_random_move(env.grid))
        if(env.was_winning_move()):
            env.reset(first_player='o')
            env.act(action = 2)
            return -1
        elif(len(env.available_actions) == 0):
            env.reset(first_player='o')
            env.act(action = 2)
            return 0
    

# Plays a game where one agent chooses actions according to the Q table, the other chooses
# actions randomly. Stops when win, draw or loss occurs.
def play_full_game():
    env.reset(first_player='o')
    env.act(action = 2)
    while(True):
        env.change_turn()
        s = np.array_str(env.grid)
        a = env.available_actions
        if((s,a[0]) in Q):
            env.act(action = get_best_action(s, a))
        else:
            env.act(action = make_random_move(env.grid))
        if(env.was_winning_move()):
            env.reset(first_player='o')
            env.act(action = 2)
            return 1
        env.change_turn()
        env.act(action = make_random_move(env.grid))
        if(env.was_winning_move()):
            env.reset(first_player='o')
            env.act(action = 2)
            return -1
        elif(len(env.available_actions) == 0):
            env.reset(first_player='o')
            env.act(action = 2)
            return 0
    

# Performs one turn within a game where one player chooses according to the Q table
# and the other chooses randomly.
def play_move():
    env.change_turn()
    s = np.array_str(env.grid)
    poss_moves = env.available_actions
    a = get_best_action(s, poss_moves)
    env.act(action = a)
    if(env.was_winning_move()):
        Q[(s,a)] = 1
        env.reset(first_player='o')
        env.act(action=2)
    else:
        env.change_turn()
        aprime = make_random_move(env.grid)
        env.act(action = aprime)
        if(env.was_winning_move()):
            Q[(s,a)] = -1
            env.reset(first_player='o')
            env.act(action = 2)
        elif(len(env.available_actions) == 0):
            Q[(s,a)] = 0
            env.reset(first_player='o')
            env.act(action = 2)
        else:
            add_states_to_q()
            update_q_table(s,a)

setup_game()
play_game(500, 10, 200, 50)
plt.plot(k_played, games_won)
plt.plot(k_played, random_games_won)
plt.show()