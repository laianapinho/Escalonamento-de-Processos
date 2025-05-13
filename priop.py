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

    while tarefas_restantes or fila_prontos or processo_em_execucao:
        # Adiciona tarefas que chegaram à fila de prontos
        for tarefa in list(tarefas_restantes):
            if tarefa.tempoIngresso <= tempoAtual:
                fila_prontos.append(tarefa)
                tarefas_restantes.remove(tarefa)

        # Preempção: troca se houver tarefa com prioridade menor (maior prioridade)
        if processo_em_execucao and fila_prontos:
            mais_prioritaria = min(fila_prontos, key=lambda tarefa: tarefa.prioridade)
            if mais_prioritaria.prioridade < processo_em_execucao.prioridade:
                fila_prontos.append(processo_em_execucao)
                processo_em_execucao = None

        # Se não há processo em execução, escolhe o de maior prioridade (menor número)
        if not processo_em_execucao and fila_prontos:
            processo_em_execucao = min(fila_prontos, key=lambda tarefa: tarefa.prioridade)
            fila_prontos.remove(processo_em_execucao)

            if processo_em_execucao.nome not in tempo_inicio_execucao:
                tempo_inicio_execucao[processo_em_execucao.nome] = tempoAtual
                print(f"Processo {processo_em_execucao.nome} começou no tempo {tempoAtual}")

        # Executa o processo atual por 1 unidade de tempo
        if processo_em_execucao:
            tempo_restante[processo_em_execucao.nome] -= 1
            ordem_execucao.append((processo_em_execucao.nome, tempoAtual))

            # Atualiza o tempo de espera de processos na fila
            for tarefa in fila_prontos:
                tempo_espera[tarefa.nome] += 1

            # Finaliza se tempo restante for zero
            if tempo_restante[processo_em_execucao.nome] == 0:
                tempo_fim_execucao[processo_em_execucao.nome] = tempoAtual + 1
                print(f"Processo {processo_em_execucao.nome} completado no tempo {tempoAtual + 1}")
                processo_em_execucao = None

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

    print("Tempo Médio de Execução:", tempomedioexecucao)
    print("Tempo Médio de Espera:", tempomedioespera)
