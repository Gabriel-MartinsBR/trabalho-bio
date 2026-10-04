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
# (a) Convertendo o arquivo baixado
# ==========================================================

if (pasta_dados / "DOAL2025.csv").exists():
    dados = pd.read_csv(
        pasta_dados / "DOAL2025.csv",
        dtype="string",
        encoding="utf-8-sig"
    )
    # Como eu já converti o arquivo, só abro o CSV que foi conferido.
    # Assim, não preciso descompactar e salvar a mesma base toda vez.

else:
    import datasus_dbc
    from dbfread import DBF
    # datasus_dbc desfaz a compactação específica do DATASUS.
    # DBF lê a tabela descompactada. Nesta versão, utilizei dbfread
    # no lugar de simpledbf e conferi que o resultado é idêntico.

    datasus_dbc.decompress(
        str(pasta_dados / "DOAL2025.dbc"),
        str(pasta_dados / "DOAL2025.dbf")
    )
    print("Convertido para .dbf com sucesso")

    dbf = DBF(
        str(pasta_dados / "DOAL2025.dbf"),
        encoding="latin1"
    )
    # latin1 é a codificação de caracteres utilizada nesse arquivo.
    # Preciso dela para ler os textos com acentuação corretamente.

    dados = pd.DataFrame(iter(dbf))
    # Transforma os registros do DBF em uma tabela do pandas.

    dados.to_csv(
        pasta_dados / "DOAL2025.csv",
        index=False,
        encoding="utf-8-sig"
    )
    # index=False evita salvar a numeração das linhas como uma variável.
    # utf-8-sig preserva a acentuação e também facilita abrir no Excel.

print(dados.shape)
print(dados.head())
print("Salvo em:", pasta_dados / "DOAL2025.csv")
# Obtido na cópia original: 22.936 linhas e 87 variáveis.
