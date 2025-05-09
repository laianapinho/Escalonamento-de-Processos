
from tarefa import Tarefa
from collections import deque

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

def executar_rr(tarefas):
    quantum = int(input("Informe o quantum: "))
    tempoAtual = 0
    somaTempoEspera = 0
    somaTempoExecucao = 0
    total_tarefas = len(tarefas)  # Número total de tarefas
    tarefas_restantes = tarefas.copy()  # Cópia das tarefas que ainda não foram concluídas
    ordem_execucao = []  # Lista para registrar a ordem e os intervalos de execução
    fila_prontos = deque()  # Fila das tarefas prontas para executar (implementação do Round Robin)

# Inicializa atributos auxiliares em cada tarefa
    for tarefa in tarefas:
        tarefa.duracao_restante = tarefa.duracao  # Quanto tempo ainda falta para terminar
        tarefa.tempoTermino = None  # Quando a tarefa foi finalizada

# Loop principal: continua enquanto houver tarefas pendentes ou na fila
    while len(tarefas_restantes) > 0 or len(fila_prontos) > 0:
    # Adiciona à fila de prontos as tarefas cujo tempo de ingresso já chegou
        for tarefa in list(tarefas_restantes):  # Faz uma cópia da lista para poder alterar dentro do loop
            if tarefa.tempoIngresso <= tempoAtual:
                fila_prontos.append(tarefa)
                tarefas_restantes.remove(tarefa)

        if len(fila_prontos) != 0:
        # Retira a próxima tarefa da fila
            tarefa = fila_prontos.popleft()

            inicio = tempoAtual  # Marca o início da execução desta fatia
            tempo_execucao = min(quantum, tarefa.duracao_restante)  # Executa até o quantum ou o tempo restante
            tempoAtual += tempo_execucao  # Atualiza o tempo atual
            fim = tempoAtual  # Marca o fim desta fatia
            tarefa.duracao_restante -= tempo_execucao  # Reduz o tempo restante da tarefa

        # Registra essa execução na lista de ordem
            ordem_execucao.append((tarefa.nome, inicio, fim))

        # Verifica se novas tarefas chegaram enquanto esta executava
            for t in list(tarefas_restantes):
                if t.tempoIngresso <= tempoAtual:
                    fila_prontos.append(t)
                    tarefas_restantes.remove(t)

            if tarefa.duracao_restante == 0:
            # A tarefa terminou, então calculamos tempos finais
                tarefa.tempoTermino = tempoAtual
                tarefa.tempoExecucao = tarefa.tempoTermino - tarefa.tempoIngresso
                tarefa.tempoEspera = tarefa.tempoExecucao - tarefa.duracao

            # Acumulamos os tempos para depois calcular as médias
                somaTempoExecucao += tarefa.tempoExecucao
                somaTempoEspera += tarefa.tempoEspera
            else:
            # A tarefa não terminou, então volta para o final da fila
                fila_prontos.append(tarefa)
        else:
        # Nenhuma tarefa pronta ainda, avança o tempo até a próxima tarefa chegar
            tempoAtual += 1

# Cálculo das médias após a simulação
    tempomedioexecucao = somaTempoExecucao / total_tarefas
    tempomedioespera = somaTempoEspera / total_tarefas

# Impressão da ordem de execução com intervalos
    print("\nOrdem de execução:")
    for nome, inicio, fim in ordem_execucao:
        print(f"{nome} executou de {inicio} até {fim}")

# Impressão dos tempos médios
    print("Tempo Médio de Execução", tempomedioexecucao)
    print("Tempo Médio de Espera", tempomedioespera)