from tarefa import Tarefa
from collections import deque

def ler_tarefas_de_arquivo(nome_arquivo):
    tarefas = []
    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            if linha.strip() == "":
                continue
            dados = linha.strip().split()
            nome = dados[0]
            tempoIngresso = int(dados[1])
            duracao = int(dados[2])
            prioridade = int(dados[3])
            tipo = int(dados[4])
            tarefas.append(Tarefa(nome, tempoIngresso, duracao, prioridade, tipo))
    return tarefas

def executar_srtf(tarefas):
    tempoAtual = 0
    somaTempoEspera = 0  
    somaTempoExecucao = 0 
    tempo_restante = {t.nome: t.duracao for t in tarefas}
    tempo_espera = {t.nome: 0 for t in tarefas}
    tempo_inicio_execucao = {}
    tempo_fim_execucao = {}
    total_tarefas = len(tarefas)
    fila_prontos = deque()
    tarefas_restantes = tarefas.copy()
    processo_em_execucao = None
    ordem_execucao = []

    while tarefas_restantes or fila_prontos or processo_em_execucao:
        # Adiciona à fila de prontos as tarefas cujo tempo de ingresso chegou
        for tarefa in list(tarefas_restantes):
            if tarefa.tempoIngresso <= tempoAtual:
                fila_prontos.append(tarefa)
                tarefas_restantes.remove(tarefa)

        # Se o processo atual existe e há outro com menor tempo restante, interrompe
        if processo_em_execucao and fila_prontos:
            menor = min(fila_prontos, key=lambda t: tempo_restante[t.nome])
            if tempo_restante[menor.nome] < tempo_restante[processo_em_execucao.nome]:
                fila_prontos.append(processo_em_execucao)
                processo_em_execucao = None

        # Se não há processo em execução, pega o próximo da fila
        if not processo_em_execucao and fila_prontos:
            processo_em_execucao = min(fila_prontos, key=lambda t: tempo_restante[t.nome])
            fila_prontos.remove(processo_em_execucao)
            if processo_em_execucao.nome not in tempo_inicio_execucao:
                tempo_inicio_execucao[processo_em_execucao.nome] = tempoAtual
            print(f"Processo {processo_em_execucao.nome} começou no tempo {tempoAtual}")

        # Executa o processo atual
        if processo_em_execucao:
            tempo_restante[processo_em_execucao.nome] -= 1
            ordem_execucao.append((processo_em_execucao.nome, tempoAtual))

            # Atualiza espera dos outros na fila
            for tarefa in fila_prontos:
                tempo_espera[tarefa.nome] += 1

            # Verifica se o processo terminou
            if tempo_restante[processo_em_execucao.nome] == 0:
                tempo_fim_execucao[processo_em_execucao.nome] = tempoAtual + 1
                print(f"Processo {processo_em_execucao.nome} completado no tempo {tempoAtual + 1}")
                processo_em_execucao = None

        tempoAtual += 1

    # Cálculo dos tempos médios
    for t in tarefas:
        tempo_execucao = tempo_fim_execucao[t.nome] - t.tempoIngresso
        somaTempoExecucao += tempo_execucao
        somaTempoEspera += tempo_espera[t.nome]

    tempomedioexecucao = somaTempoExecucao / total_tarefas
    tempomedioespera = somaTempoEspera / total_tarefas

    print("\nOrdem de execução:")
    for nome, tempo in ordem_execucao:
        print(f"{nome} executado no tempo {tempo}")

    print("Tempo Médio de Execução",tempomedioexecucao)
    print("Tempo Médio de Espera",tempomedioespera)
