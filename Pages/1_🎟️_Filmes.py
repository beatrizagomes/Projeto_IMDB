import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_icon="🎟️")
st.title("🎟️ Evolução dos Filmes e dos Ratings")

#------------- Carregar o DataFrame a partir do arquivo CSV -------------#
try:
    df = pd.read_csv("imdb (1000 movies) in june 2022.csv")

    # Renomear colunas para facilitar o acesso
    df.columns = df.columns.str.strip().str.upper().str.replace(' ', '_')

    # Substituir caracteres indesejados na coluna "Year"
    df['YEAR'] = df['YEAR'].str.replace(r'[^0-9]', '', regex=True)

    # Agora, converta a coluna "Year" para numérica
    df['YEAR'] = pd.to_numeric(df['YEAR'], errors='coerce')

except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}")
    st.stop()

# Remover o símbolo "$" e a letra "M" da coluna 'GROSS_COLLECTION' e converter para valores numéricos
df['GROSS_COLLECTION'] = df['GROSS_COLLECTION'].replace('[\$,M]', '', regex=True).astype(float)

# Ordenar DataFrame com base na coluna 'GROSS_COLLECTION' de forma descendente
df = df.sort_values(by='GROSS_COLLECTION', ascending=True)

#------------- Opção de Escolha do Tipo de Gráfico -------------#
opcao_grafico = st.radio("Escolha o tipo de gráfico:", ["Filmes por Ano", "Relação entre Votos e Bilheteria", "Generos ao longo dos anos"])

