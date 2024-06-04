import streamlit as st
import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor


st.set_page_config(layout="wide", page_icon="📚")
st.title("📚 Vamos Explorar Juntos os DataSets!")

st.markdown("Pode encontrar os dataframes utilizados nesta aplicação no seguinte link, ou fazer download num dos botões abaixo: \n https://www.kaggle.com/datasets/ramjasmaurya/top-250s-in-imdb")

#------------- Carregar os DataFrames a partir do arquivo CSV -------------#
df = pd.read_csv("imdb (1000 movies) in june 2022.csv")
df1 = pd.read_csv("imdb (1000 tv series) - (june 2022).csv")

# ------------- Fazer Download dos DataFrames -------------#

# Fazer Download do DataFrame Filmes
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

# Fazer Download do DataFrame Séries
def convert_df1(df1):
    return df1.to_csv(index=False).encode('utf-8')

# Colunas para organizar os botões
col1, col2 = st.columns(2)

# Botão para Download DataFrame Filmes
with col1:
    csv_filmes = convert_df(df)
    st.download_button(
        "Download DataFrame Filmes",
        csv_filmes,
        "imdb (1000 movies) in june 2022.csv",
        "text/csv",
        key='download-csv-filmes'
    )

# Botão para Download DataFrame Séries
with col2:
    csv_series = convert_df1(df1)
    st.download_button(
        "Download DataFrame Séries",
        csv_series,
        "imdb (1000 tv series) - (june 2022).csv",
        "text/csv",
        key='download-csv-series'
    )

# ------------- Criação de Secções de Navegação -------------#

# Lista de secções
secoes = ["Filmes", "Séries"]

# Menu de navegação
st.sidebar.header("Menu de Navegação")

# Criação de links de navegação
for secao in secoes:
    st.sidebar.markdown(f"[{secao}](#{secao.lower()})")

# ------------- Conteúdo para Cada Secção -------------#

# Conteúdo específico para cada secção
for secao in secoes:
    st.markdown(f"<a name='{secao.lower()}'></a>", unsafe_allow_html=True)
    st.header(secao)

