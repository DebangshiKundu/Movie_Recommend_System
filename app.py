import streamlit as st
import pickle
import pandas as pd
import requests


# Function to get the poster URL from TMDb API
def poster(movie_id):

    res = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=d4bcea76a17dd0816b2e9880f93e0a63')
    data = res.json()
    return 'https://image.tmdb.org/t/p/w500' + data['poster_path']

# Function to recommend movies
def recommend(movie):
    l = []
    mov_poster = []
    idx = df.loc[df.title == movie].index[0]
    dist = sim[idx]
    mov = sorted(list(enumerate(dist)), reverse=True, key=lambda x: x[1])[1:6]
    for i in mov:
        movie_id = df.iloc[i[0]].id
        l.append(df.iloc[i[0]].title)
        mov_poster.append(poster(movie_id))
    return l, mov_poster


st.title('Movie Recommender System')

df = pickle.load(open('mov.pkl', 'rb'))
df = pd.DataFrame(df)
sim = pickle.load(open('sim.pkl', 'rb'))

selected = st.selectbox('Which movie would you like to watch?', df['title'].values)

# Recommend movies
if st.button('Recommend'):
    mov_list, mov_poster = recommend(selected)

    # Display recommendations in columns
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(mov_list[i])
            st.image(mov_poster[i])
