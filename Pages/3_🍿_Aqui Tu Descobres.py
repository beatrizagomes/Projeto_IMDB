import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from PIL import Image

st.set_page_config (layout="wide", page_icon="🍿")
st.title("🍿 Aproveita este Universo!")

#------------- Carregar os DataFrames a partir do arquivo CSV -------------#
df = pd.read_csv("imdb (1000 tv series) - (june 2022).csv")
df1 = pd.read_csv("imdb (1000 movies) in june 2022.csv")

#------------- Escolha da Informação a Exibir -------------#
escolha = ["Filmes", "Séries", "Que Filme vais ver hoje?", "Que Série vais começar hoje?"]

selected=st.radio("Escolha o Quer Fazer:", escolha, horizontal=False)

# Renomear colunas para facilitar o acesso
df.columns = df.columns.str.strip().str.upper().str.replace(' ', '_')
df1.columns = df1.columns.str.strip().str.upper().str.replace(' ', '_')

# Substituir caracteres indesejados na coluna "Year"
df1['YEAR'] = df1['YEAR'].str.replace(r'[^0-9]', '', regex=True)

# Converter a coluna "Year" para numérica
df1['YEAR'] = pd.to_numeric(df1['YEAR'], errors='coerce')


# Função para obter o URL das Capas das Séries apartir de uma chave API pelo Título da Série
def get_poster_url_omdb(series_name):
    omdb_api_key = "9b7816bf"  
    omdb_url = f"http://www.omdbapi.com/?apikey={omdb_api_key}&t={series_name}"

    response = requests.get(omdb_url)
    data = response.json()

    if "Poster" in data and data["Poster"] != "N/A":
        return data["Poster"]
    else:
        return None

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

#------------- Dropdown para selecionar a Série -------------#

if selected == "Séries":
    selected_serie = st.selectbox("Escolhe uma série:", df["SERIES_NAME"])

    # Informação sobre a Série
    serie_info = df[df["SERIES_NAME"] == selected_serie].iloc[0]

    # Obter a capa da Série através do URL com a utilização da API
    poster_url = get_poster_url_omdb(selected_serie)

    # Configuração para 2 Colunas
    col1, col2 = st.columns([1, 2])

    # Painel de Informação sobre a Série (Coluna 1)
    with col1:
        st.subheader("Informações das Series:")
        st.write(f"**Título:** {serie_info['SERIES_NAME']}")
        st.write(f"**Ano:** {serie_info['YEAR']}")
        st.write(f"**Classificação:** {serie_info['CERTIFICATE']}")
        st.write(f"**Duração:** {serie_info['RUNTIME']}")
        st.write(f"**Gênero:** {serie_info['GENRE']}")
        st.write(f"**Avaliação IMDb:** {serie_info['RATING']}")
        st.write(f"**Atores:** {serie_info['ACTOR_1']}, {serie_info['ACTOR_2']}, {serie_info['ACTOR_3']}, {serie_info['ACTOR_4']}")
        st.write(f"**Numero de Votos:** {serie_info['VOTES']}")
        st.write(f"**Resumo:** {serie_info['DETAILS']}")

    # Painel com a Capa da Série (Coluna 2)
    with col2:
        st.subheader("Imagem Serie:")
        if poster_url:
            response = requests.get(poster_url)

            # Confirmar o tipo de informações presentes
            content_type = response.headers.get('Content-Type')
            if content_type and content_type.startswith('image'):
                try:
                    # Tentativa de abrir a imagem
                    poster_img = Image.open(BytesIO(response.content))
                    st.image(poster_img, caption=selected_serie, use_column_width=True)
                except Exception as e:
                    st.warning(f"Error opening the image: {e}")
            else:
                st.warning("Unable to find the poster for this serie. Try another image source.")
        else:
            st.warning("Unable to find the poster for this serie. Try another image source.")

#------------- Dropdown para selecionar o Filme -------------#

