# -*- coding: utf-8 -*-
"""Limpeza_e_tratamento_churn.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1oBMKqHt9vsDKAmP2iJ44dUx5efwls87U
"""

import pandas as pd

pd.read_json("dataset-telecon.json")

dados_churn = pd.read_json("dataset-telecon.json")
dados_churn.head()

dados_churn['conta'][0]

#Vamos usar o Json normalize para normalizar as colunas
pd.json_normalize(dados_churn['conta']).head()

#Vamos usar o Json normalize para normalizar as colunas
pd.json_normalize(dados_churn['telefone']).head()



#Importando a biblioteca Json
import json

with open("dataset-telecon.json") as f:
    json_bruto = json.load(f)

json_bruto

pd.json_normalize(json_bruto)

dados_normalizados = pd.json_normalize(json_bruto)
dados_normalizados.head()

#Usando a função abaixo para ver as informações dos dados
dados_normalizados.info()

#transformar o tipo de dado com o astype
dados_normalizados.head()

dados_normalizados[dados_normalizados['conta.cobranca.Total'] == ' '].head()

dados_normalizados[dados_normalizados['conta.cobranca.Total'] == ' '][
    ['cliente.tempo_servico', 'conta.contrato', 'conta.cobranca.mensal', 'conta.cobranca.Total']
]

dados_normalizados[dados_normalizados['conta.cobranca.Total'] == ' '].index

idx = dados_normalizados[dados_normalizados['conta.cobranca.Total'] == ' '].index

dados_normalizados.loc[idx, "conta.cobranca.Total"] = dados_normalizados.loc[idx, "conta.cobranca.mensal"] * 24

dados_normalizados.loc[idx, "cliente.tempo_servico"] = 24

dados_normalizados.loc[idx][
['cliente.tempo_servico', 'conta.contrato', 'conta.cobranca.mensal', 'conta.cobranca.Total']
]

dados_normalizados['conta.cobranca.Total'] = dados_normalizados['conta.cobranca.Total'].astype(float)

dados_normalizados.info()

for col in dados_normalizados.columns:
    print(f"Coluna: {col}")
    print(dados_normalizados[col].unique())
    print("-" * 30)

dados_normalizados.query("Churn == ''")

dados_normalizados[dados_normalizados['Churn'] != '']

dados_sem_vazio = dados_normalizados[dados_normalizados['Churn'] != '']

dados_sem_vazio = dados_normalizados[dados_normalizados['Churn'] != ''].copy()

dados_sem_vazio.info()

dados_sem_vazio.reset_index()

dados_sem_vazio.reset_index(drop=True, inplace=True)

dados_sem_vazio

#identificar dados duplicados
dados_sem_vazio.duplicated()

#Agora vou verificar o total, a quantidade de dados duplicados
dados_sem_vazio.duplicated().sum()

filtro_duplicadas = dados_sem_vazio.duplicated()
filtro_duplicadas

dados_sem_vazio[filtro_duplicadas]

#Fórmula para retirar duplicadas
dados_sem_vazio.drop_duplicates(inplace=True)

dados_sem_vazio.duplicated().sum()



"""Verificação de dados nulos"""

dados_sem_vazio.isna()

dados_sem_vazio.isna().sum()

dados_sem_vazio.isna().sum().sum()

dados_sem_vazio[dados_sem_vazio.isna().any(axis=1)]

dados_sem_vazio['cliente.tempo_servico'].isna()

filtro = dados_sem_vazio['cliente.tempo_servico'].isna()

dados_sem_vazio[filtro][['cliente.tempo_servico', 'conta.cobranca.mensal', 'conta.cobranca.Total']]

5957.90/90.45

import numpy as np

np.ceil(5957.90/90.45)

dados_sem_vazio['cliente.tempo_servico'].fillna(
    np.ceil(
        dados_sem_vazio['conta.cobranca.Total'] / dados_sem_vazio['conta.cobranca.mensal']
    ), inplace=True
)

dados_sem_vazio[filtro][['cliente.tempo_servico', 'conta.cobranca.mensal', 'conta.cobranca.Total']]

dados_sem_vazio.isna().sum()



"""Remover dados nulos"""

dados_sem_vazio['conta.contrato'].value_counts()

colunas_dropar = ['conta.contrato', 'conta.faturamente_eletronico', 'conta.metodo_pagamento']

dados_sem_vazio[colunas_dropar].isna().any(axis=1).sum()

#Retirar valores nulos com o dropna
dados_sem_vazio.dropna(subset=colunas_dropar)

