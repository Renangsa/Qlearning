#Aqui vocês irão colocar seu algoritmo de aprendizado
import connection as cn
import random
 
alpha = 0.1
gamma = 0.4
 
Qtable = []
 
def init():
    with open("resultado.txt", "r") as f:
        lines = f.readlines()
 
    for line in lines:
        values = [float(value) for value in line.split()]
        Qtable.append(values)
 
def save_table():
    with open("resultado.txt", "w") as f:
        for row in Qtable:
            f.write(" ".join(map(str, row)) + "\n")
 
def get_max_action(state):
    print(max(range(len(Qtable[state])), key=lambda action: Qtable[state][action]))
    return max(range(len(Qtable[state])), key=lambda action: Qtable[state][action])
 
def update_qtable(state, action, new_state, reward, max_next_action):
    Qtable[state][action] += alpha * (reward + (gamma * (max_next_action - Qtable[state][action])))
 
def get_action_cmd(action):
    actions = ["left", "right", "jump"]
    return actions[action]
def get_max(state):
    print(max(Qtable[state][0], Qtable[state][1], Qtable[state][2]))
    return max(Qtable[state][0], Qtable[state][1], Qtable[state][2])
 
def choose_action(state):
    return get_max_action(state)
 
def learning():
    connection = cn.connect(2037)
    current_state, reward = cn.get_state_reward(connection, "jump")
 
    episode_count = 0
    while True:
        action = choose_action(to_int(current_state))
        action_cmd = get_action_cmd(action)
        new_state, reward = cn.get_state_reward(connection, action_cmd)
        max_next_action = get_max(to_int(new_state))
 
        update_qtable(to_int(current_state), action, to_int(new_state), reward, max_next_action)
        current_state = new_state
 
        episode_count += 1
        print(f"Episode {episode_count}, Action: {action_cmd}, Total Rewards: {reward}", end="\r")
 
        if episode_count % 50 == 0:
            save_table()
            print("Table updated.")
 
def to_int(txt):
    return int(txt, 2)
 
def main():
    init()
    learning()
 
if __name__ == "__main__":
    main()