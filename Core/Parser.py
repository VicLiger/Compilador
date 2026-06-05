class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.indice = -1
        self.token_atual = None
        self.avancar()

    def avancar(self):
        self.indice += 1

        if self.indice == len(self.tokens):
            self.token_atual = self.tokens[self.indice]

        return self.token_atual