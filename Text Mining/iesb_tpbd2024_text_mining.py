# -*- coding: utf-8 -*-
"""iesb_tpbd2024_text_mining.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1dn-BMDr2S9XYH8QRfXmmh35_ZDKgQtk1
"""

# instalação dos pacotes necessários

!pip install spaCy

!pip install -U spacy-lookups-data

!python -m spacy download pt_core_news_lg

!pip install nltk

################################################################################################

# Instituição: IESB
# Disciplina:  Tópicos em Banco de Dados (TPBD)
# Objetivo:    Fornecer conhecimentos e práticas de paradigmas de programação para IA aplicada.
# Professor:   Bruno Miranda [bruno.marcos@iesb.edu.br]
# Data:        Junho2024

# Prática: Text Ming - Dataset fakenwes Brasil (FACTCKBR)

################################################################################################

# imports necessarios ao projeto

import pandas as pd
import spacy
import nltk
import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

# download e load de pacotes e modelo
nltk.download('punkt')
pln = spacy.load('pt_core_news_lg')

# codificação das funções utilitarias
def remover_acentos(df):
  df = df.str.replace('[ãá]', 'a')
  df = df.str.replace('[éê]', 'e')
  df = df.str.replace('[í]', 'i')
  df = df.str.replace('[ôó]', 'o')
  df = df.str.replace('[ú]', 'u')
  df = df.str.replace('[ç]', 'c')
  return df

def converter_letras_minusculas(df):
  df = df.str.lower()
  return df

def remover_pontuacao(df):
  df = df.str.replace('[^\w\s]', '')
  return df

def remover_numeros(df):
  df = df.apply(lambda x: ''.join([word for word in x.split() if not word.isdigit()]))
  return df

def remover_url(df):
  return df

def remover_tag(df):
  return df

# codificação das funções text mining

# remoção das palavras FREQUENTES do dataset de texto
def remover_palavras_frequentes(df, n_palavras):
  palavras = []
  textos = df.apply(nltk.word_tokenize)

  for texto in textos:
    for palavra in texto:
      palavras.append(palavra)

  freq = [x for x in nltk.FreqDist(palavras)]

  frequentes = freq[0:n_palavras]

  df = df.apply(lambda x: ''.join([word for word in x.split() if word not in (frequentes)]))

  return df

# remoção das palavras VAZIAS do dataset de texto
def remover_palavras_vazias(df):
  stopwords = pln.Defaults.stop_words

  df = df.apply(lambda x: ''.join([word for word in x.split() if word not in (stopwords)]))

  return df;

# efetua o processo de Transformação de Textos (lematização)
def exec_lematizacao(df):
  df = df.apply(lambda x: ''.join([word.lemma_ for word in pln(x)]))

  return df

# efetua o processo de Engenharia de Características de Textos
def exec_bag_of_words(df):
  metodo = CountVectorizer(ngram_range=(1, 1), stop_words=pln.Defaults.stop_words)

  X = metodo.fit_transform(df)
  df = pd.DataFrame(X.toarray(), columns=metodo.get_features_names())

  return df

def exec_tfidf(df):
  metodo = TfidfVectorizer()

  X = metodo.fit_transform(df)
  df = pd.DataFrame(X.toarray(), columns=metodo.get_feature_names_out())

  return df

# executa o modelo de NLP
df = pd.read_csv('FACTCKBR.tsv', sep='\t')
df = df.rename(columns={'title': 'titulo'})

## trata os dados em texto
df['titulo'] = remover_acentos(df['titulo'])
df['titulo'] = converter_letras_minusculas(df['titulo'])
df['titulo'] = remover_pontuacao(df['titulo'])
df['titulo'] = remover_numeros(df['titulo'])
df['titulo'] = remover_palavras_vazias(df['titulo'])
df['titulo'] = exec_lematizacao(df['titulo'])
df['titulo'] = remover_palavras_frequentes(df['titulo'], 20)

#df['titulo'] = exec_bag_of_words(df['titulo'])

# testa o modelo de NLP
dataset_final = exec_tfidf(df['titulo'])

dataset_final

from matplotlib import pyplot as plt
dataset_final['2estradaquebolsonaroinaugurounonordeste'].plot(kind='hist', bins=20, title='2estradaquebolsonaroinaugurounonordeste')
plt.gca().spines[['top', 'right',]].set_visible(False)