# -*- coding: utf-8 -*-
# Nome(s): Gabriel Martins, Hadassah Teodoro e Ruanytha Miranda - Turma 101.
# Matrícula(s): não informadas; preencher antes da entrega.
# Enunciado n: 2.
#
# DECLARAÇÃO DE USO DE INTELIGÊNCIA ARTIFICIAL
# Usei ferramenta de IA neste trabalho? ( ) Não (X) Sim.
# Ferramentas: Claude (rascunho mencionado no passo a passo) e ChatGPT/Codex.
# Uso: auxílio no tratamento; revisão da codificação; conclusão dos itens (a)-(f);
# organização do script e verificação dos resultados na base fornecida.
# Pedido: terminar SOMENTE a Parte 1 em Python, autorizado pela professora.
# Correções realizadas na revisão assistida: caminho do CSV, unidades de IDADE,
# idade ignorada 999, SEXO=0, dicionário e comentários com resultados reais.
# Cada integrante deve revisar o código e confirmar, antes de entregar:
# "Declaro que compreendo todo o código que estou entregando e que sou capaz
# de explicá-lo oralmente."
#
# Download original: 23/09/2026, confirmado por Gabriel em 04/10/2026.
# Fonte: SIM/DATASUS, óbitos de residentes em Alagoas, 2025, PRELIMINARES.
# Esta versão aproveita o download original e NÃO o substitui automaticamente.
# Os arquivos numerados são as etapas que utilizo para organizar o trabalho.
# A versão única para entregar fica na pasta entrega.
#
# Executar este arquivo reproduz todas as etapas na ordem de 01 a 09.
# Ele procura os dados na pasta dados, ao lado de python e entrega.

# Referências de codificação consultadas em 04/10/2026:
# Guia do estudante e Enunciado 2 fornecidos pela professora.
# https://github.com/rfsaldanha/microdatasus/blob/master/R/process_sim.R
# https://github.com/mymatsubara/datasus-dbc-py
# https://planalto.gov.br/ccivil_03/_ato2007-2010/2010/lei/l12288.htm


# ================================================================
# Arquivo: 01_download_sim.py
# ================================================================

from ftplib import FTP
from datetime import datetime, timezone, timedelta
from pathlib import Path

pasta_projeto = Path(__file__).resolve().parent.parent
pasta_dados = pasta_projeto / "dados"
# Nesse momento, pego a pasta do projeto a partir do próprio arquivo.
# Fiz assim porque o CSV está dentro de dados, e não dentro de python.
# Com isso, o caminho funciona mesmo se eu abrir o terminal em outra pasta.

# ==========================================================
# (a) Baixando os dados do SIM
# ==========================================================

# ftplib é uma biblioteca NATIVA do Python, então eu não utilizei
# o pip do terminal para instalar. Ela implementa o protocolo FTP
# (File Transfer Protocol), usado pelo DATASUS para disponibilizar
# os arquivos publicamente.

local_path = pasta_dados / "DOAL2025.dbc"

if local_path.exists():
    print("O arquivo já foi baixado:", local_path)
    # Como eu já baixei essa base no dia 23/09/2026, preferi continuar
    # utilizando o mesmo arquivo. Os dados de 2025 são preliminares,
    # então baixar novamente poderia mudar os resultados que conferi.

else:
    pasta_dados.mkdir(parents=True, exist_ok=True)

    ftp = FTP("ftp.datasus.gov.br", timeout=60)
    # Nesse momento, ela abre uma conexão com o servidor FTP oficial
    # do DATASUS. Deixei 60 segundos para dar tempo de ele responder.

    ftp.login()
    # O servidor não exige login, então entrei como anônimo.

    ftp.cwd("/dissemin/publicos/SIM/PRELIM/DORES")
    # Muda o diretório no servidor para os dados PRELIMINARES do SIM,
    # especificamente a subpasta dos óbitos por residência.

    with open(local_path, "wb") as f:
        ftp.retrbinary("RETR DOAL2025.dbc", f.write)
    # Abre o arquivo local em modo de escrita binária (wb).
    # Cada pedaço recebido pelo FTP é gravado por f.write.

    ftp.quit()
    # Encerra a conexão com o servidor depois de terminar o download.

    data_download = datetime.now(timezone(timedelta(hours=-3)))
    (pasta_dados / "data_download.txt").write_text(
        data_download.isoformat(),
        encoding="utf-8"
    )
    # Se eu precisar baixar do zero, esta linha registra a data real.
    # Os comentários com os números abaixo se referem à cópia original
    # de 23/09/2026; uma nova cópia pode trazer outros resultados.

    print("Baixouuuuuuuuu:", local_path)
    print("Data do download:", data_download)

