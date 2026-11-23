# Parte 2 — Homicídios, juventude e raça/cor

Gabriel Martins, Hadassah Teodoro e Ruanytha Miranda · UFTM · Bioestatística · Enunciado 2.

Continuação da Parte 1, usando **a mesma cópia de Alagoas/2025, baixada em 23/09/2026**. Não houve novo download. Os dados originais da Parte 1 foram preservados.

## Arquivos para a entrega

- [Relatório PDF](../entrega/Parte2_Gabriel_Hadassah_Ruanytha.pdf): **10 páginas de relatório + 2 de anexo**, com as cinco seções exigidas. Cada teste principal apresenta os oito itens pedidos.
- [Script R](../entrega/Parte2_Gabriel_Hadassah_Ruanytha.R): versão completa e comentada, anexada ao PDF. **Ainda não executada**, pois R não está instalado no ambiente de preparação. Usa somente bibliotecas incluídas no R. Deve ser executada antes de entregar em R.
- [Análise Python executada](analisar.py): fonte dos números, CSVs e gráficos. O projeto da Parte 1 registra autorização da docente para Python; confirmar se essa autorização também cobre a entrega da Parte 2.
- [Gerador do PDF](gerar_relatorio.py): formatação do relatório, com fonte Arial instalada no Windows.
- [Relatório legível no GitHub](RELATORIO.md).
- [Resultados numéricos](resultados.json), [tabelas](tabelas/) e [gráficos](graficos/).
- [Verificação independente](verificar.py) e [registro de verificação](verificacao.txt).

## Como reproduzir

Na **raiz do repositório**, com Python 3.12:

```powershell
python -m pip install -r parte2/requirements.txt
python parte2/analisar.py
python parte2/verificar.py
python parte2/gerar_relatorio.py
```

O script localiza a raiz pelo próprio arquivo, não pelo diretório do terminal. Não requer internet após instalar dependências; lê `dados/DOAL2025_tratado.csv`. Conserva todos os arquivos da Parte 1. A geração do PDF requer as fontes `C:/Windows/Fonts/arial.ttf` e `arialbd.ttf`; análises e gráficos são independentes dessas fontes. Para outro sistema, adaptar apenas o registro de fontes no gerador.

Em R, execute da raiz:

```powershell
Rscript entrega/Parte2_Gabriel_Hadassah_Ruanytha.R
```

Saídas R são gravadas em `parte2/validacao_R/`, sem sobrescrever as saídas Python. Como os geradores pseudoaleatórios diferem entre linguagens, p por permutação e IC bootstrap podem variar ligeiramente. Estatísticas determinísticas, grupos e contagens devem coincidir.

## Resultados e interpretação

| Bloco | Resultado principal |
|---|---|
| Descritivos | 1.107 homicídios; idade mediana 28 anos; 75,16% por arma de fogo |
| Correlação municipal | 100 municípios; rho = −0,2535; p por permutação = 0,01095 |
| Associação racial | 1.104 óbitos; χ² = 36,5143; OR = 7,43 (IC95% 3,50–15,77) |
| Comparação etária | H = 29,3008; p < 0,001; épsilon² = 0,0247 |

**A OR refere-se a homicídio versus outras causas entre os óbitos**, não a risco de morrer entre residentes vivos. O indicador ecológico de escolaridade usa apenas registros conhecidos no denominador; com todos os óbitos, a correlação muda para −0,0385. A sensibilidade é discutida explicitamente, sem conclusão causal ou individual.

## Decisões de análise

- Correlação: todos os óbitos, agregados em 102 municípios; mínimo de 30 óbitos seleciona 100 municípios. Escolaridade até sete anos = ESC 1–3; conhecidos = ESC 1–5. As 4.867 ausências não viram escolaridade alta.
- Raça/cor: homens de 15–29 anos; preta+parda versus branca; 14 sem raça/cor, um amarelo e cinco indígenas ficam fora apenas desse contraste. Restam 1.104 de 1.124 óbitos.
- Idade por meio: todos os 1.107 homicídios, independentemente de sexo e idade. Três grupos independentes; Kruskal–Wallis com empates; complemento Mann–Whitney com Holm.
- Efeitos e poder: resultados pequenos por phi e épsilon²; poder calculado com efeito observado, declarado como aproximado nos testes não paramétricos. Poder pós-hoc não é evidência independente.
- Semente 20261123; 19.999 permutações bilaterais de Spearman; 5.000 reamostragens bootstrap. `rho²` não é interpretado como R² causal nem risco explicado.
- Três testes principais sem correção conjunta; Holm apenas para os três pares etários. Limitação de multiplicidade explicitada.

## Conferência e proveniência

`verificar.py` refaz as seleções diretamente do CSV original, confere recodificações, controles, tabela racial, estatísticas por fórmulas de postos e integridade do CSV tratado. `resultados.json` registra versões, hash SHA-256 e saídas sem arredondamento de apresentação. Não há afirmação de execução de R.

## Uso de inteligência artificial

ChatGPT/Codex foi usado nesta continuação para gerar/revisar código, executar análises, estruturar tabelas e gráficos e elaborar a redação. Os scripts contêm declaração específica, alternativas rejeitadas e diário de erros reais de dependências/rede. Os integrantes precisam revisar a interpretação, adequar a redação à própria voz e confirmar compreensão oral; não se atribui a eles revisão que ainda não ocorreu. O histórico de uso de Claude na Parte 1 foi preservado.

## Subir ao GitHub

Esta pasta faz parte de uma **cópia completa e atualizada do projeto**, preservando `dados/`, `python/`, os arquivos da Parte 1 e adicionando `parte2/` e os arquivos de entrega. No repositório existente, envie o **conteúdo da raiz do projeto**; os caminhos `dados/`, `python/`, `entrega/` e `parte2/` devem ficar lado a lado. Não é necessário habilitar GitHub Pages: o GitHub exibe o README, o relatório Markdown e permite baixar o PDF.

Não envie o ZIP como substituto dos arquivos se quiser que o GitHub mostre o conteúdo navegável. O ZIP é apenas um pacote para baixar e extrair. Não há automação de publicação nem envio à professora.

## Fontes de implementação

- Guia do estudante e Enunciado nº 2, fornecidos pela professora (PDFs locais).
- [SciPy — Spearman e cuidados com p em pequenas amostras](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html).
- [SciPy — qui-quadrado e frequências esperadas](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2_contingency.html).
- [SciPy — Kruskal–Wallis, empates e teste global](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kruskal.html).

As fontes orientam a implementação; todos os números foram calculados com os arquivos da Parte 1.
