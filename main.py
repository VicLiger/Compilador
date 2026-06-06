from Core.Lexer import Lexer
from Core.Parser import Parser
from Core.Interpreter import Interpreter

texto = "x = 10"

lexer = Lexer(texto)
tokens = lexer.gerar_tokens()

parser = Parser(tokens)
arvore = parser.processar_atribuicao()

interpreter = Interpreter()
resultado = interpreter.visitar(arvore)

print("Tokens:", tokens)
print("Resultado:", resultado)
print("Variáveis:", interpreter.variaveis)