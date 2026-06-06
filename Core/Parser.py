from Core.Node import NumeroNode, OperacaoBinariaNode, OperacaoUnariaNode, VariavelNode, AtribuicaoNode
from Core.Node import BoleanoNode
from Core.Node import IfNode

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

        if token.tipo == "IDENTIFICADOR":
            self.avancar()
            return VariavelNode(token.valor)

        if token.tipo in ["SOMA", "SUBTRACAO", "NOT"]:
            self.avancar()
            node = self.processar_fator()
            return OperacaoUnariaNode(token, node)

        if token.tipo in ["INTEIRO", "DECIMAL"]:
            self.avancar()
            return NumeroNode(token)

        if token.tipo == "BOOL":
            self.avancar()
            return BoleanoNode(token.valor)

        if token.tipo == "PARENTESES_ESQUERDA":
            self.avancar()
            resultado = self.processar_logicos()
            
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

    def processar_comparacao(self):
        return self.processar_operacao(
            self.processar_expressao,
            ["IGUAL_A", "DIFERENTE", "MAIOR", "MENOR"]
        )

    def processar_atribuicao(self):
        if(
            self.token_atual is not None and
            self.token_atual.tipo == "IDENTIFICADOR" and
            self.indice + 1 < len(self.tokens) and
            self.tokens[self.indice + 1].tipo == "ATRIBUICAO"
        ):
            nome = self.token_atual.valor

            self.avancar()
            self.avancar()

            valor = self.processar_logicos()

            return AtribuicaoNode(nome, valor)

        return self.processar_logicos()


    def processar_if(self):

        if self.token_atual is not None and self.token_atual.tipo == "IF":
            self.avancar()

            condicao = self.processar_logicos()

            if self.token_atual is None or self.token_atual.tipo != "THEN":
                raise Exception("Erro de Sintaxe: Esperado 'then'")

            self.avancar()

            caso_verdadeiro = self.processar_atribuicao()

            if self.token_atual is None or self.token_atual.tipo != "ELSE":
                raise Exception("Erro de Sintaxe: esperado 'else'")

            self.avancar()

            caso_falso = self.processar_atribuicao()

            return IfNode(condicao, caso_verdadeiro, caso_falso)

        return self.processar_atribuicao()


    def processar_logicos(self):
        return self.processar_operacao(
            self.processar_comparacao,
            ["AND", "OR"]
        )

