# Parte 1: Homicídios, juventude e raça/cor
# Gabriel Martins, Hadassah Teodoro e Ruanytha Miranda - Turma 101
# Enunciado n: 2 | Download original: 23/09/2026
# Uso de IA: Claude e ChatGPT/Codex, declarado na versão de entrega.
# Resultados comentados: cópia original, não um novo download.

from pathlib import Path

pasta_projeto = Path(__file__).resolve().parent.parent
pasta_dados = pasta_projeto / "dados"
# Nesse momento, pego a pasta do projeto a partir do próprio arquivo.
# Fiz assim porque o CSV está dentro de dados, e não dentro de python.
# Com isso, o caminho funciona mesmo se eu abrir o terminal em outra pasta.

# ==========================================================
# (f) O que essa base não permite responder
# ==========================================================

# Depois de conferir os dados, deixei registradas as limitações.
# Essa parte não faz outro cálculo; é para mostrar o que eu consigo
# e o que eu não consigo afirmar a partir da base que utilizei.

# (f) Limitações da base (oito linhas).
# 1. O SIM registra óbitos: sem população viva, não calculamos risco ou taxa de homicídio.
# 2. A proporção de homicídios entre óbitos não mede o risco de morrer da população.
# 3. Dados preliminares de 2025 podem mudar após atualização e investigação dos óbitos.
# 4. Sub-registro e causas mal definidas ou de intenção indeterminada podem ocultar homicídios.
# 5. Raça/cor e escolaridade ausentes podem selecionar o subconjunto com dados completos.
# 6. A declaração de óbito não identifica motivação, autor, contexto social ou renda individual.
# 7. O agrupamento preta+parda reduz detalhes e usa raça/cor registrada, não comprovadamente autodeclarada.
# 8. Esta descrição de óbitos não demonstra causalidade nem se generaliza a outras UFs ou anos.

# ==========================================================
# Diário de erros
# ==========================================================

# DIÁRIO DE ERROS REAIS, reproduzidos durante a revisão em 04/10/2026:
# 1. No script 05_tratamento_variaveis.py, rodando da raiz do projeto:
# FileNotFoundError: [Errno 2] No such file or directory: 'DOAL2025.csv'.
# Causa: o CSV estava em dados/, mas CAMINHO apontava à raiz. Solução:
# localizar com Path(__file__) e dados/DOAL2025.csv e não o nome do CSV sozinho.
# 2. No script teste.py: NameError: name 'IDADE' is not defined.
# Causa: IDADE é uma coluna do DataFrame, não uma variável avulsa. Solução:
# usar dados['IDADE'] e conferir dados['IDADE'].dtype ou dados.dtypes.
# Correção adicional de conteúdo: o dicionário antigo associava 1 a minutos,
# 2 a horas e omitira dias; corrigi para 0 minutos, 1 horas, 2 dias, 3 meses.
# Nenhum teste, valor-p, correlação ou comparação inferencial foi executado.

print(
    "Parte 1 concluída. As limitações e o diário de erros estão nos comentários deste arquivo."
)
