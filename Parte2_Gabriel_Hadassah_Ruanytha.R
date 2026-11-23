# Nome(s): Gabriel Martins, Hadassah Teodoro e Ruanytha Miranda
# Matrículas: d202510498, d202520450 e d202520419 | Enunciado n: 2
# DECLARAÇÃO DE USO DE INTELIGÊNCIA ARTIFICIAL
# Usei ferramenta de IA? ( ) Não (X) Sim. ChatGPT/Codex.
# Uso: geração desta versão R a partir da análise Python executada.
# Pedido: elaborar a Parte 2 com os dados preservados da Parte 1.
# Correções assistidas: denominadores, interpretação não causal e poder aproximado.
# Esta versão R NÃO foi executada no ambiente de preparação (R indisponível).
# Antes da entrega: executar no R e os integrantes confirmarem compreensão oral.
# Não se declara revisão pessoal dos integrantes ainda não realizada.
# Execute na raiz do repositório: Rscript entrega/Parte2_Gabriel_Hadassah_Ruanytha.R
# Pacotes: somente base/stats/graphics/utils, incluídos na instalação do R.

args <- commandArgs(trailingOnly = FALSE)
argfile <- grep('^--file=', args, value = TRUE)
if (length(argfile)) {
  root <- dirname(dirname(normalizePath(sub('^--file=', '', argfile[1]))))
} else {
  root <- getwd() # No RStudio, abrir a raiz do projeto como diretório de trabalho.
}
out <- file.path(root, 'parte2', 'validacao_R')
dir.create(out, recursive = TRUE, showWarnings = FALSE)
sink(file.path(out, 'saida_R.txt'), split = TRUE)
d <- read.csv(file.path(root, 'dados', 'DOAL2025_tratado.csv'),
              colClasses = 'character', na.strings = c('', 'NA'),
              fileEncoding = 'UTF-8-BOM', check.names = FALSE)
d$idade_anos <- as.numeric(d$idade_anos)
d$homicidio <- tolower(d$homicidio) == 'true'
stopifnot(nrow(d) == 22936, sum(d$homicidio) == 1107,
          all(grepl('^27[0-9]{4}$', d$CODMUNRES)),
          all(format(as.Date(d$DTOBITO, '%d%m%Y'), '%Y') == '2025'),
          all(d$TIPOBITO == '2'))
h <- d[d$homicidio, ]
j <- d[!is.na(d$sexo) & d$sexo == 'Masculino' &
         !is.na(d$idade_anos) & d$idade_anos >= 15 & d$idade_anos <= 29, ]
a <- j[j$raca_grupo %in% c('Negra', 'Branca'), ]
stopifnot(nrow(j) == 1124, nrow(a) == 1104)
alpha <- .05
set.seed(20261123)

# 1. Descritivos: ausências não retiram pessoas de todos os blocos.
for (v in c('sexo', 'raca', 'escolaridade', 'local_obito')) {
  t <- table(h[[v]], useNA = 'always')
  print(v); print(cbind(n = t, percentual = 100 * t/nrow(h)))
}
print(quantile(h$idade_anos, c(.25, .5, .75), na.rm = TRUE))
print(sapply(d[c('idade_anos','sexo','raca','escolaridade','local_obito')], function(z) sum(is.na(z))))

# 2. Município é a unidade de correlação, sem restringir a homens jovens.
# ESC 1/2/3 = nenhuma, 1-3 e 4-7 anos; desconhecido não vira 'mais de 7'.
d$esc_conhecida <- as.integer(d$ESC %in% as.character(1:5))
d$esc_ate7 <- as.integer(d$ESC %in% as.character(1:3))
d$obitos <- 1L
m <- aggregate(d[c('obitos','homicidio','esc_conhecida','esc_ate7')],
               by = list(CODMUNRES = d$CODMUNRES), FUN = sum)
