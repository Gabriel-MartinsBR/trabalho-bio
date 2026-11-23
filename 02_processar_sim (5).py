import datasus_dbc
from simpledbf import Dbf5

# Etapa 2: descompacta o .dbc para .dbf
datasus_dbc.decompress("dados/DOAL2025.dbc", "dados/DOAL2025.dbf")
print("Convertido para .dbf com sucesso")

# Etapa 3: lê o .dbf e transforma em DataFrame
dbf = Dbf5("dados/DOAL2025.dbf", codec="latin1")
dados = dbf.to_dataframe()

print(dados.shape)
print(dados.head())

# Salva o DataFrame em CSV, preservando acentuação (utf-8-sig funciona bem no Excel também)
dados.to_csv("dados/DOAL2025.csv", index=False, encoding="utf-8-sig")

print("Salvo em: dados/DOAL2025.csv")