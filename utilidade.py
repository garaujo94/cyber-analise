from PyPDF2 import PdfFileReader
import pandas as pd
import os
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter

def ler_arquivo(arquivo): #Essa versão é a que está valendo
    pdf = open(arquivo, "rb")
    reader = PdfFileReader(pdf)
    tamanho = reader.numPages
    
    pages = []
    
    for i in range(tamanho):
        pages.append(reader.getPage(i).extractText())
        
    text = " ".join(pages)
    
    return text


def ler_todos_arquivos(local = 'textos'):
    
    textos = os.listdir(local)
    ano = []
    text = []
    
    for texto in textos:
        ano.append(texto[:4])
        text.append(ler_arquivo('textos/'+texto))
    
    df = pd.DataFrame(text, columns=['text'], index=ano)
    print(df.head())
    
    return df

def get_top_text_ngrams(corpus, g, stopwords):
    ''' 
    Corpus: texto a ser analisado
    g: Quantidade de palavras por grupo (palavras soltas, bigrams, trigrams)
    '''
    vec = CountVectorizer(ngram_range=(g, g), stop_words=stopwords).fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq = sorted(words_freq, key = lambda x: x[1], reverse=True)

    return dict(words_freq)

def plota_frequencia_dict(most_common, salvar = 0):
    '''
    Plota um gráfico de barra mostrando a frequência das palavras a partir de um dicionário.
    Para salvar o gráfico criado, definir "salvar = 1"
    '''
    plt.figure(figsize = (16,9))
    sns.barplot(x=list(most_common.values())[:30],y=list(most_common.keys())[:30])
    plt.title('30 palavras mais comuns')
    if salvar == 1:
        plt.savefig('barra1.png')
    plt.show()

def plota_wordcloud(dicionario, stop, salvar = 0):
    plt.figure(figsize = (20,20))
    wc = WordCloud(max_words = 2000 , width = 1600 , height = 800 , stopwords = stop).fit_words(dicionario)
    plt.imshow(wc , interpolation = 'bilinear')
    if salvar == 1:
        plt.savefig('worldAll1')
    plt.show()

def analise_anos(df, tipo=1, gerar_wordcloud = 0):
    '''
    df -> dataframe onde está o texto tratado
    tipo -> palavras normais, bigrams ou trigrams
    '''
    padrao = {
        1: 'tokens_lemma',
        2: 'bi_gram',
        3: 'tri_gram'
    }
    r = pd.DataFrame()
    for i in df.index:
        # Converte a lista em um dicionário com contagem de valores
        word_counts = Counter(df[padrao[tipo]][i])
        b = word_counts
        a = word_counts


        # Inverter a chave / valores no dicionário para classificarReverter a chave / valores no dicionário para classificar
        word_counts = list(zip(word_counts.values(), word_counts.keys()))

        # Classifique a lista por contagem
        word_counts = sorted(word_counts, reverse=True)

        # Imprime as 20 palavras mais comuns
        print(word_counts[:20])


        #Fazendo relatório
        b = list(zip(b.keys(), b.values()))
        b = sorted(b, reverse=True, key = lambda x: x[1])
        relatorio = pd.DataFrame(data = dict(b).values(), index = dict(b).keys(), columns = ['quantidade'])
        total_de_palavras = relatorio.quantidade.sum()
        porcentagem = relatorio.quantidade / relatorio.quantidade.sum()
        print(relatorio.head())
        print('---------')
        print(porcentagem.head())
        result = pd.concat([relatorio, porcentagem.to_frame('porcentagem')], axis=1, sort=False)
        result = result.assign(Group=i)
        
        r = pd.concat([r, result])
    
        if gerar_wordcloud == 1:
            nome = 'wordcloud'+i+'.png'    
            wordcloud = WordCloud(width=1600, height=800, max_font_size=200).fit_words(a) # o 'a' veio de um counter
            plt.figure(figsize=(16,13))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.savefig(nome)
            plt.show()
        
    r["quantidade"] = pd.to_numeric(r["quantidade"], downcast="float")
    return r

def faz_analise(df, tema = 'cyber'):
    print(df.filter(like=tema, axis=0))
    analise = df.filter(like=tema, axis=0).groupby('Group',).sum()
    analise.reset_index(inplace = True)
    analise['assunto'] = tema
    
    return analise

def plota_analise(df, tipo=['porcentagem', 'quantidade'], graf=['barra', 'linha']):

    sns.set_palette("Dark2_r")
    sns.set_style("darkgrid")

    plt.figure(figsize=(14,8))

    if graf == 'barra':
        ax = sns.barplot(data=df, x="Group", y=tipo,
                     palette="Blues_d", hue = 'assunto')
    else:
        ax = sns.lineplot(data=df, x="Group", y=tipo, hue = 'assunto')
    plt.title('Evolução de '+tipo+' por ano')
    plt.savefig('evolucao_'+tipo+'_por_ano_barra.png')
    plt.show()