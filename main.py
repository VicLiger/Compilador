from Core.Lexer import Lexer
from Core.Parser import Parser
from Core.Interpreter import Interpreter

interpreter = Interpreter()

texto = "print x"

lexer = Lexer(texto)
tokens = lexer.gerar_tokens()

parser = Parser(tokens)
arvore = parser.processar_funcao()

resultado = interpreter.visitar(arvore)

print("Resultado:", resultado)