# 🎬 Bollywood Movie Recommender

A content-based Bollywood movie recommendation web app built with Python and Streamlit.

**Live app:** https://bollywood-movies-recommender.streamlit.app/

## Features
- Pick any Bollywood movie and get 5 similar movies
- Movie posters, genres and IMDb rating on every card
- 🎬 IMDb link for each movie
- 📺 "Where to watch" link (JustWatch India) showing Netflix, Prime Video, JioHotstar, Zee5 and more

## How it works
1. Movie data (genres, story, summary, cast) is combined into one text "tag" per movie.
2. The text is turned into vectors with scikit-learn.
3. Cosine similarity finds the movies closest to the one you picked.
4. The similarity matrix is saved as `similarity.pkl` and loaded by the app.

## Tech stack
Python · Pandas · NumPy · scikit-learn · NLTK · Streamlit · Git LFS

## Project structure
```
├── app.py                              # Streamlit web app
├── movie_recommendation_fixed.ipynb    # Data cleaning and model building
├── movie_list.pkl                      # Processed movie data
├── similarity.pkl                      # Similarity matrix (Git LFS)
├── Dataset/                            # Bollywood movie CSV files
└── requirements.txt
```

## Run locally
```
git lfs install
git clone https://github.com/Happy0936/bollywood-movie-recommender.git
cd bollywood-movie-recommender
pip install -r requirements.txt
streamlit run app.py
```

## Author
Happy Kumari, M.Tech Project
