# Nome(s): Gabriel Martins, Hadassah Teodoro e Ruanytha Miranda
# Matrículas: d202510498, d202520450 e d202520419 | Enunciado nº 2
# DECLARAÇÃO DE USO DE INTELIGÊNCIA ARTIFICIAL
# Usei ferramenta de IA? ( ) Não (X) Sim. Ferramenta: ChatGPT/Codex.
# Uso: elaboração e execução da análise, revisão estatística e redação do relatório.
# Pedido: continuar a Parte 1 com os quatro blocos exigidos na Parte 2.
# Correções assistidas: denominadores da escolaridade, teste de permutação,
# distinção entre chance entre óbitos e risco populacional; poder aproximado.
# Os integrantes devem revisar as interpretações e confirmar sua compreensão
# oral do código antes da entrega. Não se declara uma revisão pessoal não realizada.
"""Executar da raiz: python parte2/analisar.py. Não baixa nem altera a Parte 1."""
from pathlib import Path
import hashlib, json, platform
import numpy as np
import pandas as pd
import scipy
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'parte2'
for folder in ['tabelas', 'graficos']:
    (OUT / folder).mkdir(exist_ok=True)
ALPHA = .05
SEED = 20261123
SOURCE = ROOT / 'dados/DOAL2025_tratado.csv'
d = pd.read_csv(SOURCE, dtype={'CODMUNRES': str, 'ESC': str, 'RACACOR': str})
d['homicidio'] = d.homicidio.astype(str).str.lower().map({'true': True, 'false': False})
assert d.homicidio.notna().all()
d['homicidio'] = d.homicidio.astype(bool)
assert len(d) == 22936 and d.homicidio.sum() == 1107
assert d.CODMUNRES.str.fullmatch(r'27\d{4}').all()
assert pd.to_datetime(d.DTOBITO.astype(str).str.zfill(8), format='%d%m%Y').dt.year.eq(2025).all()
assert pd.to_numeric(d.TIPOBITO).eq(2).all()
h = d[d.homicidio].copy()
j = d[d.sexo.eq('Masculino') & d.idade_anos.between(15,29)].copy()
a = j[j.raca_grupo.isin(['Negra','Branca'])].copy()
assert len(j) == 1124 and len(a) == 1104

def save(df, name):
    df.to_csv(OUT/'tabelas'/name, index=False, encoding='utf-8-sig', float_format='%.10g')

# Bloco 1: não excluir todos os registros com qualquer ausência.
# Cada variável tem seu denominador; ausências aparecem como categoria descritiva.
rows=[]
for col in ['sexo','raca','escolaridade','local_obito']:
    for label,n in h[col].fillna('Não informado').value_counts().items():
        rows.append([col,label,int(n),100*n/len(h)])
save(pd.DataFrame(rows,columns=['variavel','categoria','n','percentual_dos_homicidios']), '01_descritivos.csv')
missing = pd.DataFrame({'variavel':['idade_anos','sexo','raca','raca_grupo','escolaridade','local_obito']})
missing['ausentes_base']=[int(d[c].isna().sum()) for c in missing.variavel]
missing['ausentes_homicidios']=[int(h[c].isna().sum()) for c in missing.variavel]
save(missing,'02_ausencias.csv')

# Bloco 2: unidade = MUNICÍPIO, todas as idades e ambos os sexos.
# Até 7 anos = ESC 1,2,3; 9/em branco não são baixa escolaridade.
# Não usamos todos os óbitos como denominador escolar principal: isso trataria
# escolaridade ignorada como se fosse escolaridade maior que 7 anos.
d['esc_conhecida']=d.ESC.isin(['1','2','3','4','5'])
d['esc_ate7']=d.ESC.isin(['1','2','3'])
mun=d.groupby('CODMUNRES').agg(obitos=('homicidio','size'),homicidios=('homicidio','sum'),esc_conhecida=('esc_conhecida','sum'),esc_ate7=('esc_ate7','sum')).reset_index()
mun['pct_homicidios']=100*mun.homicidios/mun.obitos
mun['pct_esc_ate7']=100*mun.esc_ate7/mun.esc_conhecida.replace(0,np.nan)
mun['pct_esc_ausente']=100*(mun.obitos-mun.esc_conhecida)/mun.obitos
mun['pct_esc_ate7_total']=100*mun.esc_ate7/mun.obitos
mun['incluido']=mun.obitos.ge(30)&mun.pct_esc_ate7.notna()
save(mun,'03_municipios.csv')
eco=mun[mun.incluido]
x,y=eco.pct_homicidios.to_numpy(),eco.pct_esc_ate7.to_numpy()
rho, p_asym=stats.spearmanr(x,y)
# Como n municipal é <500, p principal por permutação bilateral de |rho|.
# Postos calculados uma vez; permutamos apenas os postos de y, preservando empates.
rx=stats.rankdata(x); ry=stats.rankdata(y)
rx=rx-rx.mean(); ry=ry-ry.mean(); denom=np.linalg.norm(rx)*np.linalg.norm(ry)
rng=np.random.default_rng(SEED); B=19999
extreme=sum(abs(np.dot(rx,rng.permutation(ry))/denom)>=abs(rho)-1e-12 for _ in range(B))
p_perm=(extreme+1)/(B+1)
# IC descritivo bootstrap de pares municipais, não intervalo de risco individual.
boot=[]
for _ in range(5000):
    ix=rng.integers(0,len(x),len(x)); boot.append(stats.spearmanr(x[ix],y[ix]).statistic)
