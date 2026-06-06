import string
from Core.Token import Token

numeros = "0123456789"
letras = string.ascii_letters
letras_numeros = letras + numeros

class Lexer:
    def __init__(self, texto):
        self.texto = texto
        self.posicao = -1
        self.caractere_atual = None
        self.avancar()

    def avancar(self):
        self.posicao += 1

        if self.posicao < len(self.texto):
            self.caractere_atual = self.texto[self.posicao]
        else:
            self.caractere_atual = None

    def gerar_tokens(self):
        tokens = []

        while self.caractere_atual is not None:

            if self.caractere_atual in " \t":
                self.avancar()

            elif self.caractere_atual in numeros:
                tokens.append(self.gerar_token_numerico())
                
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
                if self.caractere_atual == "=":
                    tokens.append(Token("IGUAL_A", "=="))
                    self.avancar()
                else:
                    tokens.append(Token("ATRIBUICAO", "="))

            elif self.caractere_atual == "!":
                self.avancar()
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
                print(f"O caractere '{self.caractere_atual}' é inválido")
                self.avancar()

        return tokens

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
        
        return Token("IDENTIFICADOR", id_texto)