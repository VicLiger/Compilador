# O Bytecode é um tipo de geração de código para Máquinas de Pilha (Stack Machines), como a JVM do Java.
# Ele empilha (PUSH) valores e depois manda executar uma instrução que puxa eles de volta para fazer a conta.
class Bytecode:
    def __init__(self):
        # Onde guardamos a lista final de instruções Assembly geradas.
        self.codigo = []
        # Contador para criar rótulos (labels) de desvio únicos
        self.contador_label = 0

    # Gera e retorna o nome de um novo rótulo único (ex: L1).
    def novo_label(self):
        self.contador_label += 1
        return f"L{self.contador_label}"

    # Método que caminha na árvore gerando as instruções de pilha.
    def gerar(self, node):
        if node is None:
            return None

        tipo_node = type(node).__name__

        # Se for a raiz do programa, gera o código para cada comando sequencialmente
        if tipo_node == "ProgramaNode":
            for cmd in node.comandos:
                self.gerar(cmd)
            return None

        # PUSH empurra valores para o topo da pilha
        if tipo_node == "NumeroNode":
            self.codigo.append(f"PUSH {node.token.valor}")

        elif tipo_node == "BoleanoNode":
            self.codigo.append(f"PUSH {node.nome}")

        elif tipo_node == "StringNode":
            self.codigo.append(f'PUSH "{node.valor}"')

        # LOAD carrega o valor que está dentro de uma variável e joga na pilha
        elif tipo_node == "VariavelNode":
            self.codigo.append(f"LOAD {node.nome}")

        # STORE tira o valor do topo da pilha e salva dentro de uma variável
        elif tipo_node == "AtribuicaoNode":
            self.gerar(node.valor) # Calcula o valor que vai atribuir
            self.codigo.append(f"STORE {node.nome}")

        # Contas e Comparações: Empurra esquerda, Empurra direita, Faz operação.
        elif tipo_node == "OperacaoBinariaNode":
            self.gerar(node.esquerda)
            self.gerar(node.direita)

            if node.operador.tipo == "SOMA":
                self.codigo.append("ADD")
            elif node.operador.tipo == "SUBTRACAO":
                self.codigo.append("SUB")
            elif node.operador.tipo == "MULTIPLICACAO":
                self.codigo.append("MUL")
            elif node.operador.tipo == "DIVISAO":
                self.codigo.append("DIV")
            elif node.operador.tipo == "MAIOR":
                self.codigo.append("GT") # Greater Than
            elif node.operador.tipo == "MENOR":
                self.codigo.append("LT") # Less Than
            elif node.operador.tipo == "IGUAL_A":
                self.codigo.append("EQ") # Equal
            elif node.operador.tipo == "DIFERENTE":
                self.codigo.append("NEQ") # Not Equal
            elif node.operador.tipo == "AND":
                self.codigo.append("AND")
            elif node.operador.tipo == "OR":
                self.codigo.append("OR")

        # Inverte valores lógicos ou inverte o sinal do número
        elif tipo_node == "OperacaoUnariaNode":
            self.gerar(node.node)

            if node.operador.tipo == "SUBTRACAO":
                self.codigo.append("NEG") # Transforma em negativo
            elif node.operador.tipo == "NOT":
                self.codigo.append("NOT") # Inverte true/false

        elif tipo_node == "PrintNode":
            self.gerar(node.valor)
            self.codigo.append("PRINT")

        elif tipo_node == "ReadNode":
            self.codigo.append(f"READ {node.nome}")

        elif tipo_node == "ReturnNode":
            self.gerar(node.valor)
            self.codigo.append("RETURN")

        # Estrutura If / Else
        elif tipo_node == "IfNode":
            self.gerar(node.condicao)
            label_else = self.novo_label()
            label_fim = self.novo_label()
            self.codigo.append(f"JUMP_IF_FALSE {label_else}")
            self.gerar(node.caso_verdadeiro)
            self.codigo.append(f"JUMP {label_fim}")
            self.codigo.append(f"LABEL {label_else}")
            self.gerar(node.caso_falso)
            self.codigo.append(f"LABEL {label_fim}")

        # Estrutura While
        elif tipo_node == "WhileNode":
            label_inicio = self.novo_label()
            label_fim = self.novo_label()
            self.codigo.append(f"LABEL {label_inicio}")
            self.gerar(node.condicao)
            self.codigo.append(f"JUMP_IF_FALSE {label_fim}")
            self.gerar(node.corpo)
            self.codigo.append(f"JUMP {label_inicio}")
            self.codigo.append(f"LABEL {label_fim}")

        # Definição de Função
        elif tipo_node == "FuncaoNode":
            self.codigo.append(f"LABEL {node.nome}")
            self.codigo.append(f"STORE_LOCAL {node.parametro}")
            self.gerar(node.corpo)

        # Chamada de Função
        elif tipo_node == "ChamarFuncaoNode":
            self.gerar(node.argumento)
            self.codigo.append(f"CALL {node.nome}")

    # Retorna o conjunto de Assembly inteiro
    def obter_codigo(self):
        return "\n".join(self.codigo)