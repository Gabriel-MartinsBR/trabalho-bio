"""Gera o PDF a partir dos resultados calculados; não insere valores de exemplo."""
from pathlib import Path
import json, html
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, Preformatted
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'parte2'
r=json.loads((OUT/'resultados.json').read_text(encoding='utf-8'))
e,a,c=r['ecologica'],r['associacao'],r['comparacao']
font=Path('C:/Windows/Fonts')
pdfmetrics.registerFont(TTFont('ArialBio',str(font/'arial.ttf')))
pdfmetrics.registerFont(TTFont('ArialBio-Bold',str(font/'arialbd.ttf')))
pdfmetrics.registerFontFamily('ArialBio',normal='ArialBio',bold='ArialBio-Bold',italic='ArialBio',boldItalic='ArialBio-Bold')
s=getSampleStyleSheet()
s.add(ParagraphStyle(name='TextoBio',fontName='ArialBio',fontSize=10.5,leading=15,spaceAfter=9,alignment=TA_JUSTIFY))
s.add(ParagraphStyle(name='NotaBio',fontName='ArialBio',fontSize=8.3,leading=11,spaceAfter=8,textColor=colors.HexColor('#455566')))
s.add(ParagraphStyle(name='TituloBio',fontName='ArialBio-Bold',fontSize=20,leading=24,spaceAfter=15,textColor=colors.HexColor('#16445b')))
s.add(ParagraphStyle(name='SubBio',fontName='ArialBio-Bold',fontSize=13,leading=17,spaceAfter=10,textColor=colors.HexColor('#16445b')))
s.add(ParagraphStyle(name='CelulaBio',fontName='ArialBio',fontSize=9,leading=12))
story=[]; source='Fonte: SIM/DATASUS, residentes em Alagoas, 2025 (preliminar); cópia de 23/09/2026.'
md=[]
def fmt(v,n=2): return f'{v:,.{n}f}'.replace(',','@').replace('.',',').replace('@','.')
def pval(v): return '&lt;0,001' if v<.001 else fmt(v,4)
def para(text,note=False):
    story.append(Paragraph(text,s['NotaBio' if note else 'TextoBio']));md.append(text.replace('<b>','').replace('</b>',''))
def heading(text,top=False):
    story.append(Paragraph(text,s['TituloBio' if top else 'SubBio']));md.append('\n'+('# ' if top else '## ')+text)
