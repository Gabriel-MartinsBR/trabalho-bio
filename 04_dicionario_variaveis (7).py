import pandas as pd

dados = pd.read_csv("dados/DOAL2025.csv", encoding="utf-8-sig")

# ==========================================================
# (c) Inspeção das variáveis do enunciado (antes de tratar)
# ==========================================================

variaveis = ["CAUSABAS", "IDADE", "SEXO", "RACACOR", "ESC", "LOCOCOR", "CODMUNRES"]

# Tipo de dado que o pandas enxergou ao ler o CSV
print("Tipos de dados:")
print(dados[variaveis].dtypes)

# Distribuição de valores de cada variável (os mais frequentes)
for v in variaveis:
    print(f"\n--- {v} ---")
    print(f"Valores únicos: {dados[v].nunique()}")
    print(f"Faltantes (NaN): {dados[v].isna().sum()}")
    print(dados[v].value_counts(dropna=False).head(15))