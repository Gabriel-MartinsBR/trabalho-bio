# Parte 1: Homicídios, juventude e raça/cor
# Gabriel Martins, Hadassah Teodoro e Ruanytha Miranda - Turma 101
# Enunciado n: 2 | Download original: 23/09/2026
# Uso de IA: Claude e ChatGPT/Codex, declarado na versão de entrega.
# Resultados comentados: cópia original, não um novo download.

import pandas as pd
from pathlib import Path

pasta_projeto = Path(__file__).resolve().parent.parent
pasta_dados = pasta_projeto / "dados"
# Nesse momento, pego a pasta do projeto a partir do próprio arquivo.
# Fiz assim porque o CSV está dentro de dados, e não dentro de python.
# Com isso, o caminho funciona mesmo se eu abrir o terminal em outra pasta.

# ==========================================================
# (c) Conferindo as variáveis antes de tratar
# ==========================================================

dados = pd.read_csv(
    pasta_dados / "DOAL2025.csv",
    dtype="string",
    encoding="utf-8-sig"
)

variaveis = ["CAUSABAS", "IDADE", "SEXO", "RACACOR", "ESC", "LOCOCOR", "CODMUNRES"]

print("Tipos de dados:")
print(dados[variaveis].dtypes)
# Dessa vez, eu já leio tudo como texto para não perder zeros à esquerda.
# O tipo que o pandas usa para armazenar o campo não é o tipo estatístico.

linhas = ["Tipos de dados:", dados[variaveis].dtypes.to_string()]
(pasta_dados / "conferencias").mkdir(exist_ok=True)
(pasta_dados / "tabelas").mkdir(exist_ok=True)

for v in variaveis:
    print(f"\n--- {v} ---")
    print(f"Valores únicos: {dados[v].nunique()}")
    print(f"Faltantes (NaN): {dados[v].isna().sum()}")
    print(dados[v].value_counts(dropna=False).head(15))
    # Assim como eu tinha feito antes, olho os valores mais frequentes.
    # Também salvo a contagem completa, porque só os 15 primeiros
    # poderiam esconder os códigos raros, como a idade ignorada.

    frequencias = dados[v].value_counts(dropna=False).sort_index()
    frequencias.to_csv(
        pasta_dados / f"conferencias/codigos_{v}.csv",
        encoding="utf-8-sig"
    )
    linhas.extend([f"\n--- {v} ---", frequencias.to_string()])

(pasta_dados / "saida_dicionario.txt").write_text(
    "\n".join(linhas),
    encoding="utf-8"
)
# Agora a própria execução salva a saída, sem precisar redirecionar
# o console manualmente para o arquivo saida_dicionario.txt.

# (c) Dicionário das sete variáveis. Idade é um tempo quantitativo CONTÍNUO;
# idade_anos registra anos completos, com precisão discretizada pelo SIM.
# O PDF anterior trocava as unidades 0/1/2 e chamava a idade de discreta.
linhas_dicionario = [
    [
        "CAUSABAS",
        "Causa básica do óbito, CID-10",
        "Texto, ex. I219 ou X954; primeiros 3 caracteres identificam a categoria",
        "Qualitativa nominal"
    ],
    [
        "IDADE",
        "Idade ao óbito com unidade codificada",
        "3 dígitos: 0 minutos, 1 horas, 2 dias, 3 meses, 4 anos, 5 = 100 + valor; 000/999 ignorados",
        "Quantitativa contínua; anos completos na variável derivada"
    ],
    [
        "SEXO",
        "Sexo registrado na declaração de óbito",
        "1 masculino; 2 feminino; 0/9 ignorado",
        "Qualitativa nominal"
    ],
    [
        "RACACOR",
        "Raça/cor registrada na declaração de óbito",
        "1 branca; 2 preta; 3 amarela; 4 parda; 5 indígena; 9/branco ignorado",
        "Qualitativa nominal"
    ],
    [
        "ESC",
        "Escolaridade em faixas de anos de estudo",
        "1 nenhuma; 2 de 1 a 3; 3 de 4 a 7; 4 de 8 a 11; 5 de 12 ou mais; 9/branco ignorado",
        "Qualitativa ordinal"
    ],
    [
        "LOCOCOR",
        "Local de ocorrência do óbito",
        "1 hospital; 2 outro estabelecimento de saúde; 3 domicílio; 4 via pública; 5 outros; 9/branco ignorado",
        "Qualitativa nominal"
    ],
    [
        "CODMUNRES",
        "Município de residência",
        "Código IBGE de 6 dígitos, texto identificador; prefixo 27 = Alagoas",
        "Qualitativa nominal"
    ],
]
dicionario = pd.DataFrame(
    linhas_dicionario,
    columns=["variavel", "o_que_registra", "codificacao", "tipo_estatistico"]
)
dicionario.to_csv(
    pasta_dados / "tabelas/dicionario_variaveis.csv",
    index=False,
    encoding="utf-8-sig"
)
print("\nDicionário:\n" + dicionario.to_string(index=False))

