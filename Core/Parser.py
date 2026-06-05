from Core.Node import NumeroNode, OperacaoBinariaNode, OperacaoUnariaNode


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.indice = -1
        self.token_atual = None
        self.avancar()

    def avancar(self):
        self.indice += 1

        if self.indice < len(self.tokens):
            self.token_atual = self.tokens[self.indice]
        else:
            self.token_atual = None

    def processar_fator(self):
        token = self.token_atual

        if token.tipo in ["SOMA", "SUBTRACAO"]:
            self.avancar()
            node = self.processar_fator()
            return OperacaoUnariaNode(token, node)

        if token.tipo in ["INTEIRO", "DECIMAL"]:
            self.avancar()
            return NumeroNode(token)

        if token.tipo == "PARENTESES_ESQUERDA":
            self.avancar()
            resultado = self.processar_expressao()
            
            if self.token_atual is not None and self.token_atual.tipo == "PARENTESES_DIREITA":
                self.avancar()
                return resultado
            raise Exception("Erro de Sintaxe: Esperado ')'")

    def processar_operacao(self, funcao, operadores):
        esquerda = funcao()

        while self.token_atual is not None and self.token_atual.tipo in operadores:
            operador = self.token_atual
            self.avancar()
            direita = funcao()

            esquerda = OperacaoBinariaNode(esquerda, operador, direita)

        return esquerda

    def processar_multiplicacao_divisao(self):
        return self.processar_operacao(
            self.processar_fator,
            ["MULTIPLICACAO", "DIVISAO"]
        )

    def processar_expressao(self):
        return self.processar_operacao(
            self.processar_multiplicacao_divisao,
            ["SOMA", "SUBTRACAO"]
        )