from tarefa import Tarefa

tarefas = []

def ler_tarefas_de_arquivo(nome_arquivo):
    tarefas = []
    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            if linha.strip() == "":
                continue  # pula a linha vazia
            dados = linha.strip().split()
            nome = dados[0]
            tempoIngresso = int(dados[1])
            duracao = int(dados[2])
            prioridade = int(dados[3])
            tipo = int(dados[4])
            tarefas.append(Tarefa(nome, tempoIngresso, duracao, prioridade, tipo))
    return tarefas

def executar_sjf(tarefas):
    tempoAtual = 0
    somaTempoEspera = 0
    somaTempoExecucao = 0
    total_tarefas = len(tarefas)
    ordem_execucao = []

    while len(tarefas) != 0:

    # Cria a lista tarefas disponiveis vazias, ela guarda, em cada momento do seu algoritmo, quais tarefas já chegaram e estão prontas para serem executadas.
        tarefas_disponiveis = []
        for tarefa in tarefas: #Percorre uma por uma as tarefas
            if tarefa.tempoIngresso <= tempoAtual:
                tarefas_disponiveis.append(tarefa) #Se a tarefa já tiver chegado, adiciona ela na lista


    # Escolhe a tarefa de menor duração entre as disponíveis
        tarefaselecionada = min(tarefas_disponiveis, key=lambda tarefa: tarefa.duracao)


    # Atualiza o tempo atual com a duração da tarefa executada
        tempoAtual += tarefaselecionada.duracao 

        tempoTermino = tempoAtual  # O tempo de término é o tempo atual após a execução da tarefa
        tempoexecucao = tempoTermino - tarefaselecionada.tempoIngresso # O tempo de execução é a diferença entre o tempo de término e o tempo de ingresso
        tempoespera = tempoexecucao - tarefaselecionada.duracao # O tempo de espera é a diferença entre o tempo de execução e a duração da tarefa

        tarefas.remove(tarefaselecionada)
        ordem_execucao.append(tarefaselecionada)

    # Atribui os valores calculados aos atributos da tarefa
        tarefaselecionada.tempoTermino = tempoTermino 
        tarefaselecionada.tempoExecucao = tempoexecucao  
        tarefaselecionada.tempoEspera = tempoespera 


    # Acumula os tempos de execução e de espera
        somaTempoExecucao += tarefaselecionada.tempoExecucao
        somaTempoEspera += tarefaselecionada.tempoEspera

# Calcula a média dos tempos de execução e espera
    tempomedioexecucao = somaTempoExecucao/total_tarefas #Média do Tempo de Execução
    tempomedioespera = somaTempoEspera/total_tarefas #Média do Tempo de Espera

# Exibibição da ordem de execução das tarefas
    print("Ordem de execução:")
    for tarefa in ordem_execucao:
        print(tarefa.nome)

# Exibe do tempo médio de execução e tempo médio de espera
    print("Tempo Médio de Execução",tempomedioexecucao)
    print("Tempo Médio de Espera",tempomedioespera)