df_sem_nulo = dados_sem_vazio.dropna(subset=colunas_dropar).copy()
df_sem_nulo.head()

df_sem_nulo.reset_index(drop=True, inplace=True)

df_sem_nulo.isna().sum()



"""Outliers"""

df_sem_nulo.describe()

import seaborn as sns

sns.boxplot(x=df_sem_nulo['cliente.tempo_servico'])

Q1 = df_sem_nulo['cliente.tempo_servico'].quantile(.25)
Q3 = df_sem_nulo['cliente.tempo_servico'].quantile(.75)
IQR = Q3 - Q1
limite_inferior = Q1 - 1.5*IQR
limite_superior = Q3 + 1.5*IQR

(df_sem_nulo['cliente.tempo_servico'] < limite_inferior) | (df_sem_nulo['cliente.tempo_servico'] > limite_superior)

outliers_index = (df_sem_nulo['cliente.tempo_servico'] < limite_inferior) | (df_sem_nulo['cliente.tempo_servico'] > limite_superior)
outliers_index

Q1 = df_sem_nulo['cliente.tempo_servico'].quantile(.25)
Q1

Q1 = df_sem_nulo['cliente.tempo_servico'].quantile(.25)
Q3 = df_sem_nulo['cliente.tempo_servico'].quantile(.75)

df_sem_nulo[outliers_index]['cliente.tempo_servico']



"""Substituir valores para Outliers"""

df_sem_out = df_sem_nulo.copy()

df_sem_out [outliers_index]['cliente.tempo_servico']

df_sem_out.loc[outliers_index, 'cliente.tempo_servico'] = np.ceil(
    df_sem_out.loc[outliers_index, 'conta.cobranca.Total'] /
    df_sem_out.loc[outliers_index, 'conta.cobranca.mensal']
)

sns.boxplot(x=df_sem_out['cliente.tempo_servico'])

df_sem_out [outliers_index]['cliente.tempo_servico']

df_sem_out [outliers_index][['cliente.tempo_servico', 'conta.cobranca.mensal', 'conta.cobranca.Total']]



"""Revover Outliers"""

df_sem_out [outliers_index]['cliente.tempo_servico']

Q1 = df_sem_nulo['cliente.tempo_servico'].quantile(.25)
Q3 = df_sem_nulo['cliente.tempo_servico'].quantile(.75)
IQR = Q3 - Q1
limite_inferior = Q1 - 1.5*IQR
limite_superior = Q3 + 1.5*IQR

outliers_index = (df_sem_nulo['cliente.tempo_servico'] < limite_inferior) | (df_sem_nulo['cliente.tempo_servico'] > limite_superior)
outliers_index

Q1 = df_sem_out['cliente.tempo_servico'].quantile(.25)
Q3 = df_sem_out['cliente.tempo_servico'].quantile(.75)
IQR = Q3 - Q1
limite_inferior = Q1 - 1.5*IQR
limite_superior = Q3 + 1.5*IQR

outliers_index = (df_sem_out['cliente.tempo_servico'] < limite_inferior) | (df_sem_out['cliente.tempo_servico'] > limite_superior)
outliers_index

df_sem_out[outliers_index]

df_sem_out[~outliers_index]
df_sem_out

sns.boxplot(x=df_sem_out['cliente.tempo_servico'])

df_sem_out

df_sem_out.drop('id_cliente', axis=1)

df_sem_id = df_sem_out.drop('id_cliente', axis=1).copy()
df_sem_id

mapeamento = {
    'nao': 0,
    'sim': 1,
    'masculino': 0,
    'feminino': 1
}

for col in dados_normalizados.columns:
    print(f"Coluna: {col}")
    print(dados_normalizados[col].unique())
    print("-" * 30)

for col in df_sem_id.columns:
    print(f"Coluna: {col}")
    print(df_sem_id[col].unique())
    print("-" * 30)

colunas = ['telefone.servico_telefone', 'Churn', 'cliente.parceiro', 'cliente.dependentes', 'conta.faturamente_eletronico', 'cliente.genero']

df_sem_id[colunas] = df_sem_id[colunas].replace(mapeamento)
df_sem_id

for col in df_sem_id.columns:
    print(f"Coluna: {col}")
    print(df_sem_id[col].unique())
    print("-" * 30)



"""One Hot Encoder (dummy)"""

s = pd.Series(list('abca'))
s

pd.get_dummies(s)

pd.get_dummies(s, dtype=int)

pd.get_dummies(df_sem_id)

df_dummies = pd.get_dummies(df_sem_id, dtype=int).copy()
df_dummies.head()

df_dummies.columns

df_dummies.info()
