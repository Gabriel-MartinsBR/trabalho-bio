# Parte 1: Homicídios, juventude e raça/cor
# Gabriel Martins, Hadassah Teodoro e Ruanytha Miranda - Turma 101
# Enunciado n: 2 | Download original: 23/09/2026
# Uso de IA: Claude e ChatGPT/Codex, declarado na versão de entrega.
# Resultados comentados: cópia original, não um novo download.

import pandas as pd
import hashlib
from pathlib import Path

pasta_projeto = Path(__file__).resolve().parent.parent
pasta_dados = pasta_projeto / "dados"
# Nesse momento, pego a pasta do projeto a partir do próprio arquivo.
# Fiz assim porque o CSV está dentro de dados, e não dentro de python.
# Com isso, o caminho funciona mesmo se eu abrir o terminal em outra pasta.

dados = pd.read_csv(
    pasta_dados / "DOAL2025.csv",
    dtype="string",
    encoding="utf-8-sig"
)

# ==========================================================
# (b) Conferência do tamanho da base
# ==========================================================

n_obs, n_vars = dados.shape
print(f"Observações (óbitos): {n_obs}")
print(f"Variáveis: {n_vars}")

# Esperado pelo enunciado: ~23.000 óbitos para AL em 2025.
# Obtido: 22.936 óbitos, 87 variáveis.
# A diferença é de 64 óbitos, aproximadamente 0,3%.
# Com isso, a quantidade está dentro do esperado para uma base preliminar.

diferenca = abs(n_obs - 23000) / 23000 * 100
print(f"Diferença em relação ao esperado: {diferenca:.3f}%")

if diferenca > 10:
    raise ValueError(
        "A base ficou muito longe de 23 mil. Conferir o arquivo antes de continuar."
    )
    # Essa trava impede que eu continue trabalhando com outro recorte
    # sem perceber. Se isso acontecer, preciso verificar o download.

assinatura = hashlib.sha256(
    (pasta_dados / "DOAL2025.csv").read_bytes()
).hexdigest()

assinatura_original = "ba754138484a991871d19564b9eaedff73d15bfe6f55648af9a570e331c123af"
print("É a mesma cópia de 23/09/2026?", assinatura == assinatura_original)
# Essa assinatura serve para conferir se o arquivo é exatamente o mesmo.
# Resultado: True. Os comentários numéricos correspondem a essa cópia.

if assinatura != assinatura_original:
    print(
        "Atenção: a base mudou. Conferir os novos resultados e atualizar os comentários."
    )