# ================================================================
# Arquivo: 02_processar_sim.py
# ================================================================

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

# ================================================================
# Arquivo: 03_conferencia_variaveis.py
# ================================================================

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

# ================================================================
# Arquivo: 04_dicionario_variaveis.py
# ================================================================

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


# ================================================================
# Arquivo: 05_tratamento_variaveis.py
# ================================================================

import pandas as pd
from pathlib import Path

pasta_projeto = Path(__file__).resolve().parent.parent
pasta_dados = pasta_projeto / "dados"
# Nesse momento, pego a pasta do projeto a partir do próprio arquivo.
# Fiz assim porque o CSV está dentro de dados, e não dentro de python.
# Com isso, o caminho funciona mesmo se eu abrir o terminal em outra pasta.

# ================================================================
# (d) Tratando as variáveis
# Ritmo de cada passo: OLHAR -> DECIDIR -> TRATAR -> CONTAR
# ================================================================

CAMINHO = pasta_dados / "DOAL2025.csv"
COLUNAS = ["CAUSABAS", "IDADE", "SEXO", "RACACOR", "ESC", "LOCOCOR", "CODMUNRES"]

dados = pd.read_csv(
    CAMINHO,
    usecols=COLUNAS + ["DTOBITO", "TIPOBITO"],
    dtype="string",
    encoding="utf-8-sig"
)
# Nesse momento, leio as sete variáveis do trabalho e dois campos
# auxiliares para conferir o ano e o tipo do óbito.
# Preferi ler tudo como texto para tratar os códigos depois de olhar.

for col in dados.columns:
    dados[col] = dados[col].str.strip().replace("", pd.NA)
    # Tira espaços nas extremidades e transforma campo vazio em NA.
    # Não estou excluindo a linha, apenas indicando que a informação falta.

# (d) População geral: óbitos não fetais de RESIDENTES de AL em 2025.
# Conferência original: CODMUNRES começa com 27 nos 22.936 registros;
# DTOBITO pertence a 2025 em todos; TIPOBITO=2 em todos. Exclusões: zero.
# DTOBITO e TIPOBITO são campos auxiliares para conferir o recorte.
exclusoes = []

antes = len(dados)
dados = dados[dados["CODMUNRES"].str.fullmatch(r"27\d{4}", na=False)].copy()
exclusoes.append(
    ["Residência em AL", antes, antes - len(dados), len(dados), "município ausente, malformado ou fora de AL"]
)
print("Residentes em Alagoas:", len(dados), "| excluídos:", antes - len(dados))
datas = pd.to_datetime(dados["DTOBITO"], format="%d%m%Y", errors="coerce")
antes = len(dados)
dados = dados[datas.dt.year.eq(2025)].copy()
exclusoes.append(
    ["Ano de 2025", antes, antes - len(dados), len(dados), "data ausente/inválida ou ano diferente"]
)
print("Óbitos de 2025:", len(dados), "| excluídos:", antes - len(dados))
antes = len(dados)
dados = dados[dados["TIPOBITO"].eq("2")].copy()
exclusoes.append(
    ["Óbitos não fetais", antes, antes - len(dados), len(dados), "óbito fetal ou tipo não informado"]
)
print("Óbitos não fetais:", len(dados), "| excluídos:", antes - len(dados))

