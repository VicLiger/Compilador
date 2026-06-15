from Core.Node import NumeroNode, OperacaoBinariaNode, OperacaoUnariaNode, VariavelNode, AtribuicaoNode, \
    ChamarFuncaoNode
from Core.Node import BoleanoNode
from Core.Node import IfNode
from Core.Node import WhileNode
from Core.Node import StringNode
from Core.Node import PrintNode
from Core.Node import ReadNode
from Core.Node import FuncaoNode
from Core.Node import ReturnNode
from Core.Node import ProgramaNode

# O Parser (Analisador Sintático) é a segunda etapa do compilador.
# Sua função é pegar a lista de Tokens gerada pelo Lexer e construir uma Árvore (AST).
# Ele faz isso verificando se a ordem dos tokens respeita as regras da linguagem.
# Funciona descendo do menos prioritário para o mais prioritário.
class Parser:
    def __init__(self, tokens):
        # A lista de tokens fornecida pelo Lexer
        self.tokens = tokens
        self.indice = -1
        self.token_atual = None
        self.avancar()

    # Move para o próximo token da lista.
    def avancar(self):
        self.indice += 1
        if self.indice < len(self.tokens):
            self.token_atual = self.tokens[self.indice]
        else:
            self.token_atual = None

    # Nível de MAIOR prioridade: Variáveis, Números, Textos ou blocos entre Parênteses.
    def processar_fator(self):
        token = self.token_atual

        if token is None:
            raise Exception("Erro de Sintaxe: Fim de arquivo inesperado (esperado número, variável, string, booleano, operador unário ou '(')")

        if token.tipo == "IDENTIFICADOR":
            nome = token.valor
            self.avancar()

            # Se depois da variável vier um '(', significa que na verdade é uma chamada de função! (ex: soma(5))
            if self.token_atual is not None and self.token_atual.tipo == "PARENTESES_ESQUERDA":
                self.avancar()
                # Processa o argumento que está sendo passado para a função
                argumento = self.processar_logicos()

                # A chamada de função deve terminar com ')'
                if self.token_atual.tipo != "PARENTESES_DIREITA":
                    raise Exception("Esperado ')'")
                self.avancar()

                # Retorna um nó de Chamada de Função
                return ChamarFuncaoNode(nome, argumento)

            # Se não tinha '(', é só o uso normal de uma variável
            return VariavelNode(nome)

        # Trata números negativos (ex: -5) ou negações lógicas (ex: not true)
        if token.tipo in ["SOMA", "SUBTRACAO", "NOT"]:
            self.avancar()
            node = self.processar_fator()
            return OperacaoUnariaNode(token, node)

        # Se for um número, cria o Nó de Número
        if token.tipo in ["INTEIRO", "DECIMAL"]:
            self.avancar()
            return NumeroNode(token)

        # Se for Booleano, cria Nó Booleano
        if token.tipo == "BOOL":
            self.avancar()
            return BoleanoNode(token.valor)

        # Se for Texto, cria Nó de Texto
        if token.tipo == "STRING":
            self.avancar()
            return StringNode(token.valor)

        # Se for parênteses, ele entra no parênteses e recomeça a análise (volto do começo da prioridade)
        if token.tipo == "PARENTESES_ESQUERDA":
            self.avancar()
            resultado = self.processar_logicos()
            
            # Garante que o parênteses foi fechado
            if self.token_atual is not None and self.token_atual.tipo == "PARENTESES_DIREITA":
                self.avancar()
                return resultado
            raise Exception("Erro de Sintaxe: Esperado ')'")


    # Função genérica e mágica que monta as operações.
    # Ela recebe a regra do nível inferior ('funcao') e a lista de 'operadores' do nível atual.
    def processar_operacao(self, funcao, operadores):
        # Pega a parte da esquerda
        esquerda = funcao()

        # Enquanto achar o operador que estamos procurando...
        while self.token_atual is not None and self.token_atual.tipo in operadores:
            operador = self.token_atual
            self.avancar()
            # Pega a parte da direita
            direita = funcao()
            
            # Monta o galho da árvore unindo esquerda + direita
            esquerda = OperacaoBinariaNode(esquerda, operador, direita)

        return esquerda

    # Prioridade 2: Multiplicação e Divisão (ocorre ANTES da soma).
    def processar_multiplicacao_divisao(self):
        return self.processar_operacao(
            self.processar_fator, # Chama a prioridade de baixo
            ["MULTIPLICACAO", "DIVISAO"]
        )

    # Prioridade 3: Soma e Subtração.
    def processar_expressao(self):
        return self.processar_operacao(
            self.processar_multiplicacao_divisao, # Chama a prioridade de baixo (Mult/Div)
            ["SOMA", "SUBTRACAO"]
        )

    # Prioridade 4: Comparações lógicas (==, !=, >, <).
    def processar_comparacao(self):
        return self.processar_operacao(
            self.processar_expressao, # Chama a prioridade de baixo (Soma/Sub)
            ["IGUAL_A", "DIFERENTE", "MAIOR", "MENOR"]
        )

    # Prioridade 5: Operadores AND / OR.
    def processar_logicos(self):
        return self.processar_operacao(
            self.processar_comparacao,
            ["AND", "OR"]
        )

    # Prioridade 6: Verifica se há atribuição de valor (x = 10).
    def processar_atribuicao(self):
        # Checa se o token atual é uma variável e se o PRÓXIMO é '='
        if(
            self.token_atual is not None and
            self.token_atual.tipo == "IDENTIFICADOR" and
            self.indice + 1 < len(self.tokens) and
            self.tokens[self.indice + 1].tipo == "ATRIBUICAO"
        ):
            nome = self.token_atual.valor
            self.avancar() # Passa a variável
            self.avancar() # Passa o '='

            # Processa o que tem do lado direito do '='
            valor = self.processar_logicos()

            return AtribuicaoNode(nome, valor)

        # Se não for atribuição, apenas repassa para o nível de baixo
        return self.processar_logicos()


    # Prioridade 7: Estrutura condicional If.
    def processar_if(self):
        if self.token_atual is not None and self.token_atual.tipo == "IF":
            self.avancar()

            condicao = self.processar_logicos() # Lê a condição

            # Garante que tem um 'then' (obrigatório na sintaxe desta linguagem)
            if self.token_atual is None or self.token_atual.tipo != "THEN":
                raise Exception("Erro de Sintaxe: Esperado 'then'")
            self.avancar()

            caso_verdadeiro = self.processar_return() # Lê o que roda no caso do if ser true

            # Garante que tem o 'else' (aqui o else também é obrigatório)
            if self.token_atual is None or self.token_atual.tipo != "ELSE":
                raise Exception("Erro de Sintaxe: esperado 'else'")
            self.avancar()

            caso_falso = self.processar_return() # Lê o que roda no else

            return IfNode(condicao, caso_verdadeiro, caso_falso)

        return self.processar_atribuicao()


    # Prioridade 8: Laço de repetição While.
    def processar_while(self):
        if self.token_atual is not None and self.token_atual.tipo == "WHILE":
            self.avancar()

            condicao = self.processar_logicos()

            # Garante que tem 'then'
            if self.token_atual is None or self.token_atual.tipo != "THEN":
                raise Exception("Erro de Sintaxe: Esperado 'then'")
            self.avancar()

            corpo = self.processar_return() # Corpo do laço

            return WhileNode(condicao, corpo)

        return self.processar_if()

    # Prioridade 9: Comando Print.
    def processar_print(self):
        if self.token_atual is not None and self.token_atual.tipo == "PRINT":
            self.avancar()
            valor = self.processar_logicos() # O que deve ser impresso
            return PrintNode(valor)

        return self.processar_while()

    # Prioridade 10: Comando Read (ler input).
    def processar_read(self):
        if self.token_atual is not None and self.token_atual.tipo == "READ":
            self.avancar()

            # Obriga que logo após o READ venha uma variável para guardar o dado
            if self.token_atual is None or self.token_atual.tipo != "IDENTIFICADOR":
                raise Exception("Erro de Sintaxe: Tem que ter o nome da variável após o read")

            nome = self.token_atual.valor
            self.avancar()

            return ReadNode(nome)

        return self.processar_print()


    # Prioridade 11: Comando Return (só usado dentro de funções).
    def processar_return(self):
        if self.token_atual is not None and self.token_atual.tipo == "RETURN":
            self.avancar()
            valor = self.processar_logicos() # O valor a retornar
            return ReturnNode(valor)

        return self.processar_read()

    # NÍVEL MAIS BAIXO (Ponto de Entrada das declarações normais).
    # Prioridade 12: Criação de função do usuário.
    def processar_funcao(self):
        if self.token_atual is not None and self.token_atual.tipo == "FUNC":
            self.avancar()

            # Valida e extrai o nome da função
            if self.token_atual.tipo != "IDENTIFICADOR":
                raise Exception("Esperado nome da função")
            nome = self.token_atual.valor
            self.avancar()

            # Valida o abrir de parênteses '('
            if self.token_atual.tipo != "PARENTESES_ESQUERDA":
                raise Exception("Esperado '('")
            self.avancar()

            # Valida e extrai o nome do parâmetro
            if self.token_atual.tipo != "IDENTIFICADOR":
                raise Exception("Esperado parâmetro")
            parametro = self.token_atual.valor
            self.avancar()

            # Valida o fechar de parênteses ')'
            if self.token_atual.tipo != "PARENTESES_DIREITA":
                raise Exception("Esperado ')'")
            self.avancar()

            # Processa o corpo da função (que nesta linguagem se limita a ser um return)
            corpo = self.processar_return()

            return FuncaoNode(nome, parametro, corpo)

        # Se o texto não começar definindo uma função, desce para tentar ler os comandos normais
        return self.processar_return()

    # O VERDADEIRO PONTO DE ENTRADA DO PARSER
    # Capaz de ler várias linhas de código.
    def processar_programa(self):
        comandos = []
        while self.token_atual is not None:
            token_anterior = self.token_atual
            
            comando = self.processar_funcao()
            if comando is not None:
                comandos.append(comando)
            
            # Trava de segurança para evitar loop infinito caso não entenda o token
            if self.token_atual == token_anterior:
                raise Exception(f"Erro de Sintaxe: O parser travou no token {self.token_atual}")
                
        return ProgramaNode(comandos)