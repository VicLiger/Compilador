# Importa as peças essenciais para que o compilador funcione do começo ao fim
from Analysis.Lexer import Lexer
from Analysis.Parser import Parser
from Execution.Interpreter import Interpreter
from CodeGeneration.TAC import TAC
from CodeGeneration.Simplificador import Simplificador
from CodeGeneration.Bytecode import Bytecode

# 1. ESCRITA DO CÓDIGO
# Lê o código fonte a partir do arquivo 'code.txt'
with open("code.txt", "r", encoding="utf-8") as arquivo:
    texto = arquivo.read()

# 2. ANÁLISE LÉXICA
# Envia o texto para o Lexer. A missão dele é cortar o texto em "Tokens" com significado.
lexer = Lexer(texto)
tokens = lexer.gerar_tokens()

# 3. ANÁLISE SINTÁTICA
# Pega a lista de Tokens e manda pro Parser construir a Árvore (AST).
# Aqui é onde se decide a ordem das contas (prioridade do * antes do +).
parser = Parser(tokens)
arvore = parser.processar_programa()

# 4. ANÁLISE SEMÂNTICA / EXECUÇÃO
# O Interpreter percorre a árvore e verifica erros como variável não declarada,
# função não declarada, erro de tipo e também executa os comandos print/read.
interpreter = Interpreter()
interpreter.visitar(arvore)

# 5. OTIMIZAÇÃO DE CÓDIGO
# O Simplificador passa pela árvore procurando contas que ele pode resolver agora.
# O "10 + 20 * 3" que resulta numa árvore cheia, vira um único galho "70".
simplificador = Simplificador()
arvore_simplificada = simplificador.simplificar(arvore)

# 6. GERAÇÃO DE CÓDIGO INTERMEDIÁRIO (TAC)
# Finalmente, a árvore (já simplificada) é enviada para virar uma linguagem linear.
tac = TAC()
tac.gerar(arvore_simplificada)

# 7. GERAÇÃO DE BYTECODE
# A árvore simplificada também pode ser traduzida para instruções de baixo nível.
bytecode = Bytecode()
bytecode.gerar(arvore_simplificada)

# SAÍDA NA TELA (RESULTADO)
# Mostra os tokens lidos pelo Lexer
print("\nTokens:")
print(tokens)

# Mostra o código de 3 endereços otimizado final
print("\nTAC otimizado:")
print(tac.obter_codigo())

# Mostra o bytecode gerado pelo compilador
print("\nBytecode:")
print(bytecode.obter_codigo())