# ------------- Secção dos Filmes -------------#

    if secao == "Filmes":
        st.dataframe(df)

        st.header("IMDB Atores")

        # Carregando o dataset de filmes
        movies_df = df

        # Renomear colunas para facilitar o acesso
        movies_df.columns = movies_df.columns.str.strip().str.upper().str.replace(' ', '_')

        # Substituir caracteres indesejados na coluna "Year"
        movies_df['YEAR'] = movies_df['YEAR'].str.replace(r'[^0-9]', '', regex=True)

        # Função para obter o URL das Capas dos Filmes apartir de uma chave API pelo Título do Filme
        def get_poster_url_omdb(movie_title):
            omdb_api_key = "9b7816bf"  
            omdb_url = f"http://www.omdbapi.com/?apikey={omdb_api_key}&t={movie_title}"

            response = requests.get(omdb_url)
            data = response.json()

            if "Poster" in data and data["Poster"] != "N/A":
                return data["Poster"]
            else:
                return None

        # Função para ir buscar a capa do Filme apartir do URL gerado pela função "get_poster_url_omdb"
        def fetch_poster_urls(movie_titles):
            with ThreadPoolExecutor() as executor:
                poster_urls = list(executor.map(get_poster_url_omdb, movie_titles))
            return poster_urls

        # Criação de uma nova coluna para as capas dos Filmes
        movies_df["POSTER_URL"] = fetch_poster_urls(movies_df["MOVIE_NAME"])


        # Adicione opções iniciais para escolha entre "Ator" e "Diretor"
        option = st.radio("Escolha uma opção:", ["Ator", "Diretor"])

        if option == "Ator":
            st.subheader("Explorar por Ator")
            
            # Sidebar para seleção de atores
            all_actors = pd.unique(movies_df[["ACTOR_1", "ACTOR_2", "ACTOR_3", "ACTOR_4"]].values.flatten())
            actor_option = st.selectbox("Escolha um ator:", all_actors)
            actors_directors_worked_with = movies_df[(movies_df[["ACTOR_1", "ACTOR_2", "ACTOR_3", "ACTOR_4"]] == actor_option).any(axis=1)]

            st.header(f"Filmes com {actor_option}")
            actor_movies_df = movies_df[movies_df.isin([actor_option]).any(axis=1)][["MOVIE_NAME", "YEAR", "RATING", "POSTER_URL"]]

            # Organizar os filmes em colunas
            columns = st.columns(4)

            # Exibir filmes sequencialmente nas colunas
            current_column = 0
            for index, row in actor_movies_df.iterrows():
                with columns[current_column]:
                    st.image(row["POSTER_URL"], caption=f'{row["MOVIE_NAME"]} ({row["YEAR"]}) - Rating: {row["RATING"]}', width=150)
                current_column = (current_column + 1) % 4 


            # Selecione apenas diretores com quem o ator trabalhou
            directors_option = st.selectbox("Escolha um diretor:", actors_directors_worked_with["DIRECTOR"].unique())

            # Ver filmes por diretor e ator
            st.header(f"Filmes do diretor {directors_option} com {actor_option}")
            director_actor_movies_df = movies_df[movies_df["DIRECTOR"] == directors_option]
            common_movies = pd.merge(actor_movies_df, director_actor_movies_df, how="inner", on=["MOVIE_NAME", "YEAR", "RATING", "POSTER_URL"])

            # Organizar filmes com diretor e ator em colunas
            columns_common = st.columns(4)  

            # Exibir filmes sequencialmente nas colunas
            current_column_common = 0
            for index, row in common_movies.iterrows():
                with columns_common[current_column_common]:
                    st.image(row["POSTER_URL"], caption=f'{row["MOVIE_NAME"]} ({row["YEAR"]}) - Rating: {row["RATING"]}', width=150)
                current_column_common = (current_column_common + 1) % 4 

        elif option == "Diretor":
            st.subheader("Explorar por Diretor")
            
            # Sidebar para seleção de diretores
            all_directors = pd.unique(movies_df["DIRECTOR"])
            director_option = st.selectbox("Escolha um diretor:", all_directors)
            director_movies_df = movies_df[movies_df["DIRECTOR"] == director_option]

            st.header(f"Filmes do diretor {director_option}")
            director_columns = st.columns(4)

            # Exibir filmes sequencialmente nas colunas
            current_column_director = 0
            for index, row in director_movies_df.iterrows():
                with director_columns[current_column_director]:
                    st.image(row["POSTER_URL"], caption=f'{row["MOVIE_NAME"]} ({row["YEAR"]}) - Rating: {row["RATING"]}', width=150)
                current_column_director = (current_column_director + 1) % 4

            # Selecione apenas atores que trabalharam com o diretor escolhido
            actors_worked_with_director = pd.unique(director_movies_df[["ACTOR_1", "ACTOR_2", "ACTOR_3", "ACTOR_4"]].values.flatten())
            actor_option = st.selectbox("Escolha um ator:", actors_worked_with_director)

            st.header(f"Filmes do diretor {director_option} com {actor_option}")
            common_movies = director_movies_df[director_movies_df.isin([actor_option]).any(axis=1)][["MOVIE_NAME", "YEAR", "RATING", "POSTER_URL"]]
            
            # Organizar filmes com diretor e ator em colunas
            common_columns = st.columns(4)

            # Exibir filmes sequencialmente nas colunas
            current_column_common = 0
            for index, row in common_movies.iterrows():
                with common_columns[current_column_common]:
                    st.image(row["POSTER_URL"], caption=f'{row["MOVIE_NAME"]} ({row["YEAR"]}) - Rating: {row["RATING"]}', width=150)
                current_column_common = (current_column_common+1)% 4

    # ------------- Secção das Séries -------------#
    
    elif secao == "Séries":
        # Conteúdo específico para a seção de Séries
        st.dataframe(df1)
        
        st.header("IMDB Atores")

        # Carregando o dataset de séries
        series_df = df1

        # Renomear colunas para facilitar o acesso
        series_df.columns = series_df.columns.str.strip().str.upper().str.replace(' ', '_')

        # Substituir caracteres indesejados na coluna "Year"
        series_df['YEAR'] = series_df['YEAR'].str.replace(r'[^0-9]', '', regex=True)

        def get_poster_url_omdb(serie_title):
            omdb_api_key = "9b7816bf"  
            omdb_url = f"http://www.omdbapi.com/?apikey={omdb_api_key}&t={serie_title}"

            response = requests.get(omdb_url)
            data = response.json()

            if response.status_code == 200:
                if "Poster" in data and data["Poster"] != "N/A":
                    return data["Poster"]
                else:
                    print(f"No Poster found for: {serie_title}")
                    print(f"Data: {data}")
                    return None
            else:
                print(f"Request failed for: {serie_title}")
                print(f"Status Code: {response.status_code}")
            return None

        # Função para ir buscar a capa da Série apartir do URL gerado pela função "get_poster_url_omdb"
        def fetch_poster_urls(serie_titles):
            with ThreadPoolExecutor() as executor:
                poster_urls = list(executor.map(get_poster_url_omdb, serie_titles))
            return poster_urls

        # Criação de uma nova coluna para as capas dos Filmes
        series_df["POSTER_URL"] = fetch_poster_urls(series_df["SERIES_NAME"])

        st.subheader("Explorar por Ator")
            
        # Sidebar para seleção de atores
        all_actors = pd.unique(series_df[["ACTOR_1", "ACTOR_2", "ACTOR_3", "ACTOR_4"]].values.flatten())
        actor_option = st.selectbox("Escolha um ator:", all_actors)
        actors_directors_worked_with = series_df[(series_df[["ACTOR_1", "ACTOR_2", "ACTOR_3", "ACTOR_4"]] == actor_option).any(axis=1)]

        st.header(f"Séries com {actor_option}")
        actor_series_df = series_df[series_df.isin([actor_option]).any(axis=1)][["SERIES_NAME", "YEAR", "RATING", "POSTER_URL"]]

        # Organizar as séries em colunas
        columns = st.columns(4)
        
        # Verificar se não existe valores em branco no URL gerado
        for index, row in actor_series_df.iterrows():
            poster_url = row["POSTER_URL"]
            if poster_url is None:
                continue

            # Exibir a imagem se o URL for válido
            series_name = row["SERIES_NAME"] if row["SERIES_NAME"] is not None else ""
            year = row["YEAR"] if row["YEAR"] is not None else ""
            rating = row["RATING"] if row["RATING"] is not None else ""
            st.image(poster_url, caption=f'{series_name} ({year}) - Rating: {rating}', width=150, output_format="auto")

        # Exibir séries sequencialmente nas colunas
        current_column = 0
        for index, row in actor_series_df.iterrows():
            if row["POSTER_URL"] is not None:
                with columns[current_column]:
                    series_name = row["SERIES_NAME"] if row["SERIES_NAME"] is not None else ""
                    year = row["YEAR"] if row["YEAR"] is not None else ""
                    rating = row["RATING"] if row["RATING"] is not None else ""
                    st.image(row["POSTER_URL"], caption=f'{series_name} ({year}) - Rating: {rating}', width=150, output_format="auto")
            current_column = (current_column + 1) % 4 

        
        


