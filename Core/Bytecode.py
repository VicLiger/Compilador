class Bytecode:
    def __init__(self):
        self.codigo = []

    def gerar(self, node):
        tipo_node = type(node).__name__

        if tipo_node == "NumeroNode":
            self.codigo.append(f"PUSH {node.token.valor}")

        elif tipo_node == "BoleanoNode":
            self.codigo.append(f"PUSH {node.nome}")

        elif tipo_node == "StringNode":
            self.codigo.append(f'PUSH "{node.valor}"')

        elif tipo_node == "VariavelNode":
            self.codigo.append(f"LOAD {node.nome}")

        elif tipo_node == "AtribuicaoNode":
            self.gerar(node.valor)
            self.codigo.append(f"STORE {node.nome}")

        elif tipo_node == "OperacaoBinariaNode":
            self.gerar(node.esquerda)
            self.gerar(node.direita)

            if node.operador.tipo == "SOMA":
                self.codigo.append("ADD")
            elif node.operador.tipo == "SUBTRACAO":
                self.codigo.append("SUB")
            elif node.operador.tipo == "MULTIPLICACAO":
                self.codigo.append("MUL")
            elif node.operador.tipo == "DIVISAO":
                self.codigo.append("DIV")
            elif node.operador.tipo == "MAIOR":
                self.codigo.append("GT")
            elif node.operador.tipo == "MENOR":
                self.codigo.append("LT")
            elif node.operador.tipo == "IGUAL_A":
                self.codigo.append("EQ")
            elif node.operador.tipo == "DIFERENTE":
                self.codigo.append("NEQ")
            elif node.operador.tipo == "AND":
                self.codigo.append("AND")
            elif node.operador.tipo == "OR":
                self.codigo.append("OR")

        elif tipo_node == "OperacaoUnariaNode":
            self.gerar(node.node)

            if node.operador.tipo == "SUBTRACAO":
                self.codigo.append("NEG")
            elif node.operador.tipo == "NOT":
                self.codigo.append("NOT")

        elif tipo_node == "PrintNode":
            self.gerar(node.valor)
            self.codigo.append("PRINT")

        elif tipo_node == "ReadNode":
            self.codigo.append(f"READ {node.nome}")

        elif tipo_node == "ReturnNode":
            self.gerar(node.valor)
            self.codigo.append("RETURN")

    def obter_codigo(self):
        return "\n".join(self.codigo)