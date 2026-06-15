from Core.Node import NumeroNode, OperacaoBinariaNode, OperacaoUnariaNode, BoleanoNode, IfNode, WhileNode, FuncaoNode, ChamarFuncaoNode
from Core.Token import Token

# O Simplificador é responsável por otimizar a Árvore Sintática Abstrata (AST).
# Ele faz o que chamamos de 'Constant Folding' (Dobramento de Constantes).
# Se ele encontrar contas matemáticas que já podem ser resolvidas antes do programa rodar 
# (ex: 10 + 5), ele resolve na hora e troca por um único número (15).
class Simplificador:

    def simplificar(self, node):
        if node is None:
            return None

        tipo_node = type(node).__name__

        # Se for a raiz do programa, simplifica todos os comandos
        if tipo_node == "ProgramaNode":
            node.comandos = [self.simplificar(cmd) for cmd in node.comandos if cmd is not None]
            return node

        # Se for uma operação matemática (ex: esquerda + direita)
        if tipo_node == "OperacaoBinariaNode":
            # Primeiro, tenta simplificar o lado esquerdo
            esquerda = self.simplificar(node.esquerda)
            # Depois, tenta simplificar o lado direito
            direita = self.simplificar(node.direita)

            # A mágica: se o lado esquerdo E o lado direito forem apenas números finais...
            if type(esquerda).__name__ == "NumeroNode" and type(direita).__name__ == "NumeroNode":
                valor_esquerda = esquerda.token.valor
                valor_direita = direita.token.valor
                resultado = None

                # Realiza a conta correspondente aqui mesmo no compilador e devolve um novo NúmeroNode!
                if node.operador.tipo == "SOMA":
                    resultado = valor_esquerda + valor_direita
                elif node.operador.tipo == "SUBTRACAO":
                    resultado = valor_esquerda - valor_direita
                elif node.operador.tipo == "MULTIPLICACAO":
                    resultado = valor_esquerda * valor_direita
                elif node.operador.tipo == "DIVISAO":
                    resultado = valor_esquerda / valor_direita

                if resultado is not None:
                    # Determina o tipo do token de forma dinâmica
                    tipo_token = "DECIMAL" if isinstance(resultado, float) else "INTEIRO"
                    return NumeroNode(Token(tipo_token, resultado))

            # Se não conseguiu resolver (ex: x + 5 não dá pra resolver agora), 
            # reconstrói o nó com os pedaços que conseguiu simplificar.
            return OperacaoBinariaNode(esquerda, node.operador, direita)

        # Operações unárias
        if tipo_node == "OperacaoUnariaNode":
            node.node = self.simplificar(node.node)
            if type(node.node).__name__ == "NumeroNode":
                valor = node.node.token.valor
                if node.operador.tipo == "SOMA":
                    tipo_token = "DECIMAL" if isinstance(valor, float) else "INTEIRO"
                    return NumeroNode(Token(tipo_token, +valor))
                if node.operador.tipo == "SUBTRACAO":
                    tipo_token = "DECIMAL" if isinstance(valor, float) else "INTEIRO"
                    return NumeroNode(Token(tipo_token, -valor))
            if type(node.node).__name__ == "BoleanoNode" and node.operador.tipo == "NOT":
                return BoleanoNode(not node.node.nome)
            return node

        # Se for uma atribuição (x = algo), simplifica o 'algo'
        if tipo_node == "AtribuicaoNode":
            node.valor = self.simplificar(node.valor)
            return node

        # Se for print, simplifica o que vai ser impresso
        if tipo_node == "PrintNode":
            node.valor = self.simplificar(node.valor)
            return node

        # Se for um return, simplifica o valor retornado
        if tipo_node == "ReturnNode":
            node.valor = self.simplificar(node.valor)
            return node

        # Condicionais
        if tipo_node == "IfNode":
            node.condicao = self.simplificar(node.condicao)
            node.caso_verdadeiro = self.simplificar(node.caso_verdadeiro)
            node.caso_falso = self.simplificar(node.caso_falso)
            return node

        # Laços
        if tipo_node == "WhileNode":
            node.condicao = self.simplificar(node.condicao)
            node.corpo = self.simplificar(node.corpo)
            return node

        # Definição de funções
        if tipo_node == "FuncaoNode":
            node.corpo = self.simplificar(node.corpo)
            return node

        # Chamadas de funções
        if tipo_node == "ChamarFuncaoNode":
            node.argumento = self.simplificar(node.argumento)
            return node

        # Qualquer outro tipo de nó (Variáveis, Booleanos primitivos) é repassado sem alteração.
        return node