# Importando o módulo de conexão e a biblioteca random
import connection as cn
import random

# Definindo os hiperparâmetros do algoritmo Q-learning
alpha = 0.1  # Taxa de aprendizado
gamma = 0.4  # Fator de desconto para recompensas futuras

# Inicializando a tabela Q
Qtable = []

# Função para inicializar a tabela Q a partir de um arquivo
def init():
    with open("resultado.txt", "r") as f:
        lines = f.readlines()

    for line in lines:
        values = [float(value) for value in line.split()]
        Qtable.append(values)

# Função para salvar a tabela Q em um arquivo
def save_table():
    with open("resultado.txt", "w") as f:
        for row in Qtable:
            f.write(" ".join(map(str, row)) + "\n")

# Função para escolher a ação com o maior valor na tabela Q para um estado
def choose_action(state):
    return get_max_action(state)

# Função para obter a ação com o maior valor para um estado
def get_max_action(state):
    return max(range(len(Qtable[state])), key=lambda action: Qtable[state][action])

# Função para atualizar a tabela Q com base nas recompensas e valores máximos futuros
def update_qtable(state, action, new_state, reward, max_next_action):
    Qtable[state][action] += alpha * (reward + (gamma * (max_next_action - Qtable[state][action])))

# Função para converter uma representação binária em um número inteiro
def to_int(txt):
    return int(txt, 2)

# Função para executar o processo de aprendizado
def learning():
    # Conectando ao ambiente de simulação
    connection = cn.connect(2037)
    
    # Obtendo o estado inicial e recompensa
    current_state, reward = cn.get_state_reward(connection, "jump")

    episode_count = 0
    while True:
        # Escolhendo ação com base no estado atual
        action = choose_action(to_int(current_state))
        action_cmd = get_action_cmd(action)
        
        # Obtendo novo estado e recompensa com ação escolhida
        new_state, reward = cn.get_state_reward(connection, action_cmd)
        max_next_action = get_max(to_int(new_state))
        
        # Atualizando a tabela Q com base nas informações obtidas
        update_qtable(to_int(current_state), action, to_int(new_state), reward, max_next_action)
        current_state = new_state
        
        episode_count += 1
        print(f"Episode {episode_count}, Action: {action_cmd}, Total Rewards: {reward}", end="\r")
        
        if episode_count % 50 == 0:
            # Salvando a tabela Q periodicamente
            save_table()
            print("Table updated.")

# Função para obter a ação correspondente ao índice
def get_action_cmd(action):
    actions = ["left", "right", "jump"]
    return actions[action]

# Função para obter o valor máximo entre três valores da Qtable
def get_max(state):
    return max(Qtable[state][0], Qtable[state][1], Qtable[state][2])

# Função principal
def main():
    init()      
    learning()  

# Iniciando o programa
if __name__ == "__main__":
    main()