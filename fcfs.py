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

def executar_fcfs(tarefas):
#Ordena pelo tempo de ingresso de cada tarefa
    tarefas.sort(key=lambda tarefa: tarefa.tempoIngresso)

    tempoAtual = 0
    somaTempoEspera = 0
    somaTempoExecucao = 0

#Percorre cada tarefa da lista ordenada
    for i in range(len(tarefas)):
        if (tarefas[i].tempoIngresso > tempoAtual): # Verifica se a tarefa ainda não pode ser executada
            tempoAtual = tarefas[i].tempoIngresso  # Atualiza o tempo atual para o tempo de ingresso da tarefa

        tempoAtual += tarefas[i].duracao # Adiciona a duração da tarefa ao tempo atual

        tempoTermino = tempoAtual  # O tempo de término é o tempo atual após a execução da tarefa
        tempoexecucao = tempoTermino - tarefas[i].tempoIngresso # O tempo de execução é a diferença entre o tempo de término e o tempo de ingresso
        tempoespera = tempoexecucao - tarefas[i].duracao # O tempo de espera é a diferença entre o tempo de execução e a duração da tarefa

        # Atribui os valores calculados aos atributos da tarefa
        tarefas[i].tempoTermino = tempoTermino 
        tarefas[i].tempoExecucao = tempoexecucao  
        tarefas[i].tempoEspera = tempoespera 


        # Acumula os tempos de execução e de espera
        somaTempoExecucao += tarefas[i].tempoExecucao
        somaTempoEspera += tarefas[i].tempoEspera

    # Calcula a média dos tempos de execução e espera
    tempomedioexecucao = somaTempoExecucao/len(tarefas) #Média do Tempo de Execução
    tempomedioespera = somaTempoEspera/len(tarefas) #Média do Tempo de Espera

    # Exibibição da ordem de execução das tarefas
    print("Ordem de execução:")
    for tarefa in tarefas:
        print(tarefa.nome)

    # Exibe do tempo médio de execução e tempo médio de espera
    print("Tempo Médio de Execução",tempomedioexecucao)
    print("Tempo Médio de Espera",tempomedioespera)