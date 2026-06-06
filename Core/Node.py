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


class VariavelNode:
    def __init__(self, nome):
        self.nome = nome

class AtribuicaoNode:
    def __init__(self, nome,valor):
        self.nome = nome
        self.valor = valor

class BoleanoNode:
    def __init__(self, nome):
        self.nome = nome

class IfNode:
    def __init__(self, condicao, caso_verdadeiro, caso_falso):
        self.condicao = condicao
        self.caso_verdadeiro = caso_verdadeiro
        self.caso_falso = caso_falso

class WhileNode:
    def __init__(self, condicao, corpo):
        self.condicao = condicao
        self.corpo = corpo

class StringNode:
    def __init__(self, valor):
        self.valor = valor

class PrintNode:
    def __init__(self, valor):
        self.valor = valor
