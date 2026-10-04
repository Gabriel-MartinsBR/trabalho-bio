# Parte 1: Homicídios, juventude e raça/cor
# Gabriel Martins, Hadassah Teodoro e Ruanytha Miranda - Turma 101
# Enunciado n: 2 | Download original: 23/09/2026
# Uso de IA: Claude e ChatGPT/Codex, declarado na versão de entrega.
# Resultados comentados: cópia original, não um novo download.

import pandas as pd
import json
from pathlib import Path

pasta_projeto = Path(__file__).resolve().parent.parent
pasta_dados = pasta_projeto / "dados"
# Nesse momento, pego a pasta do projeto a partir do próprio arquivo.
# Fiz assim porque o CSV está dentro de dados, e não dentro de python.
# Com isso, o caminho funciona mesmo se eu abrir o terminal em outra pasta.

# ==========================================================
# (d) Conferindo os números de controle
# ==========================================================

dados = pd.read_csv(
    pasta_dados / "DOAL2025_tratado.csv",
    dtype="string",
    encoding="utf-8-sig"
)

dados["idade_anos"] = pd.to_numeric(dados["idade_anos"], errors="coerce")
dados["homicidio"] = dados["homicidio"].map({"True": True, "False": False}).astype("boolean")
# Como eu salvei em CSV, os rótulos e códigos voltam como texto.
# Por isso, converto apenas a idade e o indicador de homicídio.
# A escolaridade continua sendo uma faixa ordenada, mesmo salva como texto.

homicidio = dados["homicidio"].fillna(False)
# Números de controle na população GERAL, antes do recorte de homens jovens.
n_homicidios = int(homicidio.sum())
print(f"1) Homicídios, todas as idades: {n_homicidios}")
# Resultado na cópia de 23/09/2026: 1.107 homicídios.
n_jovens = int(dados["idade_anos"].between(15, 29).sum())
print(f"2) Óbitos por qualquer causa, 15 a 29 anos, ambos os sexos: {n_jovens}")
# Resultado na cópia de 23/09/2026: 1.365 óbitos (sem filtrar sexo).
n_fogo = int(dados["meio"].eq("Arma de fogo").sum())
print(f"3) Homicídios por arma de fogo: {n_fogo}")
# Resultado na cópia de 23/09/2026: 832 homicídios por arma de fogo.
n_raca_ignorada = int((homicidio & dados["raca"].isna()).sum())
print(f"4) Homicídios com raça/cor ignorada ou em branco: {n_raca_ignorada}")
# Resultado na cópia de 23/09/2026: 12; todos em branco, nenhum RACACOR=9.


controles = {
    "homicidios_todas_idades": n_homicidios,
    "obitos_15_29_ambos_sexos": n_jovens,
    "homicidios_arma_fogo": n_fogo,
    "homicidios_raca_ignorada_branco": n_raca_ignorada
}

(pasta_dados / "numeros_controle.json").write_text(
    json.dumps(controles, ensure_ascii=False, indent=2),
    encoding="utf-8"
)
# Salvo os quatro números para conseguir conferir depois.
# Eles foram calculados na base geral, antes de selecionar homens jovens.
# Caso eu tirasse primeiro as raças sem informação, o quarto daria zero.

# ----------------------------------------------------------------
# Construindo a população da pergunta e contando quem saiu
# ----------------------------------------------------------------

exclusoes = pd.read_csv(pasta_dados / "tabelas/exclusoes_por_etapa.csv")
# Ao executar este arquivo novamente, atualizo apenas as suas etapas.
# Com isso, não duplico o mesmo registro de exclusão na tabela.
exclusoes = exclusoes[exclusoes["etapa"].isin([
    "Residência em AL", "Ano de 2025", "Óbitos não fetais"
])].copy()

antes = len(dados)
h = dados[dados["sexo"] == "Masculino"].copy()
print("Homens:", len(h), "| excluídos:", antes - len(h))
# Obtido: 12.859 homens. Saíram 10.077 = 10.071 mulheres + 6 ignorados.
novas_exclusoes = [
    ["Sexo masculino", antes, antes - len(h), len(h), "sexo feminino ou ignorado"]
]

antes = len(h)
h = h[h["idade_anos"].notna()].copy()
print("Homens com idade conhecida:", len(h), "| excluídos:", antes - len(h))
# Obtido: 12.855 homens; excluídos 4 por idade ignorada.
novas_exclusoes.append(
    ["Homens com idade conhecida", antes, antes - len(h), len(h), "idade ignorada"]
)

antes = len(h)
h = h[h["idade_anos"].between(15, 29)].copy()
print("Homens de 15 a 29 anos:", len(h), "| excluídos:", antes - len(h))
# Obtido: 1.124; saíram 11.731 por idade fora de 15 a 29 anos.
novas_exclusoes.append(
    ["Homens de 15 a 29 anos", antes, antes - len(h), len(h), "fora da faixa de 15 a 29 anos"]
)

print("Raça/cor dos homens jovens:")
print(h["raca"].value_counts(dropna=False))
# Obtido: parda=1.023; preta=19; branca=62; indígena=5;
# amarela=1; sem informação=14.

antes = len(h)
h_assoc = h[h["raca_grupo"].notna()].copy()
print("Com raça negra ou branca:", len(h_assoc), "| excluídos:", antes - len(h_assoc))
# Obtido: 1.104; saíram 20 = 14 ausentes + 1 amarela + 5 indígenas.
# Não retirei esses casos da base geral, só deste contraste racial.
# Esse arquivo apenas constrói o recorte; não faz teste de associação.
novas_exclusoes.append(
    ["Raça/cor negra ou branca", antes, antes - len(h_assoc), len(h_assoc), "raça/cor ausente, amarela ou indígena"]
)

novas_exclusoes = pd.DataFrame(novas_exclusoes, columns=exclusoes.columns)
exclusoes = pd.concat([exclusoes, novas_exclusoes], ignore_index=True)
exclusoes.to_csv(
    pasta_dados / "tabelas/exclusoes_por_etapa.csv",
    index=False,
    encoding="utf-8-sig"
)

h_assoc.to_csv(
    pasta_dados / "homens_15_29_negra_branca.csv",
    index=False,
    encoding="utf-8-sig"
)
print("Recorte salvo em:", pasta_dados / "homens_15_29_negra_branca.csv")
