
class Interpreter:

    def __init__(self):
        self.variaveis = {}
        self.funcoes = {}

    def visitar(self, node):
        tipo_node = type(node).__name__

        if tipo_node == "VariavelNode":
            return self.variaveis[node.nome]

        if tipo_node == "NumeroNode":
            return node.token.valor

        if tipo_node == "BoleanoNode":
            return node.nome

        if tipo_node == "StringNode":
            return node.valor

        if tipo_node == "ReturnNode":
            return self.visitar(node.valor)

        if tipo_node == "AtribuicaoNode":
            valor = self.visitar(node.valor)
            self.variaveis[node.nome] = valor
            return valor

        if tipo_node == "IfNode":
            condicao = self.visitar(node.condicao)

            if condicao:
                return self.visitar(node.caso_verdadeiro)

            return self.visitar(node.caso_falso)

        if tipo_node == "PrintNode":
            valor = self.visitar(node.valor)
            print(valor)
            return valor

        if tipo_node == "ReadNode":
            valor = input(f"Digite o valor de {node.nome}: ")

            if valor.isdigit():
                valor = int(valor)

            self.variaveis[node.nome] = valor
            return valor

        if tipo_node == "WhileNode":
            resultado = None

            while self.visitar(node.condicao):
                resultado = self.visitar(node.corpo)

            return resultado

        if tipo_node == "FuncaoNode":
            self.funcoes[node.nome] = node
            return None

        if tipo_node == "ChamarFuncaoNode":
            funcao = self.funcoes[node.nome]

            valor_argumento = self.visitar(node.argumento)

            variaveis_antigas = self.variaveis.copy()

            self.variaveis[funcao.parametro] = valor_argumento

            resultado = self.visitar(funcao.corpo)

            self.variaveis = variaveis_antigas

            return resultado


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