import pickle
from pathlib import Path
from urllib.parse import quote_plus
import re
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Bollywood Movie Recommender", page_icon="🎬", layout="wide")

# Simple dark theme
st.markdown("""
<style>
.stApp {background: #0b1020; color: white;}
.block-container {max-width: 1100px; padding-top: 3rem;}
h1, h2, h3 {color: white !important;}
div.stButton > button {background: #7555e8; color: white; border: none; border-radius: 10px; padding: 0.65rem 2rem;}
div.stButton > button:hover {background: #6043d1; color: white;}
.movie-card {background: #182036; border: 1px solid #303a55; border-radius: 12px; padding: 20px; min-height: 160px; margin-bottom: 14px;}
.movie-card h3 {font-size: 19px; margin: 0 0 14px 0;}
.movie-card p {color: #c2c9db; font-size: 14px; margin: 7px 0;}
</style>
""", unsafe_allow_html=True)

# Load files created by the notebook
folder = Path(__file__).resolve().parent
try:
    with open(folder / "movie_list.pkl", "rb") as f:
        movies = pickle.load(f).reset_index(drop=True)
    with open(folder / "similarity.pkl", "rb") as f:
        similarity = pickle.load(f)
except FileNotFoundError:
    st.error("Run the notebook first to generate movie_list.pkl and similarity.pkl.")
    st.stop()

# IMDb ids for the "IMDb" link (looked up from the dataset by title)
imdb_ids = pd.read_csv(folder / "Dataset" / "bollywood_full.csv", usecols=["title_x", "imdb_id"]).drop_duplicates("title_x").set_index("title_x")["imdb_id"].to_dict()

# Recommend five similar movies using cosine similarity
def recommend(title):
    matches = movies.index[movies["title"] == title].tolist()
    if not matches:
        return []
    index = matches[0]
    scores = list(enumerate(similarity[index]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return [movies.iloc[i] for i, score in scores if i != index][:5]

st.markdown("<h1 style='text-align:center;'>🎬 Bollywood Movie Recommendation</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#aeb9d2;'>Discover movies similar to your favorites</p>", unsafe_allow_html=True)

selected_movie = st.selectbox("Choose a Bollywood movie", movies["title"].dropna().tolist())

if st.button("✨ Explore Movies", type="primary"):
    st.subheader("Recommended Movies")
    results = recommend(selected_movie)
    if not results:
        st.warning("No recommendations found.")
    else:
        for start in range(0, len(results), 3):
            columns = st.columns(3)
            for column, movie in zip(columns, results[start:start + 3]):
                with column:
                    title = str(movie.get("title", "Unknown"))
                    genres = str(movie.get("genres", "Not available"))
                    rating = str(movie.get("imdb_rating", "Not available"))
                    poster = movie.get("poster_path")
                    # Streamlit renders escaped text by default with st.write
                    with st.container(border=True):
                        if isinstance(poster, str) and poster.startswith("http"):
                            st.image(poster, width=180)
                        else:
                            st.markdown("<div style='width:180px;height:260px;background:#182036;border-radius:8px;display:flex;align-items:center;justify-content:center;color:#aeb9d2;'>🎞️ No poster</div>", unsafe_allow_html=True)
                        st.markdown(f"### 🎥 {title}")
                        st.write("**Genres:**", genres)
                        st.write("⭐ **IMDb rating:**", rating)
                        search = quote_plus(re.sub(r"\s*\(.*?\)$", "", title))
                        links = f"[📺 Where to watch](https://www.justwatch.com/in/search?q={search})"
                        if title in imdb_ids:
                            links += f" · [🎬 IMDb](https://www.imdb.com/title/{imdb_ids[title]}/)"
                        st.markdown(links)