if selected == "Filmes":
    selected_movie = st.selectbox("Escolhe um filme:", df1["MOVIE_NAME"])

    # Informação sobre o Filme
    movie_info = df1[df1["MOVIE_NAME"] == selected_movie].iloc[0]

    # Obter a capa do Filme através do URL com a utilização da API
    poster_url = get_poster_url_omdb(selected_movie)

    # Configuração para 2 Colunas
    col1, col2 = st.columns([1, 2])

    # Painel de Informação sobre o Filme (Coluna 1)
    with col1:
        st.subheader("Informações do Filme:")
        st.write(f"**Título:** {movie_info['MOVIE_NAME']}")
        st.write(f"**Ranking:** {movie_info['RANKING_OF_MOVIE']}")
        st.write(f"**Ano:** {movie_info['YEAR']}")
        st.write(f"**Classificação:** {movie_info['CERTIFICATE']}")
        st.write(f"**Duração:** {movie_info['RUNTIME']}")
        st.write(f"**Gênero:** {movie_info['GENRE']}")
        st.write(f"**Avaliação IMDb:** {movie_info['RATING']}")
        st.write(f"**Metascore:** {movie_info['METASCORE']}")
        st.write(f"**Diretor:** {movie_info['DIRECTOR']}")
        st.write(f"**Atores:** {movie_info['ACTOR_1']}, {movie_info['ACTOR_2']}, {movie_info['ACTOR_3']}, {movie_info['ACTOR_4']}")
        st.write(f"**Numero de Votos:** {movie_info['VOTES']}")
        st.write(f"**Bilheteria:** {movie_info['GROSS_COLLECTION']}")
        st.write(f"**Resumo:** {movie_info['DETAIL_ABOUT_MOVIE']}")

    # Painel com a Capa do Filme (Coluna 2)
    with col2:
        st.subheader("Movie Poster:")
        if poster_url:
            response = requests.get(poster_url)

            # Confirmar o tipo de informações presentes
            content_type = response.headers.get('Content-Type')
            if content_type and content_type.startswith('image'):
                try:
                    # Tentativa de abrir a imagem
                    poster_img = Image.open(BytesIO(response.content))
                    st.image(poster_img, caption=selected_movie, use_column_width=True)
                except Exception as e:
                    st.warning(f"Error opening the image: {e}")
            else:
                st.warning("Unable to find the poster for this movie. Try another image source.")
        else:
            st.warning("Unable to find the poster for this movie. Try another image source.")

#------------- Dropdown para selecionar um Filme Random -------------#

