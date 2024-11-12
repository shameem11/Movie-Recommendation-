import pickle

import requests
import streamlit as st 


# Load movie list
with open('/home/mshameem/Documents/Movie-Recommendation-/research/artifacts/movie_list.pkl', 'rb') as file:
    movie = pickle.load(file)

# Load similarity data
with open('/home/mshameem/Documents/Movie-Recommendation-/research/artifacts/similarity.pkl', 'rb') as file:
    similarity = pickle.load(file)

movie_list = movie['title'].values
selected_movie = st.selectbox("type or select movie",movie_list)



import requests

url = "https://api.themoviedb.org/3/movie/movie_id?language=en-US"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlZTE3ZjhiZmUyYTEyNTEzNDIzZTk4OGZlZDYyMjNmOSIsIm5iZiI6MTczMTQyNzEzNy4xNjA2NzQsInN1YiI6IjY3MmQwMWQ3Yzc0ODcxOGJmMDczOTNhYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.sAAaONMMYwocOCH7sjXvcJx5NOgZcNRHf5DpQNwoyAI"
}

response = requests.get(url, headers=headers)

print(response.text)







import requests

def fetch(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?language=en-US".format(movie_id)
    headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlZTE3ZjhiZmUyYTEyNTEzNDIzZTk4OGZlZDYyMjNmOSIsIm5iZiI6MTczMTQyNzEzNy4xNjA2NzQsInN1YiI6IjY3MmQwMWQ3Yzc0ODcxOGJmMDczOTNhYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.sAAaONMMYwocOCH7sjXvcJx5NOgZcNRHf5DpQNwoyAI"
     } 
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error if the request was unsuccessful
        
        data = response.json()  # Parse the JSON response
        poster_path = data.get('poster_path')  # Use get to avoid KeyError
        
        if poster_path:  # Check if poster_path exists
            full_path = 'https://image.tmdb.org/t/p/w500/' + poster_path
            return full_path
        else:
            return None  # Return None if there's no poster path
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for movie_id {movie_id}: {e}")
        return None


def recommend(movie_title):
    # Find the index of the movie that matches the title
    index = movie[movie['title'] == movie_title].index[0]
    
    # Get similarity scores for the movie and sort them
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    # Lists to store recommended movie names and posters
    recommended_movie_names = []
    recommended_movie_posters = []
    
    # Loop through the sorted distances to get top 5 recommendations
    for i in distances[1:6]:  # Exclude the first element as it's the movie itself
        movie_id = movie.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch(movie_id))
        recommended_movie_names.append(movie.iloc[i[0]].title)
    
    return recommended_movie_names, recommended_movie_posters



st.header('movie Recommendation System')

if st.button('show recommendation'):
    recommended_movie_name,recommended_movie_postter = recommend(selected_movie)
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_name[0])
        st.image(recommended_movie_postter[0])
    with col2:
        st.text(recommended_movie_name[1])
        st.image(recommended_movie_postter[1])
    with col3:
        st.text(recommended_movie_name[2])
        st.image(recommended_movie_postter[2])
    with col4:
        st.text(recommended_movie_name[3])
        st.image(recommended_movie_postter[3])
    with col5:
        st.text(recommended_movie_name[4])
        st.image(recommended_movie_postter[4])

    

