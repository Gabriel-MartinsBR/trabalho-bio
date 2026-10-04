# Parte 1: Homicídios, juventude e raça/cor
# Gabriel Martins, Hadassah Teodoro e Ruanytha Miranda - Turma 101
# Enunciado n: 2 | Download original: 23/09/2026
# Uso de IA: Claude e ChatGPT/Codex, declarado na versão de entrega.
# Resultados comentados: cópia original, não um novo download.

import pandas as pd
import hashlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

pasta_projeto = Path(__file__).resolve().parent.parent
pasta_dados = pasta_projeto / "dados"
# Nesse momento, pego a pasta do projeto a partir do próprio arquivo.
# Fiz assim porque o CSV está dentro de dados, e não dentro de python.
# Com isso, o caminho funciona mesmo se eu abrir o terminal em outra pasta.

# ==========================================================
# (e) Fazendo o histograma da idade dos homicídios
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
obitos_homicidio = dados[homicidio].copy()
sha256 = hashlib.sha256((pasta_dados / "DOAL2025.csv").read_bytes()).hexdigest()
assinatura_original = "ba754138484a991871d19564b9eaedff73d15bfe6f55648af9a570e331c123af"
origem = "Download original: 23/09/2026." if sha256 == assinatura_original else "Cópia atualizada; conferir a data do download."
(pasta_dados / "graficos").mkdir(exist_ok=True)

# Agora vou olhar como a idade dos homicídios está distribuída.
# Utilizei intervalos de 5 anos para o gráfico ficar fácil de ler.
# Coloquei título, nomes dos eixos e fonte para ele ser compreensível
# mesmo quando estiver separado do restante do código.

# Histograma: retirar SOMENTE idades ausentes entre os homicídios.
com_idade = obitos_homicidio[obitos_homicidio["idade_anos"].notna()].copy()
print("Homicídios no gráfico:", len(com_idade))
print(
    "Excluídos do gráfico por idade ignorada:",
    len(obitos_homicidio) - len(com_idade)
)
# Resultado original: 1.107 no gráfico, zero exclusões; mínimo=1, máximo=89.
idades = com_idade["idade_anos"].to_numpy(dtype=float)
fig, ax = plt.subplots(figsize=(10, 6))
limite = max(5, (int(idades.max()) // 5 + 1) * 5) if len(idades) else 5
ax.hist(
    idades,
    bins=list(range(0, limite + 1, 5)),
    color="#22687b",
    edgecolor="white",
    linewidth=1
)
ax.set_title(
    "Idade ao óbito por homicídio\nResidentes em Alagoas, 2025",
    loc="left",
    fontweight="bold",
    fontsize=15,
    pad=18
)
ax.set_xlabel("Idade ao óbito (anos completos)", fontsize=11)
ax.set_ylabel("Número de óbitos", fontsize=11)
ax.set_xticks(list(range(0, limite + 1, 10)))
ax.set_xlim(0, limite)
ax.set_axisbelow(True)
ax.grid(axis="y", alpha=0.20)
ax.spines[["top", "right"]].set_visible(False)
ax.text(
    0.98,
    0.96,
    f"n = {len(com_idade):,}".replace(",", ".") + f" | idade ausente: {len(obitos_homicidio) - len(com_idade)}",
    transform=ax.transAxes,
    ha="right",
    va="top",
    fontsize=10
)
fig.text(
    0.09,
    0.045,
    "Fonte: SIM/DATASUS, dados preliminares de 2025. " + origem,
    fontsize=9
)
fig.subplots_adjust(left=0.09, right=0.98, top=0.84, bottom=0.16)
fig.savefig(
    pasta_dados / "graficos/histograma_idade_homicidios.png",
    dpi=180
)
plt.close(fig)

exclusoes = pd.read_csv(pasta_dados / "tabelas/exclusoes_por_etapa.csv")
exclusoes = exclusoes[exclusoes["etapa"] != "Histograma dos homicídios"].copy()
exclusoes.loc[len(exclusoes)] = [
    "Histograma dos homicídios",
    len(obitos_homicidio),
    len(obitos_homicidio) - len(com_idade),
    len(com_idade),
    "idade ignorada, apenas para o gráfico"
]
exclusoes.to_csv(
    pasta_dados / "tabelas/exclusoes_por_etapa.csv",
    index=False,
    encoding="utf-8-sig"
)
print("Gráfico salvo em:", pasta_dados / "graficos/histograma_idade_homicidios.png")
