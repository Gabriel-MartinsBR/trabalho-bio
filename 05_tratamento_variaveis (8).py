# ================================================================
# (d) TRATAMENTO DAS VARIÁVEIS — versão Python (pandas)
# Ritmo de cada passo: OLHAR -> DECIDIR -> TRATAR -> CONTAR
# Onde estiver <COLE AQUI>, cole o que o SEU console devolveu.
# ================================================================

import pandas as pd
import numpy as np

CAMINHO = "DOAL2025.csv"      # ajuste o caminho; se o CSV usar ";", acrescente sep=";"
COLUNAS = ["CAUSABAS", "IDADE", "SEXO", "RACACOR", "ESC", "LOCOCOR", "CODMUNRES"]

# ----------------------------------------------------------------
# PASSO 0 — Ler o arquivo TUDO COMO TEXTO
# O que faz: dtype=str impede o pandas de "adivinhar" os tipos.
# Por quê: se ele lê IDADE como número, o código "015" (15 minutos de
# vida) vira 15 e o 1º dígito deixa de ser a unidade. Só converto para
# número depois de olhar cada coluna.
# ----------------------------------------------------------------
print("Variáveis no arquivo bruto:", pd.read_csv(CAMINHO, nrows=0).shape[1])   # ncol do item (b)
dados = pd.read_csv(CAMINHO, usecols=COLUNAS, dtype=str)
print("Observações:", len(dados))
# <COLE AQUI: o total e se bate com "cerca de 23 mil">

# ----------------------------------------------------------------
# PASSO 1 — Conferir que são residentes em Alagoas
# O que faz: pega os 2 primeiros dígitos do código do município de
# residência (o código IBGE de AL começa com 27) e conta.
# Por quê: o enunciado pede óbitos de RESIDENTES. Se aparecer outro
# prefixo, esses registros saem — com número e motivo.
# ----------------------------------------------------------------
print(dados["CODMUNRES"].str[:2].value_counts(dropna=False))
# <COLE AQUI: só "27"? Se não, quantos de outros estados?>

# ----------------------------------------------------------------
# PASSO 2 — IDADE: do código de 3 dígitos para anos
# O que faz, em ordem:
#  (a) confere o tamanho do texto (deve ser 3) e completa zeros à
#      esquerda se algum se perdeu (zfill);
#  (b) separa o 1º dígito (unidade) do resto (quantidade);
#  (c) olha quais unidades existem ANTES de converter;
#  (d) converte: 4 = anos; 5 = 100 anos ou mais (503 = 103);
#      0/1/2/3 (minutos, horas, dias, meses) = menor de 1 ano.
# Por quê: mean() do código bruto mistura dias, meses e anos.
# ----------------------------------------------------------------
print(dados["IDADE"].str.len().value_counts(dropna=False))    # esperado: só 3
dados["IDADE"] = dados["IDADE"].str.zfill(3)                  # NaN continua NaN

unidade = dados["IDADE"].str[0]                               # 1º dígito
quantidade = pd.to_numeric(dados["IDADE"].str[1:3], errors="coerce")
print(unidade.value_counts(dropna=False).sort_index())        # esperado: 0 a 5
# <COLE AQUI: quais unidades apareceram e quantos de cada>

dados["idade_anos"] = np.select(
    [unidade.isin(["0", "1", "2", "3"]), unidade == "4", unidade == "5"],
    [0, quantidade, 100 + quantidade],
    default=np.nan)

# DECISÃO (reescreva com as suas palavras): menor de 1 ano vira 0 e NÃO
# NaN, porque a população de comparação é "todos os óbitos" e não quero
# perder esses registros. Alternativa rejeitada: NaN (o exemplo do
# guia faz isso, mas lá só interessam adultos).
print(dados["idade_anos"].describe())
# <COLE AQUI>

# ----------------------------------------------------------------
# PASSO 3 — SEXO, RACACOR, ESC, LOCOCOR: olhar e tirar os "ignorados"
# O que faz: converte cada coluna para número e mostra a contagem
# COM os faltantes (dropna=False). Depois troca os códigos por rótulos.
# Por quê: "ignorado" não é categoria, é dado que falta -> NaN. Com
# .map(dicionário), tudo que não está no dicionário (0, 9, em branco)
# vira NaN sozinho.
# ----------------------------------------------------------------
for col in ["SEXO", "RACACOR", "ESC", "LOCOCOR"]:
    dados[col] = pd.to_numeric(dados[col], errors="coerce")
    print(f"--- {col} ---")
    print(dados[col].value_counts(dropna=False).sort_index())
