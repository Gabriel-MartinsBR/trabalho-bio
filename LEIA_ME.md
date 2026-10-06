# Trabalho de Bioestatística - Parte 1

Mantive a organização que já estava sendo utilizada, com `dados`, `python` e `r`. As etapas estão em arquivos separados e numerados. 

```text
Trabalho_Bioestatistica/
    dados/
        DOAL2025.dbc
        DOAL2025.csv
        DOAL2025_tratado.csv
        homens_15_29_negra_branca.csv
        numeros_controle.json
        proveniencia_original.json
        saida_dicionario.txt
        saida_*.txt
        conferencias/
        tabelas/
        graficos/
    python/
        01_download_sim.py
        02_processar_sim.py
        03_conferencia_variaveis.py
        04_dicionario_variaveis.py
        05_tratamento_variaveis.py
        06_numeros_controle.py
        07_tabela_frequencias.py
        08_histograma_idade.py
        09_limitacoes_e_erros.py
    entrega/
        Parte1_Gabriel_Hadassah_Ruanytha.py
```

Os arquivos `DOAL2025.dbc` e `DOAL2025.csv` são os originais de 23/09/2026. O tratamento é salvo em outro CSV. Se o DBF original já estiver na sua pasta, ele também permanece lá.

## Executando por etapas

Abra a pasta `Trabalho_Bioestatistica` no VS Code e, no terminal, instale as bibliotecas:

```powershell
python -m pip install -r requirements.txt
```

Depois, execute os arquivos na ordem:

```powershell
python python/01_download_sim.py
python python/02_processar_sim.py
python python/03_conferencia_variaveis.py
python python/04_dicionario_variaveis.py
python python/05_tratamento_variaveis.py
python python/06_numeros_controle.py
python python/07_tabela_frequencias.py
python python/08_histograma_idade.py
python python/09_limitacoes_e_erros.py
```

Os dois primeiros aproveitam os arquivos já baixados e convertidos. Para continuar de onde você tinha parado, pode começar pelo `05`, desde que o CSV original esteja em `dados`. O `06` lê o CSV tratado salvo pelo `05`. O `07` e o `08` também usam essa base tratada; o `08` atualiza a tabela de exclusões produzida nas etapas anteriores.

O `04` salva automaticamente `saida_dicionario.txt`. Os outros arquivos `saida_*.txt` incluídos na pasta registram a execução conferida desta versão. Para atualizar uma saída no PowerShell, você pode usar:

```powershell
python python/06_numeros_controle.py > dados/saida_numeros_controle.txt
```

## Versão única para entregar

A pasta `entrega` contém as nove etapas reunidas em um único `.py`, também com código em sequência e comentários. Você pode executar essa versão diretamente:

```powershell
python entrega/Parte1_Gabriel_Hadassah_Ruanytha.py
```

Ela reproduz os mesmos resultados dos arquivos separados. Antes de entregar, preencha as matrículas e revise a declaração de IA e de compreensão do código no cabeçalho.

## Resultados conferidos

- Base: 22.936 óbitos e 87 variáveis.
- Homicídios, todas as idades: 1.107.
- Óbitos por qualquer causa entre 15 e 29 anos, ambos os sexos: 1.365.
- Homicídios por arma de fogo: 832.
- Homicídios com raça/cor ignorada ou em branco: 12.
- Homens de 15 a 29 anos: 1.124; no contraste negra x branca: 1.104.

A tabela do meio empregado e o dicionário ficam em `dados/tabelas`. O histograma fica em `dados/graficos`. Não foi feita a Parte 2.

As referências de codificação estão no script de entrega e na proveniência da base. Na atualização da pasta da Área de Trabalho, os arquivos antigos são guardados em `python/historico` antes da substituição.
