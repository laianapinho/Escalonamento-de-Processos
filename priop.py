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

def executar_priop(tarefas):
    tempoAtual = 0
    somaTempoEspera = 0
    somaTempoExecucao = 0
    tempo_restante = {tarefa.nome: tarefa.duracao for tarefa in tarefas}  # Dicionário para armazenar o tempo restante de cada tarefa
    tempo_espera = {tarefa.nome : 0  for tarefa in tarefas}   # Inicializa o tempo de espera de todas as tarefas como 0
    # Dicionários para registrar o início e fim de execução de cada tarefa
    tempo_inicio_execucao = {}  # Armazena o tempo de início da execução de cada processo
    tempo_fim_execucao = {} # Armazena o tempo de término da execução de cada processo
    total_tarefas = len(tarefas) # Número total de tarefas
    fila_prontos = deque() #Fila de prontos
    tarefas_restantes = tarefas.copy()  # Lista de tarefas que ainda não entraram na fila
    processo_em_execucao = None #Processo atualmente em execução
    ordem_execucao = []

    # Loop principal: continua até que todas as tarefas sejam finalizadas
    while tarefas_restantes or fila_prontos or processo_em_execucao:
    # Verifica quais tarefas já chegaram e move para fila de prontos
        for tarefa in list(tarefas_restantes):
            if tarefa.tempoIngresso <= tempoAtual:
                fila_prontos.append(tarefa)
                tarefas_restantes.remove(tarefa)

        # Se há processo em execução e chega um com prioridade maior, faz preempção
        if processo_em_execucao and fila_prontos:
            maior = max(fila_prontos, key=lambda tarefa: tarefa.prioridade)
            if maior.prioridade > processo_em_execucao.prioridade:
                fila_prontos.append(processo_em_execucao)
                processo_em_execucao = None

        # Se não há processo em execução, seleciona o de maior prioridade da fila
        if not processo_em_execucao and fila_prontos:
            processo_em_execucao = max(fila_prontos, key=lambda tarefa: tarefa.prioridade)
            fila_prontos.remove(processo_em_execucao)

            # Registra o tempo de início de execução, se ainda não registrado
            if processo_em_execucao.nome not in tempo_inicio_execucao:
                tempo_inicio_execucao[processo_em_execucao.nome] = tempoAtual
                print(f"Processo {processo_em_execucao.nome} começou no tempo {tempoAtual}")

        # Executa o processo atual por 1 unidade de tempo
        if processo_em_execucao:
            tempo_restante[processo_em_execucao.nome] -= 1
            ordem_execucao.append((processo_em_execucao.nome, tempoAtual))
            # Incrementa tempo de espera para processos que estão aguardando na fil
            for tarefa in fila_prontos:
                tempo_espera[tarefa.nome] += 1

            # Se o processo terminou, registra o fim de execução e libera o processador
            if tempo_restante[processo_em_execucao.nome] == 0:
                tempo_fim_execucao[processo_em_execucao.nome] = tempoAtual + 1
                print(f"Processo {processo_em_execucao.nome} completado no tempo {tempoAtual + 1}")
                processo_em_execucao = None

        # Avança o tempo do relógio
        tempoAtual += 1

    # Cálculo dos tempos médios
    for tarefa in tarefas:
        tempo_execucao = tempo_fim_execucao[tarefa.nome] - tarefa.tempoIngresso
        somaTempoExecucao += tempo_execucao
        somaTempoEspera += tempo_espera[tarefa.nome]

    tempomedioexecucao = somaTempoExecucao / total_tarefas
    tempomedioespera = somaTempoEspera / total_tarefas

    print("\nOrdem de execução:")
    for nome, tempo in ordem_execucao:
        print(f"{nome} executado no tempo {tempo}")

    print("Tempo Médio de Execução",tempomedioexecucao)
    print("Tempo Médio de Espera",tempomedioespera)