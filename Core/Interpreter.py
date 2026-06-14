class Interpreter:

    def __init__(self):
        self.tabela_simbolos = {}
        self.funcoes = {}

    def obter_tipo(self, valor):
        if isinstance(valor, bool):
            return "bool"
        if isinstance(valor, int):
            return "int"
        if isinstance(valor, float):
            return "float"
        if isinstance(valor, str):
            return "string"
        return "desconhecido"


    def visitar(self, node):
        tipo_node = type(node).__name__

        if tipo_node == "VariavelNode":
            if node.nome not in self.tabela_simbolos:
                raise Exception(
                    f"Erro Semântico: variável '{node.nome}' não declarada"
                )
            return self.tabela_simbolos[node.nome]["valor"]

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
            self.tabela_simbolos[node.nome] = {
                "valor": valor,
                "tipo": self.obter_tipo(valor),
                "escopo": "global"
            }
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

            self.tabela_simbolos[node.nome] = {
                "valor": valor,
                "tipo": self.obter_tipo(valor),
                "escopo": "global"
            }
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

            tabela_antiga = self.tabela_simbolos.copy()

            self.tabela_simbolos[funcao.parametro] = {
                "valor": valor_argumento,
                "tipo": self.obter_tipo(valor_argumento),
                "escopo": "local"
            }

            resultado = self.visitar(funcao.corpo)

            self.tabela_simbolos = tabela_antiga

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
                self.verificar_tipo(esquerda, direita)
                return esquerda + direita

            if node.operador.tipo == "SUBTRACAO":
                self.verificar_tipo(esquerda, direita)
                return esquerda - direita

            if node.operador.tipo == "MULTIPLICACAO":
                self.verificar_tipo(esquerda, direita)
                return esquerda * direita

            if node.operador.tipo == "DIVISAO":
                self.verificar_tipo(esquerda, direita)
                return esquerda / direita


            if node.operador.tipo == "MAIOR":
                self.verificar_tipo(esquerda, direita)
                return esquerda > direita
            if node.operador.tipo == "MENOR":
                self.verificar_tipo(esquerda, direita)
                return esquerda < direita
            if node.operador.tipo == "IGUAL_A":
                self.verificar_tipo(esquerda, direita)
                return esquerda == direita
            if node.operador.tipo == "DIFERENTE":
                self.verificar_tipo(esquerda, direita)
                return esquerda != direita


            if node.operador.tipo == "AND":
                if not isinstance(esquerda,bool) or not isinstance(direita,bool):
                    raise Exception("Erro semântico, operador AND precisa ser True/False")
                return esquerda and direita
            if node.operador.tipo == "OR":
                if not isinstance(esquerda, bool) or not isinstance(direita, bool):
                    raise Exception("Erro semântico, operador OR precisa ser True/False")
                return esquerda or direita


    def verificar_tipo(self,esquerda,direita):
        if type(esquerda) != type(direita):
            raise Exception(
                f"Erro semânmtico: tipos incompátivei ({type(esquerda).__name__} e {type(direita).__name__})"
            )