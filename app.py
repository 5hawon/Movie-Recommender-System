import pickle
import streamlit as st
import requests
# Function to fetch movie poster
def fetch_poster(movie_id, size='w500'):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/{size}/{poster_path}"
   
    return full_path


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
fancy_photo_url = "https://editor.analyticsvidhya.com/uploads/76889recommender-system-for-movie-recommendation.jpg"  # Replace with the URL of your fancy photo
st.markdown(f'<img src="{fancy_photo_url}" style="width:100%; height:300px;">', unsafe_allow_html=True)

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
#Image Carousel
import streamlit.components.v1 as components
imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")
imageUrls = [
    'https://image.tmdb.org/t/p/w500//otzHnhXba5XsE6Gozl3Gzks0z8L.jpg',
    'https://image.tmdb.org/t/p/w500//7WsyChQLEftFiDOVTGkv3hFpyyt.jpg',
    'https://image.tmdb.org/t/p/w500//dsKRtNIPFcmxhs6RDOMRCm0PfkW.jpg',
    'https://image.tmdb.org/t/p/w500//eZsFXr3m0shC5HH7SRlZouiuQVH.jpg',
    'https://image.tmdb.org/t/p/w500//75gDv38UgRtAukSxNXcjatyQmEa.jpg',
    'https://image.tmdb.org/t/p/w500//bQqHksFAeUdozGGABxHJt3YVIyA.jpg',
    'https://image.tmdb.org/t/p/w500//iFQrK0NHA4OMAvzyJVW4DA0kAFz.jpg',
    'https://image.tmdb.org/t/p/w500//hek3koDUyRQk7FIhPXsa6mT2Zc3.jpg',
    'https://image.tmdb.org/t/p/w500//qJ2tW6WMUDux911r6m7haRef0WH.jpg',
    'https://image.tmdb.org/t/p/w500//k7eYdWvhYQyRQoU2TB2A2Xu2TfD.jpg',
    'https://image.tmdb.org/t/p/w500//1QpO9wo7JWecZ4NiBuu625FiY1j.jpg',
    'https://image.tmdb.org/t/p/w500//x9yjkm9gIz5qI5fJMUTfBnWiB2o.jpg',
    'https://image.tmdb.org/t/p/w500//jg73umEpBHT7l4DBmV5bR78H1JI.jpg'

   
]

imageCarouselComponent(imageUrls=imageUrls, height=200)

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
            st.markdown(f"<a class='button-text' href='https://www.imdb.com/title/{recommended_movie_ids[i]}' target='_blank'>"
                        "<div class='watch-button'>Go to IMDB</div></a>", unsafe_allow_html=True)

# Custom styling with HTML
st.markdown("""
    <style>
        .watch-button {
            background-color: #e50914; /* Netflix Red */
            border: none;
            color: white;
            decoration: none;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 20px;
            margin: 4px 2px;
            cursor: pointer;
        }
        .button-text {
            text-decoration: none;
            decoration: none;
            color: white;
            }
    </style>
""", unsafe_allow_html=True)

