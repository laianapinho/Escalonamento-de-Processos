class Tarefa:
    def __init__(self, nome, tempoIngresso, duracao,prioridade,tipo):  # Método construtor
        self.nome = nome
        self.tempoIngresso = tempoIngresso
        self.duracao = duracao
        self.prioridade = prioridade
        self.tipo = tipo

    def impressao(self):
        print(f"Nome: {self.nome},tempo de ingresso: {self.tempoIngresso}, duracao: {self.duracao}, prioridade: {self.prioridade}, tipo: {self.tipo}")


