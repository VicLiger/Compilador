import string
from Core.Token import Token

# Definindo o que é um número e o que é uma letra
numeros = "0123456789"
letras = string.ascii_letters + "_"
letras_numeros = letras + numeros

# O Lexer (Analisador Léxico) é a primeira etapa do compilador.
# Sua função é ler o texto do código caractere por caractere e transformá-lo
# em uma lista de "Tokens" (pequenos blocos de significado, como "SOMA", "INTEIRO", etc.).
class Lexer:
    def __init__(self, texto):
        self.texto = texto
        self.posicao = -1
        self.caractere_atual = None
        self.avancar()

    # Move para o próximo caractere no texto.
    def avancar(self):
        self.posicao += 1

        if self.posicao < len(self.texto):
            self.caractere_atual = self.texto[self.posicao]
        else:
            self.caractere_atual = None

    # Função principal que varre o texto todo gerando e colecionando Tokens.
    def gerar_tokens(self):
        tokens = []

        while self.caractere_atual is not None:

            # Ignora espaços em branco e quebras de linha (Enter)
            if self.caractere_atual in " \t\n\r":
                self.avancar()

            # Se achar aspas, começa a gerar um texto (String)
            elif self.caractere_atual == '"':
                tokens.append(self.gerar_string())

            # Se for um número, gera um Token Numérico
            elif self.caractere_atual in numeros:
                tokens.append(self.gerar_token_numerico())
                
            # Se for letra, pode ser o nome de uma variável, ou palavras como 'if', 'while'
            elif self.caractere_atual in letras:
                tokens.append(self.gerar_identificador())

            ### OPERADORES MATEMÁTICOS ###
            elif self.caractere_atual == "+":
                tokens.append(Token("SOMA", "+"))
                self.avancar()
            elif self.caractere_atual == "-":
                tokens.append(Token("SUBTRACAO", "-"))
                self.avancar()
            elif self.caractere_atual == "*":
                tokens.append(Token("MULTIPLICACAO", "*"))
                self.avancar()
            elif self.caractere_atual == "/":
                tokens.append(Token("DIVISAO", "/"))
                self.avancar()
            elif self.caractere_atual == "(":
                tokens.append(Token("PARENTESES_ESQUERDA", "("))
                self.avancar()
            elif self.caractere_atual == ")":
                tokens.append(Token("PARENTESES_DIREITA", ")"))
                self.avancar()
            
            ### OPERADORES LÓGICOS E ATRIBUIÇÃO ###
            elif self.caractere_atual == "=":
                self.avancar()
                # Verifica se é '=='
                if self.caractere_atual == "=":
                    tokens.append(Token("IGUAL_A", "=="))
                    self.avancar()
                # Se não for, é só atribuição '='
                else:
                    tokens.append(Token("ATRIBUICAO", "="))

            elif self.caractere_atual == "!":
                self.avancar()
                # Verifica se é '!='
                if self.caractere_atual == "=":
                    tokens.append(Token("DIFERENTE", "!="))
                    self.avancar()
                    
            elif self.caractere_atual == ">":
                tokens.append(Token("MAIOR", ">"))
                self.avancar()
                
            elif self.caractere_atual == "<":
                tokens.append(Token("MENOR", "<"))
                self.avancar()
                
            else:
                # Se o caractere não bater com nenhuma das regras, mostra erro
                print(f"O caractere '{self.caractere_atual}' é inválido")
                self.avancar()

        return tokens

    # Lê tudo até a próxima aspas e transforma num Token de TEXTO (STRING).
    def gerar_string(self):
        texto =""
        self.avancar() # Pula as primeiras aspas

        while self.caractere_atual is not None and self.caractere_atual != '"':
            texto += self.caractere_atual
            self.avancar()

        self.avancar() # Pula as aspas do fim
        return Token("STRING", texto)


    # Lê os números, e se encontrar um ponto '.' transforma num Token DECIMAL.
    def gerar_token_numerico(self):
        numero_texto = ''
        e_decimal = False

        while (self.caractere_atual is not None and
               (self.caractere_atual in numeros or self.caractere_atual == '.')):

            if self.caractere_atual == '.':
                e_decimal = True

            numero_texto += self.caractere_atual
            self.avancar()

        if e_decimal:
            return Token("DECIMAL", float(numero_texto))

        return Token("INTEIRO", int(numero_texto))

    # Identifica se é uma palavra chave reservada da linguagem ou se é uma variável que o usuário inventou.
    def gerar_identificador(self):
        id_texto = ''
        while self.caractere_atual is not None and self.caractere_atual in letras_numeros:
            id_texto += self.caractere_atual
            self.avancar()

        if id_texto == "true":
            return Token("BOOL", True)

        if id_texto == "false":
            return Token("BOOL", False)

        if id_texto == "if":
            return Token("IF", id_texto)

        if id_texto == "then":
            return Token("THEN", id_texto)

        if id_texto == "else":
            return Token("ELSE", id_texto)

        if id_texto == "and":
            return Token("AND", id_texto)

        if id_texto == "or":
            return Token("OR", id_texto)

        if id_texto == "not":
            return Token("NOT", id_texto)

        if id_texto == "while":
            return Token("WHILE", id_texto)

        if id_texto == "print":
            return Token("PRINT", id_texto)

        if id_texto == "read":
            return Token("READ", id_texto)

        if id_texto == "func":
            return Token("FUNC", id_texto)

        if id_texto == "return":
            return Token("RETURN", id_texto)

        # Se não é palavra reservada, então o usuário acabou de declarar o nome de uma variável!
        return Token("IDENTIFICADOR", id_texto)