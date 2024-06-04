import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import geopandas as gpd

# Configurações iniciais
sns.set_style("dark")
cor_genero = ['#F781D8', '#819FF7']
st.set_page_config(layout="wide")

# Carregar dados
df = pd.read_csv('https://raw.githubusercontent.com/V1n1ci0s/projeto-Kayo_ter-a/main/base%20dados.csv')
gdf_brazil_states = gpd.read_file("https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
)

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
sns.barplot(x=[x.split(' ')[0] for x in mulheres.index.get_level_values(1)], y=mulheres.values, ax=ax)
ax.set_title('Faixa etária (mulheres)', fontsize=19)
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=[x.split(' ')[0] for x in mulheres.index.get_level_values(1)], y=mulheres.values, ax=ax)
ax.set_title('Faixa etária (mulheres)', fontsize=19)
st.pyplot(fig)

# Total de homens e mulheres
st.write(f"""
Total de homens: {sum(homens)}
Total de mulheres: {sum(mulheres)}
""")

# PIB per capita ao longo do tempo no Brasil
st.header("PIB per Capita ao Longo do Tempo no Brasil")
fig, ax = plt.subplots(figsize=(15, 5))
sns.lineplot(x=anos, y=gdp_media_brasil, color='green', ax=ax)
ax.set_ylabel('PIB per capita ($)', fontsize=15)
ax.set_title('PIB per capita ao longo do tempo', fontsize=19)
st.pyplot(fig)

# Correlação entre PIB per capita e número de suicídios no Brasil
st.header("Correlação entre PIB per Capita e Número de Suicídios no Brasil")
fig, ax = plt.subplots(figsize=(15, 5))
sns.regplot(x=gdp_media_brasil, y=suicidio_brasil_media, ax=ax, color='green')
ax.set_title('Correlação entre PIB per capita e número de suicídios por 100 mil habitantes', fontsize=15)
ax.set_ylabel('Média de suicídio / 100k habitantes', fontsize=13)
ax.set_xlabel('PIB per capita ($)', fontsize=11)
st.pyplot(fig)

# Média de suicídio no Brasil ao longo do tempo
st.header("Média de Suicídio no Brasil ao Longo do Tempo")
fig, ax = plt.subplots(figsize=(15, 5))
sns.lineplot(x=anos, y=suicidio_brasil_media, color='green', ax=ax)
ax.set_title('Média de suicídio a cada ano por 100 mil habitantes', fontsize=15)
ax.set_ylabel('Média de suicídio / 100k habitantes', fontsize=13)
st.pyplot(fig)

# Média de suicídio no Brasil ao longo do tempo com regressão
st.header("Média de Suicídio no Brasil ao Longo do Tempo com Regressão")
fig, ax = plt.subplots(figsize=(15, 5))
sns.regplot(x=anos, y=suicidio_brasil_media, ax=ax, color='green')
ax.set_title('Média de suicídio no Brasil a cada 100 mil habitantes ao longo do tempo', fontsize=17)
ax.set_ylabel('Média de suicídio / 100k habitantes', fontsize=13)
ax.set_xlabel('Anos', fontsize=13)
sns.lineplot(x=anos, y=suicidio_brasil_media, color='green', ax=ax)
st.pyplot(fig)

# Mapa mundial interativo com Plotly
st.header("Mapa Mundial de Taxas de Suicídio")
df_world = df.groupby(['year', 'country'])['suicides/100k pop'].mean().reset_index()
year_selected = st.slider("Selecione o Ano", min_value=int(df_world['year'].min()), max_value=int(df_world['year'].max()), value=int(df_world['year'].min()))

df_year = df_world[df_world['year'] == year_selected]

fig = px.choropleth(df_year, locations="country", locationmode='country names', color="suicides/100k pop", hover_name="country", projection="natural earth", title="Taxa de Suicídio por 100k habitantes")
st.plotly_chart(fig)

# Adicionando interatividade com Plotly
st.header("Gráficos Interativos")
option = st.selectbox('Selecione o Gráfico', ('Tendência de Suicídios por Sexo', 'Suicídios por Faixa Etária', 'Suicídios por Geração', 'Suicídios por Gênero'))

if option == 'Tendência de Suicídios por Sexo':
    fig = px.line(df_trend, labels={'value': 'Taxa de Suicídio por 100k habitantes', 'year': 'Ano'}, title="Tendência das Taxas de Suicídio por Sexo ao Longo do Tempo")
    st.plotly_chart(fig)

elif option == 'Suicídios por Faixa Etária':
    fig = px.bar(tabela.reset_index(), x='year', y=tabela.columns, barmode='stack', title="Suicídios por Faixa Etária no Brasil")
    st.plotly_chart(fig)

