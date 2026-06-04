# Tipos de Tokens #

TK_INT = "INTEIRO"
TK_FLOAT = "DECIMAL"
TK_STRING = "STRING"
TK_BOOL = "BOOL"

TK_SUM = "SOMA"
TK_SUB = "SUBTRACAO"
TK_MUL = "MULTIPLACAO"
TK_DIV = "DIVISAO"

TK_EPARENTESES = "PARENTESES_ESQUERDA"
TK_DPARENTESES = "PARENTESES_DIREITA"

# Finalizando tipos de tokens #

class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        return f"Tipo:({self.tipo} / Valor: {self.valor})"