m$pct_homicidios <- 100*m$homicidio/m$obitos
m$pct_esc_ate7 <- 100*m$esc_ate7/m$esc_conhecida
m$pct_esc_ausente <- 100*(m$obitos-m$esc_conhecida)/m$obitos
e <- m[m$obitos >= 30 & is.finite(m$pct_esc_ate7), ]
write.csv(m, file.path(out, 'municipios_R.csv'), row.names = FALSE)
x <- e$pct_homicidios; y <- e$pct_esc_ate7
rho <- cor(x, y, method = 'spearman')
# Alternativa rejeitada: Pearson assume associação linear; proporções e postos
# permitem escolher Spearman. Dispersão deve ser inspecionada antes de concluir.
# p bilateral por 19.999 permutações, preservando empates e n municípios.
rx <- rank(x); ry <- rank(y); B <- 19999L
perm <- replicate(B, cor(rx, sample(ry)))
p_perm <- (1+sum(abs(perm) >= abs(rho)-1e-12))/(B+1)
boot <- replicate(5000, {
  ix <- sample.int(length(x), replace = TRUE)
  cor(x[ix], y[ix], method = 'spearman')
})
ic <- quantile(boot, c(.025,.975), na.rm = TRUE)
mu <- sqrt(length(x)-3)*atanh(abs(rho)); z <- qnorm(.975)
power_r <- pnorm(mu-z)+pnorm(-z-mu)
print(c(n_municipios=nrow(e), rho=rho, rho2=rho^2, p=p_perm,
        IC_inf=ic[1], IC_sup=ic[2], poder_aproximado=power_r))
print(cor.test(x, 100*e$esc_ate7/e$obitos, method='spearman', exact=FALSE))
png(file.path(out, 'dispersao_R.png'), width=1600, height=1000, res=180)
plot(x,y,pch=19,col='#147d92',xlab='Homicidios entre todos os obitos (%)',
     ylab='Ate 7 anos entre escolaridades conhecidas (%)',main='Correlacao municipal - AL, 2025')
mtext('Fonte: SIM/DATASUS; copia de 23/09/2026',side=1,line=3.5,cex=.7)
dev.off()

# 3. Comparação racial entre óbitos de homens de 15-29 anos, não entre vivos.
tab <- table(factor(a$raca_grupo, levels=c('Negra','Branca')),
             factor(a$homicidio, levels=c(TRUE,FALSE)))
ct <- chisq.test(tab, correct=FALSE)
stopifnot(min(ct$expected) >= 5)
phi <- sqrt(unname(ct$statistic)/sum(tab))
OR <- tab[1,1]*tab[2,2]/(tab[1,2]*tab[2,1])
se <- sqrt(sum(1/tab)); ci_or <- exp(log(OR)+c(-1,1)*z*se)
power_chi <- pchisq(qchisq(.95,1),df=1,ncp=sum(tab)*phi^2,lower.tail=FALSE)
print(tab); print(ct); print(ct$expected)
print(c(phi=phi, OR=OR, IC_inf=ci_or[1], IC_sup=ci_or[2], poder=power_chi))
write.csv(as.data.frame.matrix(tab),file.path(out,'associacao_R.csv'))

# 4. Três meios independentes, todas as vítimas de homicídio com idade conhecida.
# Não usar três testes t sem controle de multiplicidade; teste global por postos.
hc <- h[!is.na(h$idade_anos) & !is.na(h$meio), ]
hc$meio <- factor(hc$meio, levels=c('Arma de fogo','Objeto cortante','Outros'))
print(tapply(hc$idade_anos,hc$meio,quantile,probs=c(.25,.5,.75)))
kw <- kruskal.test(idade_anos~meio,data=hc)
N <- nrow(hc); k <- nlevels(hc$meio)
eps <- max(0,(unname(kw$statistic)-k+1)/(N-k))
f <- sqrt(eps/(1-eps))
power_kw <- if (f>0) pf(qf(.95,k-1,N-k),k-1,N-k,ncp=N*f^2,lower.tail=FALSE) else .05
# Aproximação ANOVA com alocação equilibrada média, não poder exato do KW.
print(kw); print(c(epsilon2=eps, f_aproximado=f, poder_aproximado=power_kw))
# Brown-Forsythe: ANOVA sobre desvios absolutos da mediana de cada grupo.
hc$desvio <- abs(hc$idade_anos-ave(hc$idade_anos,hc$meio,FUN=median))
print(summary(aov(desvio~meio,data=hc)))
print(pairwise.wilcox.test(hc$idade_anos,hc$meio,p.adjust.method='holm',exact=FALSE))
png(file.path(out,'boxplot_R.png'),width=1600,height=1000,res=180)
boxplot(idade_anos~meio,data=hc,col='#b5dbe1',ylab='Idade ao obito (anos completos)',
        main='Homicidios segundo meio empregado - AL, 2025')
mtext('Fonte: SIM/DATASUS; copia de 23/09/2026',side=1,line=3.5,cex=.7)
dev.off()
print(sessionInfo())
sink()
# Diário de erros REAIS da continuação, registrados na execução Python:
# 1. SciPy/Matplotlib ausentes: instaladas dependências isoladas.
# 2. pip com NameResolutionError: download repetido com permissão de rede.
# Não foram inventados erros de console R: esta versão ainda precisa ser executada.
