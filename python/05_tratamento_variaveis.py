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
