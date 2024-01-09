import pickle
import streamlit as st
import requests

def fetch_movie_details(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url).json()
    poster_path = data['poster_path']
    imdb_id = data.get('imdb_id', '')  # Assuming IMDb ID is directly available in the API response
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path, imdb_id

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_ids = []
    for i in distances[1:6]:
        # fetch the movie details including poster and IMDb ID
        movie_id = movies.iloc[i[0]].movie_id
        full_path, imdb_id = fetch_movie_details(movie_id)
        recommended_movie_posters.append(full_path)
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_ids.append(imdb_id)

    return recommended_movie_names, recommended_movie_posters, recommended_movie_ids

# Streamlit app
st.set_page_config(page_title='Movie Recommender', layout='wide')

# Load data
movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))

# Netflix-themed styling
st.markdown("""
    <style>
        body {
            background-color: #141414;
            color: #ffffff;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        }
        .st-bq {
            background-color: #141414 !important;
            color: #ffffff !important;
        }
        .st-cv {
            color: #ffffff !important;
        }
        .st-d8 {
            background-color: #E50914 !important;
            color: #ffffff !important;
        }
        .st-ez {
            background-color: #E50914 !important;
        }
        .st-em {
            color: #ffffff !important;
        }
        .st-cl {
            color: #ffffff !important;
        }
        .st-fv {
            color: #ffffff !important;
        }
    </style>
""", unsafe_allow_html=True)

# UI
st.title('Movie Recommender System Using Machine Learning')
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters, recommended_movie_ids = recommend(selected_movie)

    # Display recommendations
    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i], use_column_width=True)
            st.markdown(f"<a href='https://www.imdb.com/title/{recommended_movie_ids[i]}' target='_blank'>"
                        "<div class='watch-button'>Watch on Netflix</div></a>", unsafe_allow_html=True)

# Custom styling with HTML
st.markdown("""
    <style>
        .watch-button {
            background-color: #E50914; /* Netflix Red */
            border: none;
            color: white;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
        }
    </style>
""", unsafe_allow_html=True)

