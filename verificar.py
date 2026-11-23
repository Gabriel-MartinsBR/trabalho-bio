"""Auditoria independente: refaz seleções do CSV original e fórmulas de postos."""
from pathlib import Path
import hashlib,json
import numpy as np
import pandas as pd
from scipy import stats
R=Path(__file__).resolve().parents[1]
r=json.loads((R/'parte2/resultados.json').read_text(encoding='utf-8'))
d=pd.read_csv(R/'dados/DOAL2025.csv',dtype=str)
assert d.shape==(22936,87)
cid=d.CAUSABAS.str.replace('.','',regex=False).str[:3]
h=cid.between('X85','X99') | cid.between('Y00','Y09')
unit=d.IDADE.str[0];value=pd.to_numeric(d.IDADE.str[1:],errors='coerce')
age=pd.Series(np.nan,index=d.index)
age[unit.isin(list('0123'))]=0
age[unit.eq('4')]=value
age[unit.eq('5')]=100+value
assert (int(h.sum()),int(age.between(15,29).sum()),int((h&cid.isin(['X93','X94','X95'])).sum()),int((h&d.RACACOR.isna()).sum()))==(1107,1365,832,12)
sel=d.SEXO.eq('1')&age.between(15,29)&d.RACACOR.isin(['1','2','4'])
assert sel.sum()==1104
mat=np.array([[int((sel&d.RACACOR.isin(['2','4'])&h).sum()),int((sel&d.RACACOR.isin(['2','4'])&~h).sum())],
              [int((sel&d.RACACOR.eq('1')&h).sum()),int((sel&d.RACACOR.eq('1')&~h).sum())]])
assert np.array_equal(mat,[[546,496],[8,54]])
expected=mat.sum(1)[:,None]*mat.sum(0)[None,:]/mat.sum()
chi=((mat-expected)**2/expected).sum()
assert np.isclose(chi,r['associacao']['chi2'])
groups=[age[h&cid.isin(['X93','X94','X95'])].to_numpy(),age[h&cid.eq('X99')].to_numpy(),age[h&~cid.isin(['X93','X94','X95','X99'])].to_numpy()]
pooled=np.concatenate(groups);ranks=stats.rankdata(pooled);N=len(pooled)
splits=np.split(ranks,np.cumsum([len(g) for g in groups])[:-1])
H=12/(N*(N+1))*sum(rr.sum()**2/len(rr) for rr in splits)-3*(N+1)
_,cnt=np.unique(pooled,return_counts=True)
H/=1-sum(cnt**3-cnt)/(N**3-N)
assert np.isclose(H,r['comparacao']['H'])
treated=R/'dados/DOAL2025_tratado.csv'
assert hashlib.sha256(treated.read_bytes()).hexdigest()==r['sha256_tratado']
t=pd.read_csv(treated)
assert np.allclose(age,t.idade_anos,equal_nan=True)
assert np.array_equal(h,t.homicidio)
mun=pd.read_csv(R/'parte2/tabelas/03_municipios.csv')
assert len(mun)==102 and mun.incluido.sum()==100
assert mun.loc[~mun.incluido,'obitos'].sum()==32
text='''VERIFICAÇÃO CONCLUÍDA
CSV original: 22.936 linhas x 87 colunas.
Idade e homicídio reconstruídos do original coincidem com a Parte 1.
Controles: 1.107 homicídios; 1.365 jovens; 832 armas de fogo; 12 raças ausentes.
Tabela racial refeita do original: [[546,496],[8,54]], n=1.104.
Qui-quadrado conferido pela fórmula das frequências esperadas.
Kruskal-Wallis conferido pela soma dos postos com correção de empates.
102 municípios; 100 incluídos; 32 óbitos em dois municípios excluídos.
Hash SHA-256 da base tratada confirmado.
Versão R: não executada neste ambiente; pendente validação em R.
'''
(R/'parte2/verificacao.txt').write_text(text,encoding='utf-8')
print(text)