ci_rho=np.nanquantile(boot,[.025,.975])
# Poder aproximado pela transformação z de Fisher; não é poder exato do teste
# de postos/permutação. Calculado com n municípios e efeito observado.
zcrit=stats.norm.ppf(1-ALPHA/2)
mu=np.sqrt(len(x)-3)*np.arctanh(abs(rho))
power_r=float(stats.norm.sf(zcrit-mu)+stats.norm.cdf(-zcrit-mu))
sensitivity=stats.spearmanr(x,eco.pct_esc_ate7_total)

# Bloco 3: matriz com exposição nas linhas, desfecho nas colunas.
tab=pd.crosstab(a.raca_grupo,a.homicidio).reindex(index=['Negra','Branca'],columns=[True,False],fill_value=0)
chi,p_chi,df_chi,exp=stats.chi2_contingency(tab,correction=False)
assert exp.min()>=5
aa,bb,cc,dd=tab.to_numpy().ravel()
odds=aa*dd/(bb*cc); se=np.sqrt(1/aa+1/bb+1/cc+1/dd)
ci_or=np.exp(np.log(odds)+np.array([-1,1])*zcrit*se)
phi=np.sqrt(chi/len(a))
power_chi=stats.ncx2.sf(stats.chi2.ppf(.95,1),1,len(a)*phi**2)
assoc=tab.rename(columns={True:'homicidio',False:'outras_causas'}).reset_index()
assoc['total']=assoc.homicidio+assoc.outras_causas
assoc['pct_homicidios']=100*assoc.homicidio/assoc.total
save(assoc,'04_associacao.csv')
save(pd.DataFrame(exp,index=['Negra','Branca'],columns=['homicidio','outras_causas']).reset_index(names='raca_grupo'),'05_frequencias_esperadas.csv')

# Bloco 4: TODAS as vítimas; não limitar aos homens jovens do bloco anterior.
means=['Arma de fogo','Objeto cortante','Outros']
hc=h.dropna(subset=['idade_anos','meio'])
groups=[hc.loc[hc.meio.eq(m),'idade_anos'].to_numpy() for m in means]
H,p_kw=stats.kruskal(*groups)
N=sum(map(len,groups)); k=len(groups)
epsilon=max(0,(H-k+1)/(N-k))
f=np.sqrt(epsilon/(1-epsilon))
# Aproximação ANOVA equilibrada, n médio=N/k. Grupos reais são desiguais.
power_kw=stats.ncf.sf(stats.f.ppf(.95,k-1,N-k),k-1,N-k,N*f*f) if f>0 else .05
lev=stats.levene(*groups,center='median')
comp=[]
for m,g in zip(means,groups):
    comp.append([m,len(g),np.median(g),*np.quantile(g,[.25,.75]),np.mean(g),np.std(g,ddof=1),min(g),max(g),stats.skew(g,bias=False)])
save(pd.DataFrame(comp,columns=['meio','n','mediana','q1','q3','media','dp','min','max','assimetria']), '06_comparacao.csv')
# Comparações exploratórias Mann-Whitney com Holm, após o teste global.
post=[]
for i in range(k):
    for jj in range(i+1,k):
        res=stats.mannwhitneyu(groups[i],groups[jj],alternative='two-sided',method='asymptotic')
        post.append(dict(grupo1=means[i],grupo2=means[jj],U=float(res.statistic),p=float(res.pvalue)))
order=np.argsort([r['p'] for r in post]); prev=0
for rank,idx in enumerate(order):
    prev=max(prev,min(1,(len(post)-rank)*post[idx]['p'])); post[idx]['p_holm']=prev
save(pd.DataFrame(post),'07_pos_teste_holm.csv')

