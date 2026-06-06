class Interpreter:

    def visitar(self, node):
        tipo_node = type(node).__name__

        if tipo_node == "NumeroNode":
            return node.token.valor

        if tipo_node == "OperacaoUnariaNode":
            numero = self.visitar(node.node)
            if node.operador.tipo == "SOMA":
                return +numero
            if node.operador.tipo == "SUBTRACAO":
                return -numero

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