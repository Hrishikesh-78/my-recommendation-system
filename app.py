import numpy as np
import streamlit as st
import pickle
import pandas as pd
import requests
#from PIL import Image

def get_recommendations(df,mapping,title,cosine_sim,top=5):                #Find similar most similar on basis of cosine similarity matrix
    idx = mapping[title]   #form movie title get index for cosine matrix
    
    sim_scores = list(enumerate(cosine_sim[idx]))   # Get the pairwsie similarity scores of all movies with that movie index
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)   # Sort the movies based on the similarity scores
    sim_scores = sim_scores[1:top+1]   # Get the scores of the 10 most similar movies

    movie_indices = [i[0] for i in sim_scores]   # Get the movie indices
    movie_posters=[get_poster(movie_id)[0] for movie_id in df['movie_id'].iloc[movie_indices]] 
    movie_overviews=[get_poster(movie_id)[1] for movie_id in df['movie_id'].iloc[movie_indices]] 
    movie_ratings=[get_poster(movie_id)[2] for movie_id in df['movie_id'].iloc[movie_indices]] 
    movie_date=[get_poster(movie_id)[3] for movie_id in df['movie_id'].iloc[movie_indices]] 
    movie_genre=[get_poster(movie_id)[4] for movie_id in df['movie_id'].iloc[movie_indices]] 
    return movie_posters,movie_overviews,movie_ratings,movie_date,movie_genre,list(df['movie'].iloc[movie_indices])    # Return the top 10 most similar movies and its posters

def movie_2_id_map(df):
    d={}
    for i in range(len(df)):
        movie=df.loc[i,'movie']
        if movie not in d:
            d[movie]=i
    return d    
def get_poster(movie_id):   #my api_key=acaae44ff45beeee150d8f1a63f00ee9
    url_path=f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=acaae44ff45beeee150d8f1a63f00ee9' 
    response=requests.get(url_path)
    data=response.json()
    poster='https://image.tmdb.org/t/p/original/'+data['poster_path']
    movie_overview=data['overview']
    vote_avg=data['vote_average']
    date=data['release_date']
    genres=[]
    for d in data['genres']:
        genres.append(d['name'])
  
    return poster,movie_overview,vote_avg,date,genres



movie_d=pickle.load(open('movies_dict.pkl','rb'))
cosine_sim=pickle.load(open('cosine_similarity_matrix.pkl','rb'))
df=pd.DataFrame(movie_d)
mapping=movie_2_id_map(df)



st.title('Movie Recommendation System')
selected_movie= st.selectbox('Select the Movie for Recommendation', df['movie'].values)


#nested button
if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked=False
def callback():
    st.session_state.button_clicked=True

if st.button('Recommend',on_click=callback) or st.session_state.button_clicked:
    poster_list,overview_list,rating_list,date_list,genre_list,recc_movie_list=get_recommendations(df,mapping,selected_movie,cosine_sim,top=5)
    
    for i in range(len(poster_list)):
        lst=st.columns(2)
        col1,col2=lst
        with col1:
            st.text(str(i+1)+'.'+recc_movie_list[i])
            #new_image = Image.open(requests.get(poster_list[i], stream=True).raw).resize((400, 500))  
            st.image(poster_list[i])
        with col2:    
            #if st.button('Overview'+str(i+1)):
            st.text('Rating: '+ str(rating_list[i]))
            st.text('Released on: '+ str(date_list[i]))
            st.text('Genre: '+ str(genre_list[i]))
            st.write('Overview: '+ overview_list[i])

        