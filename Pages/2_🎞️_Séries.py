import pandas as pd
import streamlit as st
import altair as alt
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_icon="🎞️")
st.title("🎞️ Séries")


#------------- Carregar o DataFrame a partir do arquivo CSV -------------#
df = pd.read_csv("imdb (1000 tv series) - (june 2022).csv")

# Renomear colunas para facilitar o acesso
df.columns = df.columns.str.strip().str.upper().str.replace(' ', '_')

# Renomear colunas para facilitar o acesso
df.columns = df.columns.str.strip().str.upper().str.replace(' ', '_')

# Limpeza da coluna "YEAR" para séries
df['YEAR'] = df['YEAR'].str.extract(r'(\d{4})')

# Converter a coluna 'YEAR' para o tipo numérico
df['YEAR'] = pd.to_numeric(df['YEAR'], errors='coerce')

# Lista de gêneros
genres_list = ["Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Documentary",
               "Drama", "Family", "Fantasy", "Film-Noir", "History", "Horror", "Music", "Musical",
               "Mystery", "Romance", "Sci-Fi", "Sport", "Thriller", "War", "Western", "Game-Show",
               "News", "Reality-TV", "Talk show"]

#------------- Opção de Escolha do Tipo de Gráfico -------------#
opcao_grafico = st.radio("Escolha o tipo de gráfico:", ["TOP Séries por Género", "Relação entre Votos e Rating", "Gêneros ao longo dos anos"])

#------------- Ínicio da Apresentação do Gráfico -------------#
if opcao_grafico == "TOP Séries por Género":
   
    # Caixa para seleção por gênero
    selected_genre = st.selectbox("Selecione um gênero", genres_list)

    # Filtrar os dados por gênero
    filtered_df = df[df['GENRE'].str.contains(selected_genre, case=False, na=False)]

    # Converter a coluna "VOTES" para números
    filtered_df['VOTES'] = filtered_df['VOTES'].str.replace(',', '').astype(float)

    # Converter a coluna "RANKING" para números
    filtered_df['RANKING'] = pd.to_numeric(filtered_df['RANKING'].str.replace(',', ''), errors='coerce')

    # Criar um gráfico de barras horizontais com texto
    chart = alt.Chart(filtered_df).mark_bar().encode(
        x=alt.X('VOTES:Q', title='VOTES'),
        y=alt.Y('RANKING:O', title='RANKING'),
        color='RATING:O',
        tooltip=['SERIES_NAME:N', 'RANKING:O', 'VOTES:Q', 'RATING:O']
    ).properties(
        width=600,
        title=f"Top Séries ({selected_genre})" 
    )

    # Adicionar texto com o nome da série (com quebras de linha)
    text = chart.mark_text(
        align='left',
        baseline='middle',
        dx=3,
    ).encode(
        text='SERIES_NAME:N'
    )

    # Combinar gráfico de barras com texto
    final_chart = (chart + text).interactive()

    # Exibir gráfico
    st.altair_chart(final_chart, use_container_width=True)

# ------------- Fazer um Gráfico de Dispersão (Rating vs Votes) -------------#

elif opcao_grafico == "Relação entre Votos e Rating":
    scatter_fig = go.Figure()

    scatter_fig.add_trace(
        go.Scatter(
            x=df['VOTES'],
            y=df['RATING'],
            mode='markers',
            marker=dict(
                size=8,
                color='rgba(31, 119, 180, 0.7)',
                line=dict(
                    width=2,
                    color='DarkSlateGrey'
                    )
                ),
            text=df['SERIES_NAME']
            )
        )

        # Configurações de layout para o gráfico de dispersão
    scatter_fig.update_layout(
        title='Relação entre o Rating e os Votos',
        xaxis=dict(title='Número de Votos'),
        yaxis=dict(title='Rating'),
        showlegend=False,
        height=1000, 
        width=1600,  
        )

    st.plotly_chart(scatter_fig, use_container_width=True)

# ------------- Código para o gráfico de Barras -------------
elif opcao_grafico == "Gêneros ao longo dos anos":
    st.markdown('## Gêneros ao longo dos anos')

    # Defina opções dos anos
    escolha_anos_series = [str(ano) for ano in range(1951, 2023)]

    # Defina opções dos anos
    escolha_anos = [str(ano) for ano in range(1999, 2001)]

    # Colunas para opções de seleção
    col1, col2 = st.columns(2)

    # Opções de seleção dos anos
    with col1:
        escolha_opcao_1 = st.checkbox("Escolha todos os anos")

    with col2:
        escolha_opcao_2 = st.checkbox("Compare entre 2 ou mais anos")

    # Lógica para a seleção dos anos para séries
    if escolha_opcao_1:
        escolha_opcao_2 = False
        anos_selecionados_series = escolha_anos_series if escolha_opcao_1 else []
    elif escolha_opcao_2:
        escolha_opcao_1 = False
        anos_selecionados_series = st.multiselect("Escolha os anos:", escolha_anos_series, default=['1999', '2001'])
    else:
        anos_selecionados_series = [st.selectbox("Escolha o ano:", escolha_anos_series)]

    # Verificar se existe anos selecionados para séries
    if anos_selecionados_series:
        # Filtrar o DataFrame para incluir apenas os anos selecionados
        filtered_df_series = df[df['YEAR'].astype(str).isin(anos_selecionados_series)]

        # Extrair o primeiro gênero da lista (se houver múltiplos gêneros)
        filtered_df_series['GENRE'] = filtered_df_series['GENRE'].str.split(',').str[0].str.strip()

        # Filtrar DataFrame para incluir apenas colunas relevantes
        genre_df_series = filtered_df_series[['YEAR', 'GENRE']]

        # Criar um DataFrame com contagem de gêneros por ano
        genre_counts_series = pd.crosstab(genre_df_series['YEAR'], genre_df_series['GENRE'])

        # Criar um gráfico de barras empilhadas para séries
        stacked_bar_fig_series = go.Figure()

        for genre in genre_counts_series.columns:
            stacked_bar_fig_series.add_trace(go.Bar(
                x=genre_counts_series.index,
                y=genre_counts_series[genre],
                name=genre
            ))

        # Configurações de layout para o gráfico de barras empilhadas para séries
        stacked_bar_fig_series.update_layout(
            barmode='stack',
            title='Número de Séries por Gênero ao Longo dos Anos',
            xaxis=dict(title='Ano'),
            yaxis=dict(title='Número de Séries'),
            showlegend=True
        )

        st.plotly_chart(stacked_bar_fig_series, use_container_width=True)

    else:
        st.info('Por favor, selecione pelo menos um ano para visualizar o gráfico para séries.')

# ------------- Fazer Download do DataFrame -------------#
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

csv = convert_df(df)

st.download_button(
   "Download Dataframe",
   csv,
   "imdb (1000 tv series) - (june 2022).csv",
   "text/csv",
   key='download-csv')