#------------- Gráfico de Filmes por Ano -------------#
if opcao_grafico == "Filmes por Ano":
    # Defina opções dos anos
    escolha_anos = [str(ano) for ano in range(1920, 2023)]

    # Colunas para opções de seleção
    col1, col2 = st.columns(2)

    # Opções de seleção dos anos
    with col1:
        escolha_opcao_1 = st.checkbox("Escolha todos os anos")

    with col2:
        escolha_opcao_2 = st.checkbox("Compare entre 2 ou mais anos")

    # Lógica para a seleção dos anos
    if escolha_opcao_1:
        # Se "Escolha todos os anos" estiver selecionado, desmarcar "Compare entre 2 ou mais anos"
        escolha_opcao_2 = False

        anos_selecionados = escolha_anos if escolha_opcao_1 else []
    elif escolha_opcao_2:
        # Se "Compare entre 2 ou mais anos" estiver selecionado, desmarcar "Escolha todos os anos"
        escolha_opcao_1 = False

        anos_selecionados = st.multiselect("Escolha os anos:", escolha_anos, default=['1999', '2001'])
    else:
        anos_selecionados = [st.selectbox("Escolha o ano:", escolha_anos)]

    # Verificar se existe anos selecionados
    if anos_selecionados:
        # Filtrar o DataFrame para incluir apenas os anos selecionados
        filtered_df = df[df['YEAR'].astype(str).isin(anos_selecionados)]

        # Criar um gráfico combinado de barras e linha
        fig = go.Figure()

        # Adicionar barras para o número de filmes por ano (eixo y à esquerda)
        fig.add_trace(
            go.Bar(
                x=filtered_df['YEAR'].value_counts().index.astype(str),
                y=filtered_df['YEAR'].value_counts().values,
                name='Número de Filmes',
                marker_color='rgba(31, 119, 180, 0.7)'
            )
        )

        # Adicionar linha para a média do rating por ano (eixo y à direita)
        fig.add_trace(
            go.Scatter(
                x=filtered_df.groupby('YEAR')['RATING'].mean().reset_index()['YEAR'].astype(str),
                y=filtered_df.groupby('YEAR')['RATING'].mean().reset_index()['RATING'],
                name='Média do Rating',
                yaxis='y2',
                mode='lines+markers',
                marker=dict(color='rgba(255, 127, 14, 0.7)'),
                text=filtered_df.groupby('YEAR')['RATING'].mean().reset_index()['RATING']
            )
        )

        # Configurações de layout
        fig.update_layout(
            title='Número de Filmes Realizados e Média do Rating por Ano',
            yaxis=dict(title='Número de Filmes', showgrid=False),
            yaxis2=dict(title='Média do Rating', overlaying='y', side='right', showgrid=False),
            xaxis=dict(title='Ano'),
            showlegend=True
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info('Por favor, selecione pelo menos um ano para visualizar o gráfico.')

#------------- Gráfico de Relação entre Votos e Bilheteria -------------#
elif opcao_grafico == "Relação entre Votos e Bilheteria":
    st.markdown('## Relação entre Votos e Bilheteria')
    
    
    # Criar o gráfico de dispersão
    scatter_fig = go.Figure()

    scatter_fig.add_trace(
        go.Scatter(
            x=df['VOTES'],
            y=df['GROSS_COLLECTION'],
            mode='markers',
            marker=dict(
                size=8,
                color='rgba(31, 119, 180, 0.7)',
                line=dict(
                    width=2,
                    color='DarkSlateGrey'
                )
            ),
            text=df['MOVIE_NAME']
        )
    )

    # Configurações de layout para o gráfico de dispersão
    scatter_fig.update_layout(
        title='Relação entre Votos e Bilheteria',
        xaxis=dict(title='Número de Votos'),
        yaxis=dict(title='Arrecadação Bruta (M$)'),
        showlegend=False,
        height=1000, 
        width=1600,  
    )

    st.plotly_chart(scatter_fig, use_container_width=True)

#------------- Código para o gráfico de Barras -------------#
elif opcao_grafico == "Generos ao longo dos anos":
    st.markdown('## Generos ao longo dos anos')

    # Defina opções dos anos
    escolha_anos = [str(ano) for ano in range(1920, 2023)]

    # Colunas para opções de seleção
    col1, col2 = st.columns(2)

    # Opções de seleção dos anos
    with col1:
        escolha_opcao_1 = st.checkbox("Escolha todos os anos")

    with col2:
        escolha_opcao_2 = st.checkbox("Compare entre 2 ou mais anos")

    # Lógica para a seleção dos anos
    if escolha_opcao_1:
        escolha_opcao_2 = False

        anos_selecionados = escolha_anos if escolha_opcao_1 else []
    elif escolha_opcao_2:
        escolha_opcao_1 = False

        anos_selecionados = st.multiselect("Escolha os anos:", escolha_anos, default=['1999', '2001'])
    else:
        anos_selecionados = [st.selectbox("Escolha o ano:", escolha_anos)]

    # Verificar se existe anos selecionados
    if anos_selecionados:
        # Filtrar o DataFrame para incluir apenas os anos selecionados
        filtered_df = df[df['YEAR'].astype(str).isin(anos_selecionados)]

        # Extrair o primeiro gênero da lista (se houver múltiplos gêneros)
        filtered_df['GENRE'] = filtered_df['GENRE'].str.split(',').str[0].str.strip()

        # Filtrar DataFrame para incluir apenas colunas relevantes
        genre_df = filtered_df[['YEAR', 'GENRE']]

        # Criar um DataFrame com contagem de gêneros por ano
        genre_counts = pd.crosstab(genre_df['YEAR'], genre_df['GENRE'])

        # Criar um gráfico de barras empilhadas
        stacked_bar_fig = go.Figure()

        for genre in genre_counts.columns:
            stacked_bar_fig.add_trace(go.Bar(
                x=genre_counts.index,
                y=genre_counts[genre],
                name=genre
            ))

        # Configurações de layout para o gráfico de barras empilhadas
        stacked_bar_fig.update_layout(
            barmode='stack',
            title='Número de Filmes por Gênero ao Longo dos Anos',
            xaxis=dict(title='Ano'),
            yaxis=dict(title='Número de Filmes'),
            showlegend=True
        )

        st.plotly_chart(stacked_bar_fig, use_container_width=True)

    else:
        st.info('Por favor, selecione pelo menos um ano para visualizar o gráfico.')

#------------- Fazer Download do DataFrame -------------#
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(df)

st.download_button(
    "Download Dataframe",
    csv,
    "imdb (1000 movies) in june 2022.csv",
    "text/csv",
    key='download-csv'
)