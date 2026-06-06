from Core.Lexer import Lexer
from Core.Parser import Parser
from Core.Interpreter import Interpreter

interpreter = Interpreter()

texto = "func dobro(x) x * 2"

lexer = Lexer(texto)
tokens = lexer.gerar_tokens()

parser = Parser(tokens)
arvore = parser.processar_funcao()

interpreter.visitar(arvore)

texto = "dobro(10)"

lexer = Lexer(texto)
tokens = lexer.gerar_tokens()

parser = Parser(tokens)
arvore = parser.processar_funcao()

resultado = interpreter.visitar(arvore)

print("Resultado:", resultado)