# ----------------------------------------------------------------
# PASSO 2 - Convertendo a idade para anos
# ----------------------------------------------------------------
# A primeira coisa que precisei perceber foi que IDADE não está em anos.
# Por isso, separo a unidade da quantidade antes de fazer qualquer conta.
# IDADE: conferência dos códigos. Unidade: 0=38, 1=92, 2=265, 3=178,
# 4=22.124, 5=235, 9=4. Todos os textos têm 3 dígitos; 000=0 e 999=4.
# Exemplos: 005=5 minutos; 218=18 dias; 311=11 meses; 477=77 anos.
# O código 999 vira NA, nunca 999 anos. Unidade 5 inclui também 100 anos.
idade_codigo = dados["IDADE"].str.zfill(3)
unidade = idade_codigo.str[0]
quantidade = pd.to_numeric(idade_codigo.str[1:], errors="coerce")
print(
    "\nComprimento original de IDADE:\n" + dados["IDADE"].str.len().value_counts(dropna=False).to_string()
)
print(
    "Unidades de IDADE:\n" + unidade.value_counts(dropna=False).sort_index().to_string()
)
valida = idade_codigo.str.fullmatch(r"[0-5]\d{2}", na=False) & ~idade_codigo.isin(["000", "999"])
dados["idade_anos"] = pd.Series(pd.NA, index=dados.index, dtype="Float64")
dados.loc[valida & unidade.isin(["0", "1", "2", "3"]), "idade_anos"] = 0
dados.loc[valida & unidade.eq("4"), "idade_anos"] = quantidade
dados.loc[valida & unidade.eq("5"), "idade_anos"] = 100 + quantidade
# DECISÃO 1: 573 menores de 1 ano ficam com 0 anos completos.
# Não transformei esses casos em NA nem os excluí da base geral, pois sua
# idade é conhecida e a população de comparação inclui todos os óbitos.
# Resultado: 22.932 idades conhecidas; 4 ignoradas. Nenhuma linha apagada.
print("Idade em anos completos:\n" + dados["idade_anos"].describe().to_string())

# ----------------------------------------------------------------
# PASSO 3 - Tratando o sexo
# ----------------------------------------------------------------
# Agora troco os códigos pelos rótulos para conseguir ler a tabela.
# SEXO: 1=12.859; 2=10.071; 0=6; 9=0; vazios=0. O 0 é ignorado,
# não um código anômalo nem um terceiro sexo, corrigindo o PDF anterior.
dados["sexo"] = pd.Categorical(
    dados["SEXO"].map({"1": "Masculino", "2": "Feminino"}),
    categories=["Masculino", "Feminino"]
)

# ----------------------------------------------------------------
# PASSO 4 - Tratando raça/cor e formando o grupo negra x branca
# ----------------------------------------------------------------
# Nesse momento, mantenho as cinco categorias e crio outro campo
# somente para o agrupamento pedido no enunciado.
# RACACOR: 1=4.821; 2=1.345; 3=139; 4=15.905; 5=99; vazios=627;
# código 9=0. Ausências permanecem NA; não se imputa raça/cor.
rotulos_raca = {
    "1": "Branca",
    "2": "Preta",
    "3": "Amarela",
    "4": "Parda",
    "5": "Indígena"
}
dados["raca"] = pd.Categorical(
    dados["RACACOR"].map(rotulos_raca),
    categories=list(rotulos_raca.values())
)
dados["raca_grupo"] = pd.Categorical(
    dados["RACACOR"].map({"1": "Branca", "2": "Negra", "4": "Negra"}),
    categories=["Branca", "Negra"]
)
# Negra=17.250 (1.345 pretas + 15.905 pardas); branca=4.821;
# fora do contraste=865 (139 amarelas + 99 indígenas + 627 ausentes).
# Justificativa: definição de população negra do art. 1º, parágrafo único,
# IV, da Lei 12.288/2010. Aqui agrupamos a informação da declaração de
# óbito, sem presumir que foi necessariamente autodeclarada pelo falecido.
# DECISÃO 2: amarela e indígena permanecem na base e na variável raca.
# Não as agrupei com branca como "não negra", porque isso mudaria o
# contraste negra x branca exigido pelo enunciado.

# ----------------------------------------------------------------
# PASSO 5 - Tratando escolaridade e local de ocorrência
# ----------------------------------------------------------------
# Aqui preciso lembrar que os códigos da escolaridade são faixas,
# então o número 3 não quer dizer que a pessoa estudou três anos.
# ESC: 1=6.138; 2=3.113; 3=4.707; 4=3.129; 5=982; 9=1.801;
# vazios=3.066. Total de ausentes após tratamento=4.867.
# São FAIXAS ordenadas, não valores exatos de anos nem quantidade 1 a 5.
rotulos_esc = {
    "1": "Nenhuma",
    "2": "1 a 3 anos",
    "3": "4 a 7 anos",
    "4": "8 a 11 anos",
    "5": "12 anos ou mais"
}
dados["escolaridade"] = pd.Categorical(
    dados["ESC"].map(rotulos_esc),
    categories=list(rotulos_esc.values()),
    ordered=True
)
# LOCOCOR: 1=13.555; 2=1.957; 3=5.447; 4=974; 5=989; 9=14.
# Os 14 ignorados viram NA apenas nesta variável. Não são "Outros".
rotulos_local = {
    "1": "Hospital",
    "2": "Outro estabelecimento de saúde",
    "3": "Domicílio",
    "4": "Via pública",
    "5": "Outros"
}
dados["local_obito"] = pd.Categorical(
    dados["LOCOCOR"].map(rotulos_local),
    categories=list(rotulos_local.values())
)
# CODMUNRES: 102 códigos, zero ausentes. Mantido como identificador textual;
# não se calcula média de código municipal, que não é medida quantitativa.

