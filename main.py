from Core.Lexer import Lexer
from Core.Parser import Parser
from Core.Interpreter import Interpreter

interpreter = Interpreter()

texto = "x = 10"

lexer = Lexer(texto)
tokens = lexer.gerar_tokens()

parser = Parser(tokens)
arvore = parser.processar_funcao()

resultado = interpreter.visitar(arvore)

print("Resultado:", resultado)

print("Tabela de Símbolos:", interpreter.tabela_simbolos)