elif option == 'Suicídios por Geração':
    fig = px.histogram(df_brasil, x='generation', title="Suicídios por Geração no Brasil")
    st.plotly_chart(fig)

elif option == 'Suicídios por Gênero':
    fig = px.pie(df_brasil, names='sex', values='suicides_no', title="Número de Suicídios por Gênero no Brasil")
    st.plotly_chart(fig)
# Adicionando interatividade com Plotly
st.header("Gráficos Interativos")
option = st.selectbox('Selecione o Gráfico', ('Tendência de Suicídios por Sexo', 'Suicídios por Faixa Etária', 'Suicídios por Geração', 'Suicídios por Gênero'), key="graficos_interativos")

if option == 'Tendência de Suicídios por Sexo':
    fig = px.line(df_trend, labels={'value': 'Taxa de Suicídio por 100k habitantes', 'year': 'Ano'}, title="Tendência das Taxas de Suicídio por Sexo ao Longo do Tempo")
    st.plotly_chart(fig)

elif option == 'Suicídios por Faixa Etária':
    fig = px.bar(tabela.reset_index(), x='year', y=tabela.columns, barmode='stack', title="Suicídios por Faixa Etária no Brasil")
    st.plotly_chart(fig)

elif option == 'Suicídios por Geração':
    fig = px.histogram(df_brasil, x='generation', title="Suicídios por Geração no Brasil")
    st.plotly_chart(fig)

elif option == 'Suicídios por Gênero':
    fig = px.pie(df_brasil, names='sex', values='suicides_no', title="Número de Suicídios por Gênero no Brasil")
    st.plotly_chart(fig)

# Adicionando mais gráficos interativos
st.header("Mais Gráficos Interativos")

# Gráfico interativo de suicídios por país ao longo do tempo
st.subheader("Suicídios por País ao Longo do Tempo")
country_selection = st.multiselect("Selecione o(s) país(es)", df['country'].unique())
df_countries = df[df['country'].isin(country_selection)]
fig = px.line(df_countries, x='year', y='suicides/100k pop', color='country', title="Suicídios por País ao Longo do Tempo")
st.plotly_chart(fig)

# Gráfico interativo de suicídios por geração e sexo
st.subheader("Suicídios por Geração e Sexo")
fig = px.bar(df_brasil, x='generation', y='suicides_no', color='sex', barmode='group', title="Suicídios por Geração e Sexo no Brasil")
st.plotly_chart(fig)

# Gráfico interativo de suicídios por faixa etária e gênero
st.subheader("Suicídios por Faixa Etária e Gênero")
fig = px.bar(df_brasil, x='age', y='suicides_no', color='sex', barmode='group', title="Suicídios por Faixa Etária e Gênero no Brasil")
st.plotly_chart(fig)

# Adicionando opções de filtros e busca
st.sidebar.header("Opções de Filtro e Busca")

# Filtrar por país
country_filter = st.sidebar.multiselect("Filtrar por País", df['country'].unique())

# Filtrar por geração
generation_filter = st.sidebar.multiselect("Filtrar por Geração", df['generation'].unique())

# Filtrar por faixa etária
age_filter = st.sidebar.multiselect("Filtrar por Faixa Etária", df['age'].unique())

# Aplicar filtros
filtered_df = df[(df['country'].isin(country_filter)) & (df['generation'].isin(generation_filter)) & (df['age'].isin(age_filter))]

# Exibir dados filtrados
st.subheader("Dados Filtrados")
st.write(filtered_df.head())

# Adicionando mais análises e visualizações...

# Gráfico interativo de mapa de calor de suicídios por país ao longo do tempo
st.subheader("Mapa de Calor de Suicídios por País ao Longo do Tempo")
fig = px.choropleth(df, 
                    locations="country", 
                    locationmode='country names', 
                    color="suicides_no", 
                    hover_name="country", 
                    animation_frame="year",
                    range_color=[0, df['suicides_no'].max()],
                    title="Mapa de Calor de Suicídios por País ao Longo do Tempo")
fig.update_layout(geo=dict(showframe=False, showcoastlines=False))
st.plotly_chart(fig)

# Gráfico interativo de distribuição de suicídios por ano
st.subheader("Distribuição de Suicídios por Ano")
fig = px.histogram(df, x='year', title="Distribuição de Suicídios por Ano")
st.plotly_chart(fig)

# Gráfico interativo de distribuição de suicídios por país
st.subheader("Distribuição de Suicídios por País")
fig = px.histogram(df, x='country', title="Distribuição de Suicídios por País")
st.plotly_chart(fig)


