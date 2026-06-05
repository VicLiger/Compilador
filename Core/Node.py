class NumeroNode:
    def __init__(self, token):
        self.token = token


class OperacaoBinariaNode:
    def __init__(self, esquerda, operador, direita):
        self.esquerda = esquerda
        self.operador = operador
        self.direita = direita


class OperacaoUnariaNode:
    def __init__(self, operador, node):
        self.operador = operador
        self.node = node