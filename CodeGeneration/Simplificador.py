from Core.Node import NumeroNode, OperacaoBinariaNode
from Core.Token import Token


class Simplificador:

    def simplificar(self, node):
        tipo_node = type(node).__name__

        if tipo_node == "OperacaoBinariaNode":
            esquerda = self.simplificar(node.esquerda)
            direita = self.simplificar(node.direita)

            if type(esquerda).__name__ == "NumeroNode" and type(direita).__name__ == "NumeroNode":
                valor_esquerda = esquerda.token.valor
                valor_direita = direita.token.valor

                if node.operador.tipo == "SOMA":
                    return NumeroNode(Token("INTEIRO", valor_esquerda + valor_direita))

                if node.operador.tipo == "SUBTRACAO":
                    return NumeroNode(Token("INTEIRO", valor_esquerda - valor_direita))

                if node.operador.tipo == "MULTIPLICACAO":
                    return NumeroNode(Token("INTEIRO", valor_esquerda * valor_direita))

                if node.operador.tipo == "DIVISAO":
                    return NumeroNode(Token("DECIMAL", valor_esquerda / valor_direita))

            return OperacaoBinariaNode(esquerda, node.operador, direita)

        if tipo_node == "AtribuicaoNode":
            node.valor = self.simplificar(node.valor)
            return node

        if tipo_node == "PrintNode":
            node.valor = self.simplificar(node.valor)
            return node

        if tipo_node == "ReturnNode":
            node.valor = self.simplificar(node.valor)
            return node

        return node