# Gráficos com títulos, unidades, denominadores e fonte, antes da interpretação.
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
source='Fonte: SIM/DATASUS | AL, 2025 (preliminar) | cópia de 23/09/2026'
fig,ax=plt.subplots(figsize=(8,4.5))
ax.scatter(x,y,c='#147d92',s=38,alpha=.8)
ax.set(xlabel='Homicídios entre todos os óbitos do município (%)',ylabel='Até 7 anos entre escolaridades conhecidas (%)',title=f'Correlação ecológica - {len(eco)} municípios com pelo menos 30 óbitos')
fig.text(.08,.01,source,fontsize=8);fig.tight_layout(rect=(0,.04,1,1));fig.savefig(OUT/'graficos/01_dispersao.png',dpi=200);plt.close(fig)
fig,axes=plt.subplots(1,3,figsize=(9,3.8),sharex=True)
for ax,m,g in zip(axes,means,groups):
    ax.hist(g,bins=np.arange(0,111,5),color='#147d92',edgecolor='white');ax.set(title=f'{m} (n={len(g)})',xlabel='Idade em anos completos',ylabel='Óbitos')
fig.suptitle('Distribuição da idade das vítimas por meio empregado');fig.text(.04,.01,source,fontsize=8)
fig.tight_layout(rect=(0,.05,1,.92));fig.savefig(OUT/'graficos/02_histogramas.png',dpi=200);plt.close(fig)
fig,ax=plt.subplots(figsize=(8,4.5));ax.boxplot(groups,tick_labels=means,patch_artist=True,boxprops={'facecolor':'#b5dbe1'})
ax.set(ylabel='Idade ao óbito (anos completos)',title='Idade ao óbito por homicídio segundo o meio empregado')
fig.text(.08,.01,source,fontsize=8);fig.tight_layout(rect=(0,.04,1,1));fig.savefig(OUT/'graficos/03_boxplot.png',dpi=200);plt.close(fig)

results=dict(n_base=len(d),n_homicidios=len(h),n_jovens=len(j),n_associacao=len(a),
 controles=dict(jovens_ambos_sexos=int(d.idade_anos.between(15,29).sum()),arma_fogo=int(h.meio.eq('Arma de fogo').sum()),raca_ausente_homicidios=int(h.raca.isna().sum())),
 idade_homicidios=dict(n=int(h.idade_anos.count()),mediana=float(h.idade_anos.median()),q1=float(h.idade_anos.quantile(.25)),q3=float(h.idade_anos.quantile(.75))),
 ecologica=dict(n=len(eco),municipios_total=len(mun),municipios_excluidos=int((~mun.incluido).sum()),obitos_excluidos=int(mun.loc[~mun.incluido,'obitos'].sum()),rho=float(rho),rho2=float(rho*rho),p=float(p_perm),p_assintotico=float(p_asym),ic95=list(map(float,ci_rho)),poder=power_r,permutacoes=B,bootstrap=5000,rho_sensibilidade=float(sensitivity.statistic),p_sensibilidade_assintotico=float(sensitivity.pvalue),mediana_ausencia_esc=float(eco.pct_esc_ausente.median()),min_ausencia_esc=float(eco.pct_esc_ausente.min()),max_ausencia_esc=float(eco.pct_esc_ausente.max())),
 associacao=dict(chi2=float(chi),gl=int(df_chi),p=float(p_chi),esperada_min=float(exp.min()),phi=float(phi),odds_ratio=float(odds),ic95=list(map(float,ci_or)),poder=float(power_chi),exclusoes_raca=int(j.raca.isna().sum()),exclusoes_amarela=int(j.raca.eq('Amarela').sum()),exclusoes_indigena=int(j.raca.eq('Indígena').sum())),
 comparacao=dict(H=float(H),gl=k-1,p=float(p_kw),epsilon2=float(epsilon),f_aproximado=float(f),poder=float(power_kw),n=N,excluidos=len(h)-N,levene_estatistica=float(lev.statistic),levene_p=float(lev.pvalue)),
 ambiente=dict(python=platform.python_version(),pandas=pd.__version__,numpy=np.__version__,scipy=scipy.__version__,matplotlib=matplotlib.__version__),
 sha256_tratado=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),semente=SEED)
(OUT/'resultados.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(results,ensure_ascii=False,indent=2))
# Diário de erros reais desta continuação:
# 1. Conferência de dependências: scipy e matplotlib ausentes no runtime.
#    Solução: instalação em diretório isolado, sem modificar os dados originais.
# 2. pip: NameResolutionError para pypi.org no ambiente restrito.
#    Solução: repetição do download com a permissão de rede apropriada.
# Erros históricos da Parte 1 permanecem em python/09_limitacoes_e_erros.py.
