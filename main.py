import os

from matplotlib import pyplot as plt
from game import *


def train_min_test_min(epochs = 5000, debug_value = 100, n_tests = 20):

    game = Game()

    q_id = 1
    opp_id = 2

    q_wins = 0
    opp_wins = 0

    for epoch in range(epochs):
        winner_id = game.run_q_vs_minmax(False)

        if winner_id == q_id:
            q_wins += 1
        elif winner_id == opp_id:
            opp_wins += 1

        if (epoch+1) % debug_value == 0:
            print(f"\nEpoch {epoch+1} of {epochs} epochs")
            print(f"Q_Learn_Agent wins: {q_wins} |||| Min-Max wins: {opp_wins}")


    results = []
    for test in range(n_tests):
        print(f"\nTest number {test+1}")
        results.append(game.run_q_vs_minmax(True))

    print(f"\nTest results: {results}")

def train_min_test_rand(epochs = 5000, debug_value = 100, n_tests = 20):

    game = Game()

    q_id = 1
    opp_id = 2

    q_wins = 0
    opp_wins = 0

    for epoch in range(epochs):
        winner_id = game.run_q_vs_minmax(False)

        if winner_id == q_id:
            q_wins += 1
        elif winner_id == opp_id:
            opp_wins += 1

        if (epoch+1) % debug_value == 0:
            print(f"\nEpoch {epoch+1} of {epochs} epochs")
            print(f"Q_Learn_Agent wins: {q_wins} |||| Min-Max wins: {opp_wins}")


    results = []
    for test in range(n_tests):
        print(f"\nTest number {test+1}")
        results.append(game.run_q_vs_random(True))

    print(f"\nTest results: {results}")

def train_rand_test_rand(epochs = 5000, debug_value = 100, n_tests = 20):

    game = Game()

    q_id = 1
    opp_id = 2

    q_wins = 0
    opp_wins = 0

    for epoch in range(epochs):
        winner_id = game.run_q_vs_random(False)

        if winner_id == q_id:
            q_wins += 1
        elif winner_id == opp_id:
            opp_wins += 1

        if (epoch+1) % debug_value == 0:
            print(f"\nEpoch {epoch+1} of {epochs} epochs")
            print(f"Q_Learn_Agent wins: {q_wins} |||| Min-Max wins: {opp_wins}")


    results = []
    for test in range(n_tests):
        print(f"\nTest number {test+1}")
        results.append(game.run_q_vs_random(True))

    print(f"\nTest results: {results}")

def train_rand_test_min(epochs = 5000, debug_value = 100, n_tests = 20):

    game = Game()

    q_id = 1
    opp_id = 2

    q_wins = 0
    opp_wins = 0

    for epoch in range(epochs):
        winner_id = game.run_q_vs_random(False)

        if winner_id == q_id:
            q_wins += 1
        elif winner_id == opp_id:
            opp_wins += 1

        if (epoch+1) % debug_value == 0:
            print(f"\nEpoch {epoch+1} of {epochs} epochs")
            print(f"Q_Learn_Agent wins: {q_wins} |||| Min-Max wins: {opp_wins}")


    results = []
    for test in range(n_tests):
        print(f"\nTest number {test+1}")
        results.append(game.run_q_vs_random(True))

    print(f"\nTest results: {results}")


def train_min_test_all(epochs = 5000, debug_value = 100, n_tests = 20):

    directory = "resultados/trainM"
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    game = Game()

    q_id = 1
    opp_id = 2

    q_wins = 0
    opp_wins = 0

    cumulative_reward = []
    total_reward = 0

    for epoch in range(epochs):
        winner_id, ep_reward = game.run_q_vs_minmax(False)

        if winner_id == q_id:
            q_wins += 1
        elif winner_id == opp_id:
            opp_wins += 1



        total_reward += ep_reward
        cumulative_reward.append(total_reward)



        if (epoch+1) % debug_value == 0:
            print(f"\nEpoch {epoch+1} of {epochs} epochs")
            print(f"Q_Learn_Agent wins: {q_wins} ||| Total reward: {total_reward} |||| Min-Max wins: {opp_wins}")


    results_min_max = []
    for test in range(n_tests):
        print(f"\nTest number {test+1}")

        file_name = f"{directory}/tM{test}"

        results_min_max.append(game.run_q_vs_minmax(True, file_name)[0])

    results_random = []
    for test in range(n_tests):
        print(f"\nTest number {test+1}")

        file_name = f"{directory}/tR{test}"

        results_random.append(game.run_q_vs_random(True, file_name)[0])

    print(f"\nTest MinMax results: {results_min_max}")
    print(f"\nTest Random results: {results_random}")

    return cumulative_reward

def train_rand_test_all(epochs = 5000, debug_value = 100, n_tests = 20):

    directory = "resultados/trainR"
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    game = Game()

    q_id = 1
    opp_id = 2

    q_wins = 0
    opp_wins = 0

    cumulative_reward = []
    total_reward = 0

    for epoch in range(epochs):
        winner_id, ep_reward = game.run_q_vs_random(False)

        if winner_id == q_id:
            q_wins += 1
        elif winner_id == opp_id:
            opp_wins += 1


        total_reward += ep_reward
        cumulative_reward.append(total_reward)
        

        if (epoch+1) % debug_value == 0:
            print(f"\nEpoch {epoch+1} of {epochs} epochs")
            print(f"Q_Learn_Agent wins: {q_wins} ||| Total reward: {total_reward} |||| Random wins: {opp_wins}")


    results_min_max = []
    for test in range(n_tests):
        print(f"\nTest number {test+1}")

        file_name = f"{directory}/tM{test}"

        results_min_max.append(game.run_q_vs_minmax(True, file_name)[0])

    results_random = []
    for test in range(n_tests):
        print(f"\nTest number {test+1}")

        file_name = f"{directory}/tR{test}"

        results_random.append(game.run_q_vs_random(True, file_name)[0])

    print(f"\nTest MinMax results: {results_min_max}")
    print(f"\nTest Random results: {results_random}")

    return cumulative_reward


# TESTES

# print("\nTreino do Q com MinMax e teste com MinMax")
# train_min_test_min(epochs=10000, debug_value=50)

# print("\nTreino do Q com MinMax e teste com Random")
# train_min_test_rand(epochs=10000, debug_value=50)

# print("\nTreino do Q com Random e teste com Random")
# train_rand_test_rand()

# print("\nTreino do Q com Random e teste com MinMax")
# train_rand_test_min()

print("\nTreino do Q com MinMax e testes")
cumulative_reward = train_min_test_all(epochs=30000, debug_value=50, n_tests=20)

# print("\nTreino do Q com Random e testes")
# cumulative_reward = train_rand_test_all(epochs=10000, debug_value=50, n_tests=20)

plt.plot(cumulative_reward)
plt.xlabel('Épocas')
plt.ylabel('Recompensa Cumulativa')
plt.title('Recompensa Total ao longo das Épocas')
plt.show()