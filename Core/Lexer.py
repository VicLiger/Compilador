from Core.Token import Token

numeros = "0123456789"

class Lexer:
    def __init__(self, texto):
        self.texto = texto
        self.posicao = -1
        self.caractere_atual = None

    def avancar(self):
        self.posicao += 1

        if self.posicao < len(self.texto):
            self.caractere_atual = self.texto[self.posicao]
        else:
            self.caractere_atual = None

    def gerar_tokens(self):
        tokens =[]

        while self.caractere_atual != None:
            if self.caractere_atual in "\t":
                continue

            elif self.caractere_atual in numeros:
                tokens.append(self.gerar_token_numerico())

             ### OPERADORES ###
            elif self.caractere_atual == "+":
                tokens.append(Token("SOMA", "+"))
            elif self.caractere_atual == "-":
                tokens.append(Token("SUBTRACAO", "-"))
            elif self.caractere_atual == "*":
                tokens.append(Token("MULTIPLICACAO", "*"))
            elif self.caractere_atual == "/":
                tokens.append(Token("DIVISAO", "/"))
            elif self.caractere_atual == "(":
                tokens.append(Token("PARENTESES_ESQUERDA", "("))
            elif self.caractere_atual == ")":
                tokens.append(Token("PARENTESES_DIREITA", ")"))


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





