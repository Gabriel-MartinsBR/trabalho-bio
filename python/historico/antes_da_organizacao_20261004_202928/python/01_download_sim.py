from ftplib import FTP
import os

# ftplib é uma biblioteca NATIVA do Python, então eu não utilizei
# o pip do terminal para instalar. Ela implementa o protocolo FTP
# (File Transfer Protocol), usado pelo DATASUS para disponibilizar
# os arquivos publicamente.

local_path = "dados/DOAL2025.dbc"

ftp = FTP("ftp.datasus.gov.br", timeout=15)
# Nesse momento, ela abre uma conexão com o servidor FTP oficial
# do DATASUS. Preferi determinar também que, se o servidor não
# responder em 15 segundos, a conexão será abortada.

ftp.login()
# O servidor do DATASUS não exige login, então eu deixei em branco
# para entrar como anônimo.

ftp.cwd("/dissemin/publicos/SIM/PRELIM/DORES")
# Muda o diretório de trabalho no servidor remoto
# (cwd = change working directory) para a pasta onde ficam os dados
# PRELIMINARES do SIM (Sistema de Informação sobre Mortalidade),
# especificamente a subpasta DORES (Declarações de Óbito).

with open(local_path, "wb") as f:
    ftp.retrbinary("RETR DOAL2025.dbc", f.write)

# Abre o arquivo local em modo de escrita binária
# ("wb" = write binary), necessário porque .dbc é um arquivo
# binário compactado, não texto.
#
# ftp.retrbinary envia o comando RETR (retrieve) ao servidor,
# pedindo o arquivo DOAL2025.dbc e, a cada pedaço de dado recebido,
# chama f.write para gravá-lo no arquivo local.

ftp.quit()
# Encerra a conexão com o servidor (envia o comando QUIT antes
# de fechar o socket).

print("Baixouuuuuuuuu:", local_path)
# Confirma no console que o download terminou e onde o arquivo está.