if selected == "Que Filme vais ver hoje?":
    
    # Definir a lista de gêneros
    genres_list = ["Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Drama", "Family", "Fantasy",
               "Film-Noir", "History", "Horror", "Music", "Musical", "Mystery", "Romance", "Sci-Fi", "Sport", "Thriller", "War", "Western"]
    
    # Sidebar para seleção de gênero
    st.title("O que vais ver hoje?")

    # Dropdown para seleção de gênero
    selected_genre = st.selectbox("Selecione um gênero", ["Selecione um gênero"] + genres_list[1:])

    # Verificar se um gênero foi selecionado
    if selected_genre != "Selecione um gênero":
        # Filtrar dados por gênero
        filtered_df1 = df1[df1['GENRE'].str.contains(selected_genre, case=False, na=False)]

        # Selecionar um filme aleatório do gênero escolhido
        random_movie = filtered_df1.sample(1)

        # Exibir informações sobre o filme selecionado aleatoriamente
        st.subheader(f"Filme Aleatório do Gênero {selected_genre}")

        # Display information about the selected movie
        movie_info = random_movie.iloc[0]

        # Try to get the poster URL using OMDB API
        poster_url = get_poster_url_omdb(movie_info['MOVIE_NAME'])

        # Layout em duas colunas
        col1, col2 = st.columns([1, 2])

        # Exibir informações sobre o filme à esquerda
        with col1:
            st.subheader("Informações do Filme:")
            st.write(f"**Título:** {movie_info['MOVIE_NAME']}")
            st.write(f"*Ranking:* {movie_info['RANKING_OF_MOVIE']}")
            st.write(f"*Ano:* {movie_info['YEAR']}")
            st.write(f"*Classificação:* {movie_info['CERTIFICATE']}")
            st.write(f"*Duração:* {movie_info['RUNTIME']}")
            st.write(f"*Gênero:* {movie_info['GENRE']}")
            st.write(f"*Avaliação IMDb:* {movie_info['RATING']}")
            st.write(f"*Metascore:* {movie_info['METASCORE']}")
            st.write(f"*Diretor:* {movie_info['DIRECTOR']}")
            st.write(f"*Atores:* {movie_info['ACTOR_1']}, {movie_info['ACTOR_2']}, {movie_info['ACTOR_3']}, {movie_info['ACTOR_4']}")
            st.write(f"*Numero de Votos:* {movie_info['VOTES']}")
            st.write(f"*Bilheteria:* {movie_info['GROSS_COLLECTION']}")
            st.write(f"*Resumo:* {movie_info['DETAIL_ABOUT_MOVIE']}")

        # Exibir poster do filme (imagem) à direita
        with col2:
            st.subheader("Movie Poster:")
            if poster_url:
                # Exibir poster do filme se a URL for encontrada
                response = requests.get(poster_url)

                # Verificar o tipo de conteúdo
                content_type = response.headers.get('Content-Type')
                if content_type and content_type.startswith('image'):
                    try:
                        # Tentar abrir a imagem
                        poster_img = Image.open(BytesIO(response.content))
                        st.image(poster_img, caption=movie_info['MOVIE_NAME'], use_column_width=True)
                    except Exception as e:
                        st.warning(f"Erro ao abrir a imagem: {e}")
                else:
                    st.warning("Não foi possível encontrar o poster para este filme. Tente outra fonte de imagem.")
            else:
                st.warning("Não foi possível encontrar o poster para este filme. Tente outra fonte de imagem.")
    else:
        st.warning("Por favor, selecione um gênero para ver um filme aleatório.")