def page(): story.append(PageBreak());md.append('\n---\n')
def table(title,headers,rows,widths):
    para('<b>'+title+'</b>')
    matrix=[[Paragraph(html.escape(str(v)),s['CelulaBio']) for v in row] for row in [headers]+rows]
    t=Table(matrix,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dcecf1')),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),.8,colors.HexColor('#147d92')),('LINEBELOW',(0,-1),(-1,-1),.5,colors.HexColor('#a9bbc3')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f4f7f9')]),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    story.append(t);story.append(Spacer(1,8));para(source,True)
    md.append('| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |')
    md.extend('| '+' | '.join(map(str,row))+' |' for row in rows)
def figure(name,w=480,h=260):
    story.append(Image(str(OUT/'graficos'/name),width=w,height=h));para(source,True)
    md.append(f'![Gráfico](graficos/{name})')
def item(n,title,text): para(f'<b>{n}. {title}.</b> '+text)

heading('Homicídios, juventude e raça/cor',True)
para('Bioestatística · Medicina · UFTM · Enunciado nº 2 · Parte 2<br/>Gabriel Martins · Hadassah Teodoro · Ruanytha Miranda<br/>Prof.ª Ana Paula Fernandes · 23 de novembro de 2026',True)
heading('1. Objetivos')
para('Descrever os óbitos por homicídio de residentes em Alagoas em 2025; avaliar, nos municípios com pelo menos 30 óbitos, a correlação entre a proporção de homicídios entre os óbitos e a proporção de baixa escolaridade; verificar a associação entre raça/cor negra, em comparação à branca, e homicídio entre os óbitos de homens de 15 a 29 anos; e comparar a distribuição da idade das vítimas de homicídio segundo o meio empregado.')
heading('2. Metodologia')
para('Realizou-se estudo observacional, transversal, com dados secundários do Sistema de Informações sobre Mortalidade (SIM/DATASUS). Foi utilizada a cópia preliminar do arquivo DOAL2025.dbc, diretório SIM/PRELIM/DORES, baixada em 23/09/2026 e preservada na Parte 1. A obtenção e conversão foram realizadas em Python com datasus-dbc e dbfread, conforme a autorização para Python registrada no projeto. A Parte 2 parte do CSV tratado, sem novo download, e publica somente tabelas e gráficos agregados no relatório. A fonte contém 22.936 registros e 87 campos originais; o CSV tratado mantém as variáveis selecionadas e acrescenta as recodificações.')
para('Incluíram-se óbitos não fetais de residentes em Alagoas, ocorridos em 2025; as três verificações do recorte não excluíram registros. Para a descrição e comparação por meio, selecionaram-se 1.107 homicídios, todos com idade conhecida. Para a associação, selecionaram-se 1.124 óbitos de homens de 15–29 anos e, exclusivamente nesse bloco, retiraram-se 14 sem raça/cor, um amarelo e cinco indígenas, restando 1.104. Para a análise ecológica, agregaram-se todos os óbitos por residência: 100 dos 102 municípios atenderam ao mínimo de 30; dois municípios, que somavam 32 óbitos, ficaram fora somente desse bloco.')
para('A idade foi convertida do código SIM para anos completos: unidades 0–3 recebem zero anos completos, unidade 4 fornece os anos e unidade 5 acrescenta 100; códigos ignorados permanecem ausentes. Identificou-se homicídio pela categoria CID-10 X85–Y09. Raça/cor negra reúne preta e parda; amarela e indígena não foram reclassificadas como branca. O meio foi definido por X93–X95 (arma de fogo), X99 (objeto cortante) e demais agressões (outros). Escolaridade foi tratada como ordinal: até sete anos corresponde a ESC 1, 2 e 3. Sexo, raça/cor, local e meio são nominais; município é identificador, não medida quantitativa.')
page()
heading('2. Metodologia (continuação)',True)
para('Apresentaram-se frequências, percentuais, mediana e quartis, sem médias dos códigos ordinais. A escolaridade municipal usa como denominador os óbitos com ESC 1–5; a proporção municipal de homicídios usa todos os óbitos. Empregaram-se Spearman com p bilateral por 19.999 permutações, qui-quadrado de Pearson sem correção de continuidade e Kruskal–Wallis corrigido por empates, após examinar dispersão, histogramas, boxplots e frequências esperadas. O IC95% de rho foi obtido por 5.000 reamostragens de pares municipais. Como complemento exploratório do teste global, usaram-se Mann–Whitney bilaterais com ajuste de Holm para três pares. Adotou-se α=0,05 por análise principal; não houve ajuste conjunto para os três blocos, que respondem a perguntas distintas. A semente foi 20261123. Efeitos: rho, phi, odds ratio com IC95% log-Wald e épsilon quadrado. O poder é condicionado aos efeitos observados: aproximação normal z de Fisher para Spearman; qui-quadrado não central para associação; e F não central de ANOVA equilibrada, com n médio=N/3 e f derivado de épsilon quadrado, para Kruskal–Wallis. As aproximações não são poder exato dos testes não paramétricos nem evidência independente do valor-p.')
para(f'As análises e o PDF foram executados em Python {r["ambiente"]["python"]}, pandas {r["ambiente"]["pandas"]}, NumPy {r["ambiente"]["numpy"]}, SciPy {r["ambiente"]["scipy"]} e Matplotlib {r["ambiente"]["matplotlib"]}. O script principal lê a base da Parte 1, verifica os controles, gera tabelas, gráficos e resultados numéricos; o gerador do relatório apenas os formata. A versão equivalente em R acompanha a entrega, mas não foi executada neste ambiente, que não dispõe de R. Utilizaram-se dados públicos, sem contato com participantes nem tentativa de identificação; a apresentação é agregada. O enquadramento ético segue o caráter de dados públicos previsto no guia, sem afirmar aprovação por CEP. Houve apoio declarado de ChatGPT/Codex no código e na redação; cabe aos integrantes revisar a interpretação e compreender os scripts antes da entrega.')
table('Quadro metodológico — unidades e denominadores',['Bloco','Unidade e população','Denominador'],[
['Descritivos','Óbito por homicídio, todas as idades e sexos','1.107 homicídios'],
['Correlação','Município com ≥30 óbitos, todos os residentes falecidos','100 municípios; denominadores municipais explícitos'],
['Associação','Óbito de homem de 15–29 anos, negra ou branca','1.104 óbitos'],
['Comparação','Vítima de homicídio com idade e meio definidos','1.107 homicídios']], [82,220,181])
para('Fontes de implementação: documentação oficial de scipy.stats.spearmanr (permutação para amostras pequenas), scipy.stats.chi2_contingency e scipy.stats.kruskal. Links e instruções de reprodução estão no README da Parte 2.',True)
page()
heading('3. Resultados',True);heading('3.1. Bloco 1 — Descritivos')
table('Tabela 1A — Perfil dos óbitos por homicídio (n=1.107)',['Característica','n','%'],[
['Sexo: masculino','1.005','90,79'],['Sexo: feminino','101','9,12'],['Sexo: não informado','1','0,09'],
['Raça/cor: branca','24','2,17'],['Raça/cor: preta','10','0,90'],['Raça/cor: parda','1.057','95,48'],['Raça/cor: amarela','0','0,00'],['Raça/cor: indígena','4','0,36'],['Raça/cor: não informada','12','1,08'],
['Meio: arma de fogo','832','75,16'],['Meio: objeto cortante','132','11,92'],['Meio: outros','143','12,92']], [333,70,80])
para('Idade ao óbito: mediana de 28 anos; primeiro e terceiro quartis de 22 e 37 anos. Não houve idade ignorada entre os homicídios. O denominador de cada percentual da Tabela 1A é 1.107; diferenças residuais na soma decorrem do arredondamento.',True)
para('O perfil dos homicídios é predominantemente masculino e jovem, com forte presença de registros classificados como pardos. Armas de fogo respondem por aproximadamente três de cada quatro vítimas, o que torna esse grupo central para a comparação etária. A concentração racial entre as vítimas, isoladamente, não mede desigualdade de risco: é necessário confrontá-la com o grupo de comparação definido no enunciado e reconhecer que a base reúne somente pessoas que morreram.')
para('Na população geral, os 1.107 homicídios representam 4,83% dos 22.936 óbitos. O número de óbitos por qualquer causa na faixa de 15–29 anos, ambos os sexos, foi 1.365. Esses controles reproduzem a Parte 1 e ajudam a distinguir o universo total dos subconjuntos utilizados nas análises.')
page()
heading('3.1. Bloco 1 — Descritivos (continuação)',True)
desc=pd.read_csv(OUT/'tabelas/01_descritivos.csv')
rows=[]
for var,label in [('escolaridade','Escolaridade'),('local_obito','Local')]:
    for row in desc[desc.variavel.eq(var)].itertuples(): rows.append([label+': '+row.categoria,str(row.n),fmt(row.percentual_dos_homicidios)])
table('Tabela 1B — Escolaridade e local dos homicídios',['Característica','n','%'],rows,[333,70,80])
para('Entre os homicídios, 764 registros têm escolaridade até sete anos: 69,02% do total de vítimas ou 75,27% dos 1.015 registros com escolaridade conhecida. Os denominadores respondem a descrições diferentes e não devem ser misturados. O predomínio de baixa escolaridade descreve os falecidos; não estabelece o risco de quem tem determinada formação.')
para('A via pública é o local de ocorrência mais frequente. Esse campo informa onde ocorreu o óbito, não necessariamente onde houve a agressão: uma vítima pode receber atendimento e morrer no hospital. Portanto, a variável não permite reconstruir a dinâmica do crime ou a trajetória assistencial.')
para('A escolaridade esteve ausente em 4.867 óbitos da base geral (21,22%) e em 92 homicídios (8,31%). Raça/cor faltou em 627 óbitos gerais e em 12 homicídios. Não foi aplicada exclusão global por informação incompleta: cada bloco conserva os registros que podem contribuir para sua pergunta. A tabela de ausências por variável está disponível em CSV.')
page()
heading('3.2. Bloco 2 — Correlação ecológica',True)
item(1,'Escolha e pressupostos','A dispersão municipal foi examinada na Figura 1. As variáveis são proporções limitadas, com empates e heterogeneidade; escolheu-se Spearman para associação por postos, sem impor normalidade bivariada ou relação linear. Não se adotou Pearson apenas por ambas serem numéricas. Cada município contribui uma vez, sem ponderação por tamanho; a independência espacial não foi verificada, limitando a inferência.')
item(2,'Hipóteses','H₀: não há correlação monotônica (rho=0) entre a proporção municipal de homicídios e a proporção de escolaridade até sete anos entre registros conhecidos. H₁: rho≠0. Teste bilateral por permutação; a hipótese operacional de permutação é intercambiabilidade sob ausência de associação.')
item(3,'Significância','Adotou-se α=0,05.')
table('Tabela 2 — Correlação municipal (n=100)',['Medida','Resultado'],[
['Coeficiente de Spearman',fmt(e['rho'],4)],['IC95% bootstrap de pares',f"{fmt(e['ic95'][0],4)} a {fmt(e['ic95'][1],4)}"],['p bilateral por permutação',fmt(e['p'],5)],['p assintótico (suplementar)',fmt(e['p_assintotico'],5)],['rho² (descritivo de postos)',fmt(e['rho2'],4)],['Poder aproximado, efeito observado',fmt(e['poder']*100,2)+'%']], [320,163])
item(4,'Resultado','Obteve-se rho='+fmt(e['rho'],4)+'; IC95% '+fmt(e['ic95'][0],4)+' a '+fmt(e['ic95'][1],4)+'; p='+fmt(e['p'],5)+'. O coeficiente é a estatística principal e não tem graus de liberdade reportados; o p vem de 19.999 permutações, com correção (extremos+1)/(B+1).')
item(5,'Decisão','Rejeita-se H₀ porque o p bilateral é inferior a 0,05.')
item(6,'Conclusão contextual','Municípios com maior proporção de homicídios tenderam a apresentar menor proporção de escolaridade até sete anos entre os óbitos com campo conhecido. Isso não indica proteção da baixa escolaridade nem efeito da educação sobre a violência: são composições de óbitos municipais, influenciadas pela idade dos falecidos, pelas outras causas de morte e pela qualidade de preenchimento.')
page()
heading('3.2. Bloco 2 — Magnitude e sensibilidade',True)
figure('01_dispersao.png',480,270)
item(7,'Tamanho do efeito','A magnitude de |rho|=0,2535 é fraca/pequena, tomando 0,10, 0,30 e 0,50 como referências heurísticas. rho²=0,0643 é apenas o quadrado da correlação de postos: não representa 6,43% de risco explicado, efeito causal ou um R² de regressão das proporções originais.')
item(8,'Poder','A aproximação pela transformação de Fisher usa n=100 municípios, |rho| observado e α bilateral de 0,05: poder de '+fmt(e['poder']*100,2)+'%. É uma aproximação de planejamento aplicada ao efeito observado, não poder exato da permutação. Por depender do mesmo efeito, não valida o resultado de maneira independente nem resolve dependência espacial ou viés de seleção.')
para('A ausência municipal de escolaridade teve mediana de 17,73%, variando de 2,86% a 47,62%. Em análise de sensibilidade, dividindo os óbitos com escolaridade até sete anos por todos os óbitos, rho passou a −0,0385 (p assintótico=0,7034). Esse segundo indicador mistura escolaridade e completude; foi mantido apenas como contraste. A mudança mostra que a interpretação ecológica é sensível ao denominador e ao preenchimento, e não autoriza uma conclusão robusta sobre escolaridade individual.')
para('Os dois municípios abaixo de 30 óbitos representam 32 registros (0,14% da base). Eles não foram apagados das outras análises. O CSV municipal conserva os 102 códigos e a indicação de inclusão, tornando a seleção auditável.',True)
page()
heading('3.3. Bloco 3 — Associação raça/cor × homicídio',True)
item(1,'Escolha e pressupostos','Usou-se qui-quadrado de Pearson sem correção de Yates na tabela 2×2. Raça/cor e homicídio são variáveis nominais; os registros representam óbitos distintos. A menor frequência esperada foi '+fmt(a['esperada_min'],2)+', acima de cinco: não foi necessário substituir o teste pelo exato de Fisher. Não houve ajuste por município ou covariáveis.')
item(2,'Hipóteses','H₀: a proporção de homicídios entre os óbitos de homens de 15–29 anos é igual nos grupos negra e branca. H₁: as proporções diferem (alternativa não direcional; qui-quadrado usa a cauda superior).')
item(3,'Significância','Adotou-se α=0,05.')
table('Tabela 3 — Causa do óbito por grupo racial',['Raça/cor','Homicídio','Outras causas','Total','Homicídio (%)'],[
['Negra','546','496','1.042','52,40'],['Branca','8','54','62','12,90'],['Total','554','550','1.104','50,18']], [83,87,100,75,138])
item(4,'Resultado',f'χ²={fmt(a["chi2"],4)}; gl=1; p=1,516×10<super>−9</super>. Odds ratio negra/branca={fmt(a["odds_ratio"],2)}, IC95% {fmt(a["ic95"][0],2)}–{fmt(a["ic95"][1],2)}.')
item(5,'Decisão','Rejeita-se H₀, pois p&lt;0,05.')
item(6,'Conclusão contextual','Entre os homens jovens que morreram, os registros de raça/cor negra apresentaram maior proporção de homicídios que os brancos. A diferença foi de 39,50 pontos percentuais. A OR expressa a chance de homicídio versus outras causas entre os óbitos; não significa risco populacional 7,43 vezes maior e não mede o efeito causal da raça/cor.')
item(7,'Tamanho do efeito',f'Phi={fmt(a["phi"],4)} (V de Cramér na tabela 2×2), efeito pequeno pelas referências 0,10/0,30/0,50. A OR indica contraste expressivo, mas o IC amplo reflete, em especial, apenas oito homicídios no grupo branco. As duas medidas descrevem aspectos distintos da tabela.')
item(8,'Poder','Poder condicionado ao phi observado, pela distribuição qui-quadrado não central com gl=1 e n=1.104: '+fmt(a['poder']*100,3)+'%. A elevada sensibilidade estatística não elimina confundimento, diferença de composição etária dentro da faixa jovem ou erros de classificação racial.')
page()
heading('3.4. Bloco 4 — Idade segundo o meio empregado',True)
item(1,'Escolha e pressupostos','Compararam-se três grupos independentes, com idades em anos completos e muitos empates. Histogramas e boxplots indicam assimetria e caudas, sobretudo em arma de fogo. O teste de Brown–Forsythe (Levene centrado na mediana) indicou dispersões distintas: F='+fmt(c['levene_estatistica'],3)+'; gl=2 e 1.104; p&lt;0,001. Escolheu-se Kruskal–Wallis, corrigido por empates, em vez de ANOVA clássica. Não se interpreta o teste como comparação isolada de medianas, pois as formas e dispersões não são iguais.')
item(2,'Hipóteses','H₀: as distribuições de idade ao óbito são iguais entre arma de fogo, objeto cortante e outros. H₁: pelo menos uma difere; alternativa global não direcional, com estatística H avaliada na cauda superior.')
item(3,'Significância','Adotou-se α=0,05.')
comp=pd.read_csv(OUT/'tabelas/06_comparacao.csv')
table('Tabela 4 — Idade das vítimas por meio empregado',['Meio','n','Mediana (Q1–Q3)','Mín.–máx.'],[
[z.meio,str(z.n),f'{fmt(z.mediana,0)} ({fmt(z.q1,2)}–{fmt(z.q3,2)})',f'{int(z.min)}–{int(z.max)}'] for z in comp.itertuples()], [143,55,195,90])
item(4,'Resultado','H='+fmt(c['H'],4)+'; gl=2; p=4,339×10<super>−7</super>; n=1.107. Nenhuma vítima foi excluída por idade ou meio ausente.')
item(5,'Decisão','Rejeita-se H₀ porque p&lt;0,05.')
item(6,'Conclusão contextual','A idade das vítimas difere segundo o meio empregado, com menor mediana no grupo arma de fogo. A diferença descritiva entre arma de fogo e objeto cortante é de cinco anos. O teste global não identifica sozinho os pares distintos, nem demonstra que o meio empregado provoque uma mudança na idade das vítimas.')
item(7,'Tamanho do efeito','Épsilon quadrado=(H−k+1)/(N−k)='+fmt(c['epsilon2'],4)+'. Pela convenção heurística 0,01/0,06/0,14, o efeito global é pequeno. O resultado detectável não representa separação completa das distribuições, que se sobrepõem amplamente.')
item(8,'Poder','Poder aproximado de '+fmt(c['poder']*100,2)+'%, por ANOVA com f='+fmt(c['f_aproximado'],4)+' e n médio=369 por grupo. A aproximação ignora o desequilíbrio real (832/132/143), além da distribuição por postos: deve ser lida com cautela, sem substituir um planejamento prospectivo.')
page()
heading('3.4. Bloco 4 — Diagnósticos e comparação complementar',True)
figure('02_histogramas.png',480,200)
figure('03_boxplot.png',480,250)
para('O boxplot mostra sobreposição e idades extremas nos três grupos. No complemento exploratório, Mann–Whitney com Holm encontrou diferenças entre arma de fogo e objeto cortante (p ajustado&lt;0,001) e entre arma de fogo e outros (p ajustado=0,0037). Objeto cortante e outros não apresentaram evidência suficiente de diferença (p ajustado=0,1865). Este último resultado não prova equivalência entre os grupos; os testes pareados foram complementares e não substituem o teste global.')
para('Os três p-valores ajustados estão disponíveis em tabela CSV. As figuras exibem todas as vítimas com informação válida, não apenas os homens jovens do bloco racial. Quartis interpolados, como 25,75, resultam do método de cálculo e não de idades fracionárias registradas.',True)
page()
heading('4. Limitações',True)
para('Os dados de 2025 são preliminares e os resultados se referem estritamente à cópia de 23/09/2026. Sub-registro, causas mal definidas e eventos de intenção indeterminada podem ocultar agressões; a definição X85–Y09 não inclui toda a violência letal possível. A raça/cor é a registrada na declaração de óbito, sem garantia de autodeclaração, e o agrupamento preta+parda reduz detalhes. Escolaridade não foi informada em 4.867 dos 22.936 registros (21,22%); por isso, o indicador municipal depende da completude. A forte mudança da correlação na sensibilidade ao denominador reforça essa limitação. Foram excluídos apenas do contraste racial 20 de 1.124 homens jovens (1,78%): 14 sem raça/cor, um amarelo e cinco indígenas. Apenas do bloco ecológico, dois municípios com menos de 30 óbitos ficaram fora. Não se verificou autocorrelação espacial, e a correlação não foi ponderada pela precisão desigual dos municípios. No grupo branco houve somente oito homicídios, produzindo intervalo de confiança amplo para a OR.')
para('O SIM registra falecidos, sem denominador de pessoas vivas: não é possível calcular incidência, risco populacional ou taxa de homicídio. A associação racial é bruta, sem controle de condições socioeconômicas, município ou composição etária residual; o desenho não demonstra causalidade ou mecanismos de discriminação. O bloco ecológico não permite extrapolar relações municipais para indivíduos, sob risco de falácia ecológica, nem concluir que escolaridade proteja ou cause homicídios. Os testes inferenciais pressupõem um processo gerador além da cópia completa dos óbitos observados: não representam incerteza de uma amostra aleatória de residentes. O poder pós-hoc calculado a partir dos efeitos observados é aproximado e não valida os achados de modo independente. Os três testes principais foram avaliados a 5% sem ajuste conjunto, de modo que o conjunto tem maior probabilidade de falso positivo do que um teste isolado; Holm foi aplicado apenas aos pares etários. Assim, os resultados são associações exploratórias nesta UF e ano, sem generalização automática. A versão R anexada precisa de execução local; a versão Python que originou os números foi executada e conferida.')
para('Rastreabilidade: tabelas completas, gráficos, resultados.json, versões das bibliotecas e hash SHA-256 da base tratada acompanham o repositório. O README explica a reprodução e identifica o uso de inteligência artificial. Não houve substituição do arquivo original nem publicação no GitHub durante a preparação.',True)

# A seção Anexo inicia somente após as dez páginas do corpo principal.
page();heading('5. Anexo — Código completo e comentado',True)
para('A seguir, versão R para conferência e execução local. O arquivo .R também acompanha a entrega separadamente. A versão Python executada está em parte2/analisar.py; a formatação do PDF está em parte2/gerar_relatorio.py. A versão R usa os mesmos dados e definições, mas sementes iguais em linguagens distintas não produzem as mesmas permutações: p-valores Monte Carlo e intervalos bootstrap podem variar ligeiramente.',True)
code=(ROOT/'entrega/Parte2_Gabriel_Hadassah_Ruanytha.R').read_text(encoding='utf-8')
import textwrap
cs=ParagraphStyle(name='CodigoBio',fontName='Courier',fontSize=7.1,leading=9)
for line in code.splitlines():
    for wrapped in textwrap.wrap(line,width=95,replace_whitespace=False,drop_whitespace=False) or [' ']:
        story.append(Preformatted(wrapped,cs))

def footer(can,doc):
    can.setStrokeColor(colors.HexColor('#147d92'));can.line(48,44,A4[0]-48,44)
    can.setFont('ArialBio',8);can.setFillColor(colors.HexColor('#455566'))
    can.drawString(48,30,'Bioestatística | AL, 2025 | Gabriel · Hadassah · Ruanytha')
    can.drawRightString(A4[0]-48,30,str(doc.page))

pdf=ROOT/'entrega/Parte2_Gabriel_Hadassah_Ruanytha.pdf'
doc=SimpleDocTemplate(str(pdf),pagesize=A4,leftMargin=56,rightMargin=56,topMargin=48,bottomMargin=59,title='Homicídios, juventude e raça/cor - Parte 2',author='Gabriel Martins; Hadassah Teodoro; Ruanytha Miranda')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
(OUT/'RELATORIO.md').write_text('\n\n'.join(md[:md.index('\n# 5. Anexo — Código completo e comentado')]) if '\n# 5. Anexo — Código completo e comentado' in md else '\n\n'.join(md),encoding='utf-8')
print(pdf)
