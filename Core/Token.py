# Tipos de Tokens #

TK_INT = "INTEIRO"
TK_FLOAT = "DECIMAL"
TK_STRING = "STRING"
TK_BOOL = "BOOL"

TK_SUM = "SOMA"
TK_SUB = "SUBTRACAO"
TK_MUL = "MULTIPLICACAO"
TK_DIV = "DIVISAO"

TK_EPARENTESES = "PARENTESES_ESQUERDA"
TK_DPARENTESES = "PARENTESES_DIREITA"

TK_IDENTIFICADOR = "IDENTIFICADOR"
TK_ATRIBUICAO = "ATRIBUICAO"

TK_IGUAL_A = "IGUAL_A"
TK_DIFERENTE = "DIFERENTE"
TK_MAIOR = "MAIOR"
TK_MENOR = "MENOR"

TK_IF = "IF"
TK_THEN = "THEN"
TK_ELSE = "ELSE"

TK_AND = "AND"
TK_OR = "OR"
TK_NOT = "NOT"

TK_WHILE = "WHILE"

# Finalizando tipos de tokens #

class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        return f"Tipo:({self.tipo} / Valor: {self.valor})"