# ----------------------------------------------------------------
# PASSO 6 - Identificando os homicídios e o meio empregado
# ----------------------------------------------------------------
# Preferi olhar os três primeiros caracteres do CID, porque o código
# completo pode ter um quarto caractere, como acontece com X954.
# CAUSABAS: 1.538 códigos distintos, zero ausentes ou códigos malformados.
# O sufixo do CID (ex. X954) não deve impedir a classificação em X95.
causa = dados["CAUSABAS"].str.upper().str.replace(".", "", regex=False)
causa_valida = causa.str.fullmatch(r"[A-Z]\d{2}[A-Z0-9]?", na=False)
dados["cid3"] = causa.where(causa_valida).str[:3]
dados["homicidio"] = dados["cid3"].str.fullmatch(r"X8[5-9]|X9\d|Y0\d", na=False).astype("boolean")
dados.loc[~causa_valida, "homicidio"] = pd.NA
# X85-X99 e Y00-Y09 = agressões, definição operacional do enunciado.
# Não usei CIRCOBITO, Y10-Y34 ou Y35: seriam outras definições.
homicidio = dados["homicidio"].fillna(False)
meios = pd.Series(pd.NA, index=dados.index, dtype="string")
meios.loc[homicidio] = "Outros"
meios.loc[homicidio & dados["cid3"].isin(["X93", "X94", "X95"])] = "Arma de fogo"
meios.loc[homicidio & dados["cid3"].eq("X99")] = "Objeto cortante"
ordem_meios = ["Arma de fogo", "Objeto cortante", "Outros"]
dados["meio"] = pd.Categorical(meios, categories=ordem_meios)
# Outros = demais homicídios X85-Y09. Não homicídios têm meio ausente
# por não aplicabilidade, e não por desconhecimento do meio de homicídio.

# ----------------------------------------------------------------
# Salvando a base tratada
# ----------------------------------------------------------------

dados.to_csv(
    pasta_dados / "DOAL2025_tratado.csv",
    index=False,
    encoding="utf-8-sig"
)
# Salvo em outro arquivo para manter o CSV original do jeito que veio.
# As sete colunas originais continuam na tabela; os tratamentos estão
# em novas colunas, como idade_anos, sexo, raca e meio.

colunas_tratadas = [
    "idade_anos", "sexo", "raca", "raca_grupo",
    "escolaridade", "local_obito", "homicidio"
]
ausentes = dados[colunas_tratadas].isna().sum()
print("\nFaltantes depois do tratamento:")
print(ausentes)
# Obtido: idade=4; sexo=6; raça=627; grupo racial=865;
# escolaridade=4.867; local=14; homicídio=0.
# A base geral continua com 22.936 óbitos. Não retirei uma observação
# só porque alguma variável, como escolaridade, estava sem informação.

(pasta_dados / "tabelas").mkdir(exist_ok=True)
ausentes.rename("n_ausente").to_csv(
    pasta_dados / "tabelas/ausencias_apos_tratamento.csv",
    encoding="utf-8-sig"
)

exclusoes = pd.DataFrame(
    exclusoes,
    columns=["etapa", "antes", "excluidos", "restantes", "motivo"]
)
exclusoes.to_csv(
    pasta_dados / "tabelas/exclusoes_por_etapa.csv",
    index=False,
    encoding="utf-8-sig"
)
print("Salvo em:", pasta_dados / "DOAL2025_tratado.csv")

# ================================================================
# Arquivo: 06_numeros_controle.py
# ================================================================

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

# ================================================================
# Arquivo: 07_tabela_frequencias.py
# ================================================================

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


# ================================================================
# Arquivo: 08_histograma_idade.py
# ================================================================

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

# ================================================================
# Arquivo: 09_limitacoes_e_erros.py
# ================================================================

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