# <COLE AQUI: quantos 0, quantos 9, quantos NaN em cada uma>

dados["sexo"] = dados["SEXO"].map({1: "Masculino", 2: "Feminino"})
dados["raca"] = dados["RACACOR"].map(
    {1: "Branca", 2: "Preta", 3: "Amarela", 4: "Parda", 5: "Indígena"})
dados["ESC"] = dados["ESC"].replace(9, np.nan)          # 9 = ignorado
dados["LOCOCOR"] = dados["LOCOCOR"].replace(9, np.nan)  # 9 = ignorado

# ----------------------------------------------------------------
# PASSO 4 — Raça/cor: negra (preta + parda) × branca
# O que faz: cria o grupo; amarela, indígena e ignorada ficam NaN
# NESTA variável (continuam existindo em "raca").
# Por quê: o enunciado pede a comparação negra × branca. JUSTIFICATIVA
# (complete): agrupamento do IBGE, previsto no Estatuto da Igualdade
# Racial (Lei 12.288/2010): população negra = preta + parda.
# ----------------------------------------------------------------
dados["raca_grupo"] = dados["RACACOR"].map({1: "Branca", 2: "Negra", 4: "Negra"})
print(dados["raca_grupo"].value_counts(dropna=False))
# DECISÃO: amarela e indígena ficam fora SÓ desta comparação (não
# apaguei da base). Alternativa rejeitada: <complete>
# <COLE AQUI: quantos ficaram de fora e por quê>

# ----------------------------------------------------------------
# PASSO 5 — Homicídio (X85–Y09) e meio empregado
# O que faz: usa uma expressão regular no início do CID para marcar
# homicídio (True/False) e classifica o meio pelos 3 primeiros caracteres.
# Por quê: os códigos têm 4 caracteres (ex.: X954), então
# CAUSABAS == "X93" não acharia nada. "Outros" = homicídios que não são
# X93–X95 nem X99. Quem não é homicídio fica com meio = NaN.
# ----------------------------------------------------------------
dados["cid3"] = dados["CAUSABAS"].str[:3]
dados["homicidio"] = dados["CAUSABAS"].str.match(r"^(X8[5-9]|X9[0-9]|Y0[0-9])", na=False)

dados["meio"] = np.where(dados["cid3"].isin(["X93", "X94", "X95"]), "Arma de fogo",
                np.where(dados["cid3"] == "X99", "Objeto cortante", "Outros"))
dados.loc[~dados["homicidio"], "meio"] = np.nan

print(dados["meio"].value_counts(dropna=False))
# <COLE AQUI: as 3 categorias somam o total de homicídios?>

# ----------------------------------------------------------------
# PASSO 6 — NÚMEROS DE CONTROLE (antes de filtrar qualquer coisa!)
# Por quê: se você já tivesse descartado quem tem raça em branco, o
# nº 4 daria 0. Estes números são calculados na base inteira.
# ----------------------------------------------------------------
print("1) homicídios (todas as idades):", dados["homicidio"].sum())
# <COLE AQUI>
print("2) óbitos por qualquer causa, 15–29 anos:", dados["idade_anos"].between(15, 29).sum())
# <COLE AQUI>   (sem filtro de sexo, como está no enunciado)
print("3) homicídios por arma de fogo:", (dados["meio"] == "Arma de fogo").sum())
# <COLE AQUI>
print("4) homicídios com raça/cor ignorada ou em branco:",
      (dados["homicidio"] & dados["raca"].isna()).sum())
# <COLE AQUI>

# ----------------------------------------------------------------
# PASSO 7 — Funil de exclusões: número e motivo em cada passo
# O que faz: vai afunilando a população e imprime quantos saíram.
# Por quê: "toda exclusão sai com número e motivo". Cada filtro cria
# um objeto NOVO; "dados" continua inteiro.
# ----------------------------------------------------------------
print("Todos os óbitos de residentes:", len(dados))

h = dados[dados["sexo"] == "Masculino"]
print("Homens:", len(h), "| excluídos (mulheres e sexo ignorado):", len(dados) - len(h))

h = h[h["idade_anos"].between(15, 29)]
print("Homens de 15 a 29 anos:", len(h))

h_assoc = h[h["raca_grupo"].notna()]
print("Com raça negra ou branca:", len(h_assoc),
      "| excluídos (amarela, indígena, ignorada/em branco):", len(h) - len(h_assoc))
# h e h_assoc são as populações da Parte 2.