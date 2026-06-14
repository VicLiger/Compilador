class TAC:
    def __init__(self):
        self.codigo = []
        self.contador_temp = 0

    def novo_temp(self):
        self.contador_temp += 1
        return f"t{self.contador_temp}"

    def gerar(self, node):
        tipo_node = type(node).__name__

        if tipo_node == "NumeroNode":
            return str(node.token.valor)

        if tipo_node == "BoleanoNode":
            return str(node.nome)

        if tipo_node == "StringNode":
            return f'"{node.valor}"'

        if tipo_node == "VariavelNode":
            return node.nome

        if tipo_node == "AtribuicaoNode":
            valor = self.gerar(node.valor)
            self.codigo.append(f"{node.nome} = {valor}")
            return node.nome

        if tipo_node == "OperacaoBinariaNode":
            esquerda = self.gerar(node.esquerda)
            direita = self.gerar(node.direita)

            temp = self.novo_temp()

            self.codigo.append(
                f"{temp} = {esquerda} {node.operador.valor} {direita}"
            )

            return temp

        if tipo_node == "OperacaoUnariaNode":
            valor = self.gerar(node.node)

            temp = self.novo_temp()

            self.codigo.append(
                f"{temp} = {node.operador.valor}{valor}"
            )

            return temp

        if tipo_node == "PrintNode":
            valor = self.gerar(node.valor)
            self.codigo.append(f"print {valor}")
            return valor

        if tipo_node == "ReturnNode":
            valor = self.gerar(node.valor)
            self.codigo.append(f"return {valor}")
            return valor

        if tipo_node == "IfNode":
            condicao = self.gerar(node.condicao)

            label_else = f"L{self.contador_temp + 1}"
            label_fim = f"L{self.contador_temp + 2}"

            self.codigo.append(f"ifFalse {condicao} goto {label_else}")

            self.gerar(node.caso_verdadeiro)
            self.codigo.append(f"goto {label_fim}")

            self.codigo.append(f"{label_else}:")
            self.gerar(node.caso_falso)

            self.codigo.append(f"{label_fim}:")
            return None

        if tipo_node == "WhileNode":
            label_inicio = f"L{self.contador_temp + 1}"
            label_fim = f"L{self.contador_temp + 2}"

            self.codigo.append(f"{label_inicio}:")

            condicao = self.gerar(node.condicao)

            self.codigo.append(f"ifFalse {condicao} goto {label_fim}")

            self.gerar(node.corpo)

            self.codigo.append(f"goto {label_inicio}")
            self.codigo.append(f"{label_fim}:")

            return None

    def obter_codigo(self):
        return "\n".join(self.codigo)