if selected == "Que Série vais começar hoje?":
    # Definir a lista de gêneros para séries
    genres_list_series = ["Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Documentary", "Drama", 
                      "Family", "Fantasy", "Film-Noir", "History", "Horror", "Music", "Musical", "Mystery", "Romance", 
                      "Sci-Fi", "Sport", "Thriller", "War", "Western", "Game-Show", "News", "Reality-TV", "Talk show"]

    # Definir a lista de durações possíveis para episódios
    duration_mapping = {
        "Selecione a duração": (0, float('inf')),
        "menos de 10 minutos": (0, 10),
        "menos de 20 minutos": (11, 20),
        "menos de 30 minutos": (21, 30),
        "menos de 40 minutos": (31, 40),
        "menos de 50 minutos": (41, 50),
        "menos de 60 minutos": (51, 60),
        "mais de 1 hora": (61, float('inf'))
    }

    # Sidebar para seleção de gênero e duração para séries
    st.title("O que vais começar a ver hoje?")

    # Dropdown para seleção de gênero para séries
    selected_genre_series = st.selectbox("Selecione um gênero", ["Selecione um gênero"] + genres_list_series[1:])

    # Verificar se um gênero foi selecionado para séries
    if selected_genre_series != "Selecione um gênero":
        # Filtrar dados por gênero
        filtered_df_series = df[df['GENRE'].str.contains(selected_genre_series, case=False, na=False)]

        # Agora, vamos garantir que a coluna 'RUNTIME' contenha apenas números
        df['RUNTIME'] = df['RUNTIME'].str.extract('(\d+)').astype(float)

        # Verificar se há opções disponíveis após a filtragem
        if not filtered_df_series.empty:
            # Dropdown para seleção de duração para episódios
            selected_duration_series = st.selectbox("Selecione a duração do episódio", list(duration_mapping.keys()))

            # Verificar se uma duração foi selecionada para séries
            if selected_duration_series != "Selecione a duração":
                # Converter a coluna 'RUNTIME' para numérica
                filtered_df_series['RUNTIME'] = filtered_df_series['RUNTIME'].str.extract('(\d+)').astype(float)

                # Filtrar dados por duração
                duration_range = duration_mapping[selected_duration_series]
                filtered_df_series = filtered_df_series[(filtered_df_series['RUNTIME'] >= duration_range[0]) & 
                                                        (filtered_df_series['RUNTIME'] <= duration_range[1])]

                # Verificar se há opções disponíveis após a filtragem
                if not filtered_df_series.empty:
                    # Selecionar uma série aleatória do gênero e duração escolhidos
                    random_series = filtered_df_series.sample(1)

                    # Exibir informações sobre a série selecionada aleatoriamente
                    st.subheader(f"Série Aleatória do Gênero {selected_genre_series} e Duração {selected_duration_series}")

                    # Display information about the selected series
                    series_info = random_series.iloc[0]

                    # Try to get the poster URL using OMDB API
                    poster_url_series = get_poster_url_omdb(series_info['SERIES_NAME'])

                    # Layout em duas colunas
                    col1, col2 = st.columns([1, 2])

                    # Exibir informações sobre a série à esquerda
                    with col1:
                        st.subheader("Informações da Série:")
                        st.write(f"*Título:* {series_info['SERIES_NAME']}")
                        st.write(f"*Ranking:* {series_info['RANKING']}")
                        st.write(f"*Ano:* {series_info['YEAR']}")
                        st.write(f"*Classificação:* {series_info['CERTIFICATE']}")
                        st.write(f"*Duração do Episódio:* {series_info['RUNTIME']} minutos")
                        st.write(f"*Gênero:* {series_info['GENRE']}")
                        st.write(f"*Avaliação IMDb:* {series_info['RATING']}")
                        st.write(f"*Atores Principais:* {series_info['ACTOR_1']}, {series_info['ACTOR_2']}, {series_info['ACTOR_3']}, {series_info['ACTOR_4']}")
                        st.write(f"*Numero de Votos:* {series_info['VOTES']}")
                        st.write(f"*Detalhes:* {series_info['DETAILS']}")

                    # Exibir poster da série (imagem) à direita
                    with col2:
                        st.subheader("Série Poster:")
                        if poster_url_series:
                            # Exibir poster da série se a URL for encontrada
                            response_series = requests.get(poster_url_series)

                            # Verificar o tipo de conteúdo
                            content_type_series = response_series.headers.get('Content-Type')
                            if content_type_series and content_type_series.startswith('image'):
                                try:
                                    # Tentar abrir a imagem
                                    poster_img_series = Image.open(BytesIO(response_series.content))
                                    st.image(poster_img_series, caption=series_info['SERIES_NAME'], use_column_width=True)
                                except Exception as e:
                                    st.warning(f"Erro ao abrir a imagem: {e}")
                            else:
                                st.warning("Não foi possível encontrar o poster para esta série. Tente outra fonte de imagem.")
                        else:
                            st.warning("Não foi possível encontrar o poster para esta série. Tente outra fonte de imagem.")
                else:
                    st.warning(f"Não há séries disponíveis para o gênero {selected_genre_series} e a duração {selected_duration_series}.")
            else:
                st.warning("Por favor, selecione a duração do episódio para ver uma série aleatória.")
        else:
            st.warning(f"Não há opções de tempo disponíveis para o gênero {selected_genre_series}. Escolha outro gênero.")
    else:
        st.warning("Por favor, selecione um gênero para ver uma série aleatória.")

else:
    st.info('Por favor, selecione pelo menos uma opção para a visualização das informações.')
