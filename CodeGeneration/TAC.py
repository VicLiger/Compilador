# TAC significa 'Three-Address Code' (Código de Três Endereços).
# Esta classe traduz a nossa Árvore (AST) para uma linguagem linear, 
# bem mais próxima de como o processador ou uma linguagem de montagem (Assembly) funciona.
class TAC:
    def __init__(self):
        # Lista onde vamos guardar cada linha de instrução gerada
        self.codigo = []
        # Contador para criar variáveis temporárias únicas (t1, t2, t3...)
        self.contador_temp = 0
        # Contador para criar rótulos (labels) de pulo únicos
        self.contador_label = 0

    # Gera e retorna o nome de um novo rótulo único (ex: L1).
    def novo_label(self):
        self.contador_label += 1
        return f"L{self.contador_label}"

    # Gera e retorna o nome de uma nova variável temporária (ex: t1).
    def novo_temp(self):
        self.contador_temp += 1
        return f"t{self.contador_temp}"

    # Método recursivo que varre a árvore e gera o código correspondente.
    def gerar(self, node):
        tipo_node = type(node).__name__

        # Se for a raiz do programa, gera o código para cada comando sequencialmente
        if tipo_node == "ProgramaNode":
            for cmd in node.comandos:
                self.gerar(cmd)
            return None

        # Tipos primitivos apenas retornam seus valores como texto
        if tipo_node == "NumeroNode":
            return str(node.token.valor)

        if tipo_node == "BoleanoNode":
            return str(node.nome)

        if tipo_node == "StringNode":
            return f'"{node.valor}"'

        if tipo_node == "VariavelNode":
            return node.nome

        # Atribuição (ex: x = 10)
        if tipo_node == "AtribuicaoNode":
            valor = self.gerar(node.valor) # Descobre qual é o valor
            self.codigo.append(f"{node.nome} = {valor}") # Escreve a instrução
            return node.nome

        # Operações Matemáticas/Lógicas
        if tipo_node == "OperacaoBinariaNode":
            esquerda = self.gerar(node.esquerda)
            direita = self.gerar(node.direita)

            temp = self.novo_temp() # Pede uma variável temporária nova (ex: t1)

            # Cria a instrução: t1 = esquerda + direita
            self.codigo.append(
                f"{temp} = {esquerda} {node.operador.valor} {direita}"
            )

            return temp # Retorna a variável temporária para as próximas contas usarem

        # Operações com um único valor (ex: -5 ou not true)
        if tipo_node == "OperacaoUnariaNode":
            valor = self.gerar(node.node)

            temp = self.novo_temp()

            self.codigo.append(
                f"{temp} = {node.operador.valor}{valor}"
            )

            return temp

        # Comando Print
        if tipo_node == "PrintNode":
            valor = self.gerar(node.valor)
            self.codigo.append(f"print {valor}")
            return valor

        # Comando Return
        if tipo_node == "ReturnNode":
            valor = self.gerar(node.valor)
            self.codigo.append(f"return {valor}")
            return valor

        # Estrutura If / Else
        if tipo_node == "IfNode":
            condicao = self.gerar(node.condicao)

            # Cria "Rótulos" (Labels) únicos para onde o código deve pular
            label_else = self.novo_label()
            label_fim = self.novo_label()

            # Se a condição for falsa, pula para o Lado Else
            self.codigo.append(f"ifFalse {condicao} goto {label_else}")

            # Gera o bloco verdadeiro
            self.gerar(node.caso_verdadeiro)
            # Pula para o fim (para não executar o else)
            self.codigo.append(f"goto {label_fim}")

            # Define o ponto do Else
            self.codigo.append(f"{label_else}:")
            # Gera o bloco falso
            self.gerar(node.caso_falso)

            # Define o ponto do Fim
            self.codigo.append(f"{label_fim}:")
            return None

        # Estrutura While
        if tipo_node == "WhileNode":
            label_inicio = self.novo_label()
            label_fim = self.novo_label()

            # Marca onde o laço começa
            self.codigo.append(f"{label_inicio}:")

            condicao = self.gerar(node.condicao)

            # Se for falsa, pula lá pro final
            self.codigo.append(f"ifFalse {condicao} goto {label_fim}")

            # Gera o bloco do que fazer dentro do laço
            self.gerar(node.corpo)

            # Volte para checar a condição de novo
            self.codigo.append(f"goto {label_inicio}")
            # Marca o final
            self.codigo.append(f"{label_fim}:")

            return None

        # Definição de Função
        if tipo_node == "FuncaoNode":
            self.codigo.append(f"func {node.nome}({node.parametro})")
            self.gerar(node.corpo)
            self.codigo.append("endfunc")
            return None

        # Chamada de Função
        if tipo_node == "ChamarFuncaoNode":
            arg = self.gerar(node.argumento)
            temp = self.novo_temp()
            self.codigo.append(f"{temp} = call {node.nome}, {arg}")
            return temp

    # Junta toda a lista de comandos em uma única string com quebras de linha.
    def obter_codigo(self):
        return "\n".join(self.codigo)