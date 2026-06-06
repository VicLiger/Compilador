class Interpreter:

    def __init__(self):
        self.variaveis = {}

    def visitar(self, node):
        tipo_node = type(node).__name__

        if tipo_node == "VariavelNode":
            return self.variaveis[node.nome]

        if tipo_node == "NumeroNode":
            return node.token.valor

        if tipo_node == "BoleanoNode":
            return node.nome

        if tipo_node == "AtribuicaoNode":
            valor = self.visitar(node.valor)
            self.variaveis[node.nome] = valor
            return valor

        if tipo_node == "IfNode":
            condicao = self.visitar(node.condicao)

            if condicao:
                return self.visitar(node.caso_verdadeiro)

            return self.visitar(node.caso_falso)


        if tipo_node == "OperacaoUnariaNode":
            numero = self.visitar(node.node)
            if node.operador.tipo == "SOMA":
                return +numero
            if node.operador.tipo == "SUBTRACAO":
                return -numero
            if node.operador.tipo == "NOT":
                return not numero

        if tipo_node == "OperacaoBinariaNode":
            esquerda = self.visitar(node.esquerda)
            direita = self.visitar(node.direita)

            if node.operador.tipo == "SOMA":
                return esquerda + direita

            if node.operador.tipo == "SUBTRACAO":
                return esquerda - direita

            if node.operador.tipo == "MULTIPLICACAO":
                return esquerda * direita

            if node.operador.tipo == "DIVISAO":
                return esquerda / direita


            if node.operador.tipo == "MAIOR":
                return esquerda > direita
            if node.operador.tipo == "MENOR":
                return esquerda < direita
            if node.operador.tipo == "IGUAL_A":
                return esquerda == direita
            if node.operador.tipo == "DIFERENTE":
                return esquerda != direita


            if node.operador.tipo == "AND":
                return esquerda and direita
            if node.operador.tipo == "OR":
                return esquerda or direita