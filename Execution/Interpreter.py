# O Interpretador (Interpreter) é o Back-end em modo execução direta.
# Ele caminha pela Árvore (AST) e executa o código "ao vivo", sem precisar transformar em Assembly primeiro.
class Interpreter:
    def __init__(self):
        # Memória das variáveis: Guarda o nome da variável, o valor e o tipo.
        self.tabela_simbolos = {}
        # Memória das funções: Guarda as funções que o usuário criou para poder chamá-las depois.
        self.funcoes = {}

    # Função auxiliar para descobrir o tipo do dado que está sendo processado.
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

    # Método principal e recursivo do Interpretador. Visita e executa um Nó e seus filhos.
    def visitar(self, node):
        tipo_node = type(node).__name__

        # Se for a raiz do programa, executa cada comando e devolve o último resultado
        if tipo_node == "ProgramaNode":
            resultado = None
            for cmd in node.comandos:
                resultado = self.visitar(cmd)
            return resultado

        # Quando tenta ler uma Variável...
        if tipo_node == "VariavelNode":
            # Primeiro checa se ela já foi criada antes
            if node.nome not in self.tabela_simbolos:
                raise Exception(
                    f"Erro Semântico: variável '{node.nome}' não declarada"
                )
            # Retorna o valor guardado
            return self.tabela_simbolos[node.nome]["valor"]

        # Se for um Número, apenas devolve ele próprio
        if tipo_node == "NumeroNode":
            return node.token.valor

        # Se for um Booleano (true/false)
        if tipo_node == "BoleanoNode":
            return node.nome

        # Se for Texto (String)
        if tipo_node == "StringNode":
            return node.valor

        # Se for um comando Return (sai da função com o valor)
        if tipo_node == "ReturnNode":
            return self.visitar(node.valor)

        # Se for Atribuição (ex: x = 10)
        if tipo_node == "AtribuicaoNode":
            # Descobre o valor que vai ser guardado (pode ser uma conta gigante)
            valor = self.visitar(node.valor)
            # Salva na memória global
            self.tabela_simbolos[node.nome] = {
                "valor": valor,
                "tipo": self.obter_tipo(valor),
                "escopo": "global"
            }
            return valor

        # Estrutura de Decisão (IF)
        if tipo_node == "IfNode":
            # Executa a condição primeiro (espera-se que dê true ou false)
            condicao = self.visitar(node.condicao)

            # Se for true, roda o bloco verdadeiro
            if condicao:
                return self.visitar(node.caso_verdadeiro)

            # Se for false, roda o bloco falso (else)
            return self.visitar(node.caso_falso)

        # Imprimir na tela (Print)
        if tipo_node == "PrintNode":
            valor = self.visitar(node.valor)
            print(valor) # Usa a função print real do Python
            return valor

        # Ler do teclado (Read)
        if tipo_node == "ReadNode":
            # Pede pro usuário digitar algo no console
            valor = input(f"Digite o valor de {node.nome}: ")

            # Tenta converter para número inteiro se for digitado só números
            if valor.isdigit():
                valor = int(valor)

            # Salva a entrada do usuário na variável
            self.tabela_simbolos[node.nome] = {
                "valor": valor,
                "tipo": self.obter_tipo(valor),
                "escopo": "global"
            }
            return valor

        # Estrutura de Repetição (While)
        if tipo_node == "WhileNode":
            resultado = None

            # Fica rodando enquanto a condição for verdadeira
            while self.visitar(node.condicao):
                resultado = self.visitar(node.corpo)

            return resultado

        # Definição de nova função pelo usuário
        if tipo_node == "FuncaoNode":
            # Valida se a função criada possui um 'return' no final
            if type(node.corpo).__name__ != "ReturnNode":
                raise Exception(
                    f"Erro Semântico: função '{node.nome}' deve possuir return"
                )

            # Guarda o nó inteiro da função no dicionário de funções
            self.funcoes[node.nome] = node
            return None

        # Chamando uma função que já foi criada (ex: calcula_dobro(10))
        if tipo_node == "ChamarFuncaoNode":
            # Verifica se ela existe
            if node.nome not in self.funcoes:
                raise Exception(
                    f"Erro Semântico: função '{node.nome}' não declarada"
                )

            # Puxa a função da memória
            funcao = self.funcoes[node.nome]

            # Calcula o valor do que foi enviado entre parênteses (ex: o '10')
            valor_argumento = self.visitar(node.argumento)

            # Tira um "Xerox" da memória atual (para que as variáveis de dentro 
            # da função não baguncem as variáveis globais que estão lá fora)
            tabela_antiga = self.tabela_simbolos.copy()

            # Cria a variável local (parâmetro) da função injetando o valor recebido
            self.tabela_simbolos[funcao.parametro] = {
                "valor": valor_argumento,
                "tipo": self.obter_tipo(valor_argumento),
                "escopo": "local"
            }

            # Agora sim, roda a função!
            resultado = self.visitar(funcao.corpo)

            # Restaura a memória de volta pro estado original (apagando as variáveis locais)
            self.tabela_simbolos = tabela_antiga

            # Devolve a resposta final
            return resultado

        # Operações com apenas um valor
        if tipo_node == "OperacaoUnariaNode":
            numero = self.visitar(node.node)
            if node.operador.tipo == "SOMA":
                return +numero
            if node.operador.tipo == "SUBTRACAO":
                return -numero
            if node.operador.tipo == "NOT":
                return not numero

        # Contas e Comparações normais
        if tipo_node == "OperacaoBinariaNode":
            # Resolve a conta do lado esquerdo e do direito primeiro
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

    # Validador para impedir que alguém tente somar Texto com Número, por exemplo.
    def verificar_tipo(self,esquerda,direita):
        if type(esquerda) != type(direita):
            # Permite aritmética mista entre int e float (excluindo booleanos)
            if (isinstance(esquerda, (int, float)) and not isinstance(esquerda, bool) and
                isinstance(direita, (int, float)) and not isinstance(direita, bool)):
                return
            raise Exception(
                f"Erro semântico: tipos incompátiveis ({type(esquerda).__name__} e {type(direita).__name__})"
            )