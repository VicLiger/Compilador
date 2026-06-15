# As classes neste arquivo representam os "Nós" (Nodes) da nossa Árvore Sintática Abstrata (AST).
# O Parser usa essas classes para construir uma árvore estruturada que entende a lógica do código.

# Nó que guarda um número (inteiro ou decimal).
class NumeroNode:
    def __init__(self, token):
        self.token = token


# Nó que representa uma operação entre duas partes, como 10 + 5 ou x > y.
class OperacaoBinariaNode:
    def __init__(self, esquerda, operador, direita):
        # O nó que fica à esquerda do operador
        self.esquerda = esquerda
        # O símbolo da operação (ex: SOMA, MULTIPLICACAO)
        self.operador = operador
        # O nó que fica à direita do operador
        self.direita = direita


# Nó para operações aplicadas a apenas um elemento, como números negativos (-5) ou negação lógica (not true).
class OperacaoUnariaNode:
    def __init__(self, operador, node):
        self.operador = operador
        self.node = node


# Nó que representa o uso ou leitura de uma variável.
class VariavelNode:
    def __init__(self, nome):
        self.nome = nome

# Nó que representa a atribuição de um valor a uma variável (ex: x = 10).
class AtribuicaoNode:
    def __init__(self, nome, valor):
        # Nome da variável que receberá o valor
        self.nome = nome
        # O valor a ser guardado (pode ser um número, outra variável, ou até o resultado de uma conta)
        self.valor = valor

# Nó que guarda um valor booleano verdadeiro ou falso (true/false).
class BoleanoNode:
    def __init__(self, nome):
        self.nome = nome

# Nó que representa a estrutura de decisão condicional (if...then...else).
class IfNode:
    def __init__(self, condicao, caso_verdadeiro, caso_falso):
        # Expressão lógica para avaliar se é verdadeiro ou falso
        self.condicao = condicao
        # O que executar se a condição for verdadeira
        self.caso_verdadeiro = caso_verdadeiro
        # O que executar se a condição for falsa (o 'else')
        self.caso_falso = caso_falso

# Nó que representa um laço de repetição (while...then).
class WhileNode:
    def __init__(self, condicao, corpo):
        # Expressão que enquanto for verdadeira manterá o laço rodando
        self.condicao = condicao
        # Bloco de código a ser executado repetidamente
        self.corpo = corpo

# Nó que guarda um texto (string) lido entre aspas.
class StringNode:
    def __init__(self, valor):
        self.valor = valor

# Nó que representa o comando de imprimir algo na tela.
class PrintNode:
    def __init__(self, valor):
        self.valor = valor

# Nó que representa a leitura de um dado digitado pelo usuário.
class ReadNode:
    def __init__(self, nome):
        # Nome da variável onde o que o usuário digitar será guardado
        self.nome = nome

# Nó para definição de uma nova função.
class FuncaoNode:
    def __init__(self, nome, parametro, corpo):
        self.nome = nome
        self.parametro = parametro
        self.corpo = corpo

# Nó para quando executamos/chamamos uma função existente passando um argumento.
class ChamarFuncaoNode:
    def __init__(self, nome, argumento):
        self.nome = nome
        self.argumento = argumento

# Nó para o valor de retorno de uma função.
class ReturnNode:
    def __init__(self, valor):
        self.valor = valor

# Nó que guarda a lista de todos os comandos do programa inteiro.
class ProgramaNode:
    def __init__(self, comandos):
        self.comandos = comandos
