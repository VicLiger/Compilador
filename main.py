from Analysis.Lexer import Lexer
from Analysis.Parser import Parser
from CodeGeneration.TAC import TAC
from CodeGeneration.Simplificador import Simplificador

texto = "x = 10 + 20 * 3"

lexer = Lexer(texto)
tokens = lexer.gerar_tokens()

parser = Parser(tokens)
arvore = parser.processar_funcao()

simplificador = Simplificador()
arvore_simplificada = simplificador.simplificar(arvore)

tac = TAC()
tac.gerar(arvore_simplificada)

print("Tokens:", tokens)
print("TAC otimizado:")
print(tac.obter_codigo())