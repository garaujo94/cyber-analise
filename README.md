# cyber-analise

## Conteúdo
* [Objetivo](#objetivo)
* [Funções prontas](#funções-prontas)
* [A desenvolver](#a-desenvolver)

## Objetivo

Analisar os documentos produzidos pelo Estado Americano sobre Defesa Nacional, a fim de ver se há alguma correlação entre a quantidade de vezes que os termos relativos a cyber security aparecem é proporcional ao gastos publicos no mesmo setor.

## Funções Prontas
1. Leitura de todos os documentos .pdf disponíveis.
2. Análise de conjunto completo de todos os documentos, fazendo contagem de palavras, bigramas e trigramas, plotando essa frequência e suas WordClouds.
3. Função relatório para 1 ano que é especificado como parâmetro na função. O relatório devolve um Pandas DataFrame com a incidência de cada palavra em ordem decrescente, a sua porcentagem frente as outras palavras e uma WordCloud que já é salva automaticamente na pasta raiz discriminando o ano.

## A Desenvolver
1. Aprimorar função de relatório anual que também trabalhe com bigramas e trigramas.
2. Plotar a frequência numa linha do tempo.

![Test Image 1](https://github.com/garaujo94/cyber-analise/blob/master/wordcloud.png)
