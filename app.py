import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch movie poster
def fetch_poster(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=d97abb7307b2775d602721fc1037b369&language=en-US")
    data = response.json()
    return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"

# Function to recommend movies based on selected movie
def recommend_movies(selected_movie, movies, similarity):
    movie_index = movies[movies["title"] == selected_movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommend_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_movies_poster.append(fetch_poster(movie_id))

    return recommend_movies, recommend_movies_poster

# Main function
def main():
    st.title("Movie Recommender System")

    # Load movie data
    movies_dict = pickle.load(open('movies_dic.pk', 'rb'))
    movies = pd.DataFrame(movies_dict)

    # Load similarity data
    similarity = pickle.load(open('similarity.pkl', 'rb'))

    # Display search box
    selected_movie = st.selectbox('Search for a movie:', movies['title'].values)

    # Display recommendation button
    if st.button('Recommend'):
        recommendation_names, recommendation_posters = recommend_movies(selected_movie, movies, similarity)
        st.markdown("**Recommended Movies:**")
        cols = st.columns(5)
        for i in range(len(recommendation_names)):
            with cols[i]:
                st.text(recommendation_names[i])
                st.image(recommendation_posters[i])

    # Display movie posters and names
    st.markdown("**Explore Movies:**")
    cols = st.columns(5)
    for i, movie_row in movies.iterrows():
        if i % 5 == 0:
            cols = st.columns(5)
        with cols[i % 5]:
            st.text(movie_row['title'])
            st.image(fetch_poster(movie_row['movie_id']))

if __name__ == "__main__":
    main()

