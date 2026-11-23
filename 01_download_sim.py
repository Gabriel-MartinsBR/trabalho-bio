# Parte 1: Homicídios, juventude e raça/cor
# Gabriel Martins, Hadassah Teodoro e Ruanytha Miranda - Turma 101
# Enunciado n: 2 | Download original: 23/09/2026
# Uso de IA: Claude e ChatGPT/Codex, declarado na versão de entrega.
# Resultados comentados: cópia original, não um novo download.

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
