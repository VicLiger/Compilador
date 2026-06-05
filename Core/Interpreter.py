class Interpreter:

    def visitar(self, node):

        if type(node).__name__ == "NumeroNode":
            return node.token.valor

        if type(node).__name__ == "OperacaoBinariaNode":

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