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

# ==========================================================
# (e) Fazendo a tabela de frequências
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
n_homicidios = int(homicidio.sum())
ordem_meios = ["Arma de fogo", "Objeto cortante", "Outros"]
sha256 = hashlib.sha256((pasta_dados / "DOAL2025.csv").read_bytes()).hexdigest()
SHA256_ORIGINAL = "ba754138484a991871d19564b9eaedff73d15bfe6f55648af9a570e331c123af"

# Nesse momento, separo só os homicídios para contar o meio empregado.
# O percentual é calculado sobre os 1.107 homicídios, e não sobre todos
# os óbitos nem apenas sobre os homens de 15 a 29 anos.

# (e) Frequências de meio de homicídio, todas as idades e ambos os sexos.
obitos_homicidio = dados.loc[homicidio].copy()
contagens = obitos_homicidio["meio"].value_counts(sort=False).reindex(ordem_meios, fill_value=0)
tabela = contagens.rename("n").to_frame()
tabela["percentual"] = (100 * tabela["n"] / n_homicidios).round(2) if n_homicidios else 0.0
tabela.index.name = "meio_homicidio"
assert int(tabela["n"].sum()) == n_homicidios, "Os meios precisam somar todos os homicídios."
tabela.loc["Total"] = [n_homicidios, 100.0 if n_homicidios else 0.0]
tabela["n"] = tabela["n"].astype(int)
tabela.to_csv(pasta_dados / "tabelas/tabela_meio_homicidio.csv", encoding="utf-8-sig")
print("\nTabela - Meio do homicídio, residentes em AL, 2025:\n" + tabela.to_string())
origem = "Download original: 23/09/2026." if sha256 == SHA256_ORIGINAL else "Cópia diferente da original; conferir proveniência."
print("Denominador: todos os homicídios. Fonte: SIM/DATASUS, preliminar. " + origem)
# Resultados originais: fogo 832 (75,16%); cortante 132 (11,92%);
# outros 143 (12,92%); total 1.107 (100,00%).

