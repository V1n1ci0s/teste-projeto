import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Configurações iniciais
sns.set_style("dark")
cor_genero = ['#F781D8', '#819FF7']
st.set_page_config(layout="wide")

# Carregar dados
df = pd.read_csv('https://raw.githubusercontent.com/V1n1ci0s/projeto-Kayo_ter-a/main/base%20dados.csv')

# Títulos e descrições
st.title("Análise de Suicídios")
st.write("""
         Este aplicativo interativo analisa as taxas de suicídio globalmente e no Brasil ao longo do tempo, com base em dados históricos.
         """)

# Exibir dataframe inicial
st.header("Dados Iniciais")
st.write(df.head())

# Tendência das taxas globais de suicídio ao longo do tempo por sexo
st.header("Tendência das Taxas Globais de Suicídio por Sexo")
df_trend = df.groupby(['year', 'sex'])['suicides/100k pop'].mean().unstack()

fig, ax = plt.subplots(figsize=(10, 6))
df_trend.plot(kind='line', ax=ax)
ax.set_xlabel('Ano')
ax.set_ylabel('Taxa média de suicídio por 100 mil habitantes')
ax.set_title('Tendência das taxas globais de suicídio ao longo do tempo por sexo')
ax.legend(title='Sexo')
st.pyplot(fig)

# Informações do dataframe
st.header("Informações do DataFrame")
buffer = st.text_area("Info do DataFrame", df.info(verbose=True, buf=None))

# Filtrando dados do Brasil
df_brasil = df[df['country']=='Brazil'].copy()

# Exibindo o dataframe do Brasil
st.header("Dados do Brasil")
st.write(df_brasil.head())

# Forma dos dataframes
st.write("Forma do dataframe mundial:", df.shape)
st.write("Forma do dataframe do Brasil:", df_brasil.shape)

# Valores nulos
st.write("Valores nulos no mundo:")
st.write(df.isnull().sum())
st.write("Valores nulos no Brasil:")
st.write(df_brasil.isnull().sum())

# Média de suicídios no Brasil e mundial ao longo dos anos
st.header("Média de Suicídios: Brasil vs Mundo")
anos = df_brasil['year'].unique()
suicidio_brasil_media = df_brasil.groupby('year')['suicides/100k pop'].mean()
suicidio_mundial_media = df.groupby('year')['suicides/100k pop'].mean()
gdp_media_mundo = df.groupby('year')['gdp_per_capita ($)'].mean()
gdp_media_brasil = df_brasil.groupby('year')['gdp_per_capita ($)'].mean()

# Ajuste para remover o ano de 2016
suicidio_mundial_media.drop(2016, inplace=True)

fig, ax = plt.subplots(figsize=(15, 5))
sns.lineplot(x=anos, y=suicidio_mundial_media, label='Mundial', color='blue', ax=ax)
sns.lineplot(x=anos, y=suicidio_brasil_media, label='Brasil', color='green', ax=ax)
ax.set_title('Média de suicídio ao longo do tempo (Brasil X Mundo)', fontsize=19)
ax.set_ylabel('N° de casos a cada 100 mil pessoas', fontsize=13)
st.pyplot(fig)

# Tabela de suicídios por faixa etária no Brasil
st.header("Suicídios por Faixa Etária no Brasil")
tabela = pd.pivot_table(df_brasil, values='suicides_no', index=['year'], columns=['age'])
column_order = ['5-14 years', '15-24 years', '25-34 years', '35-54 years', '55-74 years', '+75 years']
tabela = tabela.reindex(column_order, axis=1)
st.write(tabela.head())

# Gráfico de suicídios por faixa etária
fig, ax = plt.subplots(figsize=(16, 8))
tabela.plot.bar(stacked=True, ax=ax)
ax.legend(title='Idade')
ax.set_xlabel('Ano')
ax.set_title('Suicídio por faixa etária', fontsize=21)
st.pyplot(fig)

# Suicídio por geração
st.header("Suicídio por Geração")
fig, ax = plt.subplots(figsize=(13, 5))
sns.countplot(x='generation', order=df_brasil['generation'].value_counts().index, data=df_brasil, ax=ax)
ax.set_xlabel('Gerações', fontsize=13)
ax.set_title('Suicídio por geração', fontsize=21)
st.pyplot(fig)

# Gráfico de suicídio por gênero
generos = df_brasil.groupby('sex').suicides_no.sum() / df_brasil.groupby('sex').suicides_no.sum().sum()
fig, ax = plt.subplots(figsize=(6, 6))
ax.pie(generos, labels=['MULHERES', 'HOMENS'], colors=cor_genero, autopct='%1.1f%%', shadow=True, startangle=90)
ax.set_title('Número de suicídio por gênero (1985 - 2015)', fontsize=15)
st.pyplot(fig)

# Quantidade de suicídios por gênero no Brasil
st.write(f"Quantas vezes a mais o homem se suicida em relação às mulheres? {df_brasil.groupby('sex').suicides_no.sum()[1] / df_brasil.groupby('sex').suicides_no.sum()[0]:.2f}")

# Gráfico de gênero ao longo do tempo
st.header("Gênero ao Longo do Tempo")
tabela2 = pd.pivot_table(df_brasil, values='suicides/100k pop', index=['sex'], columns=['year'])
tabela2 = tabela2.T

fig, ax = plt.subplots(figsize=(15, 5))
tabela2.plot.bar(stacked=True, color=cor_genero, ax=ax)
ax.set_xlabel('Ano')
ax.set_title('Gênero ao longo do tempo', fontsize=19)
ax.set_ylabel('N° de suicídio a cada 100 mil pessoas', fontsize=13)
st.pyplot(fig)

# Faixa etária por sexo
st.header("Faixa Etária por Sexo")
mulheres = df.groupby(['sex', 'age'])['suicides_no'].sum()[:6]
homens = df.groupby(['sex', 'age'])['suicides_no'].sum()[6:]

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=[x.split
