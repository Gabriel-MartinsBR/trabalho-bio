import pandas as pd

dados = pd.read_csv("dados/DOAL2025.csv", encoding="utf-8-sig")

# ==========================================================
# (b) Conferência do tamanho da base
# ==========================================================
n_obs, n_vars = dados.shape
print(f"Observações (óbitos): {n_obs}")
print(f"Variáveis: {n_vars}")

# Esperado pelo enunciado: ~23.000 óbitos para AL em 2025 (dado preliminar)
# Obtido: 22.936 óbitos, 87 variáveis
# Diferença: 22.936 vs ~23.000 esperado -> diferença de ~0,3%, dentro do
# esperado pelo aviso do enunciado