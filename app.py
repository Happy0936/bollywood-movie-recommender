import pickle
from pathlib import Path
from urllib.parse import quote_plus
import re
from html import escape
import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="Bollywood Movie Recommender", page_icon="🎬", layout="wide")

# Simple dark theme
st.markdown("""
<style>
.stApp {background: #0b0e14; color: white;}
.block-container {max-width: 1100px; padding-top: 3rem;}
h1, h2, h3 {color: white !important;}
div.stButton > button {background: #7555e8; color: white; border: none; border-radius: 10px; padding: 0.65rem 2rem;}
div.stButton > button:hover {background: #6043d1; color: white;}
.movie-card {background: #182036; border: 1px solid #303a55; border-radius: 12px; padding: 20px; min-height: 160px; margin-bottom: 14px;}
.movie-card h3 {font-size: 19px; margin: 0 0 14px 0;}
.movie-card p {color: #c2c9db; font-size: 14px; margin: 7px 0;}
.poster-box {position: relative; width: 100%; aspect-ratio: 2 / 3; border-radius: 10px; overflow: hidden; background: #161b26;
              display: flex; align-items: center; justify-content: center; color: #aeb9d2; font-size: 14px; margin-bottom: 12px;}
.poster-img {position: absolute; inset: 0; background-size: cover; background-position: center;}
.card-title {font-size: 17px; font-weight: 700; color: white; line-height: 1.3; height: 2.6em; overflow: hidden; margin-bottom: 8px;}
.card-line {font-size: 14px; color: #c2c9db; margin: 4px 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;}
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

# Poster from TMDB (needs TMDB_API_KEY in .streamlit/secrets.toml). Returns None if there is no key or no poster.
@st.cache_data(show_spinner=False)
def tmdb_poster(imdb_id):
    try:
        api_key = st.secrets["TMDB_API_KEY"]
    except Exception:
        return None
    try:
        url = f"https://api.themoviedb.org/3/find/{imdb_id}"
        data = requests.get(url, params={"api_key": api_key, "external_source": "imdb_id"}, timeout=5).json()
        results = data.get("movie_results") or []
        if results and results[0].get("poster_path"):
            return "https://image.tmdb.org/t/p/w500" + results[0]["poster_path"]
    except Exception:
        pass
    return None

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
        for start in range(0, len(results), 5):
            columns = st.columns(5)
            for column, movie in zip(columns, results[start:start + 5]):
                with column:
                    title = str(movie.get("title", "Unknown"))
                    genres = str(movie.get("genres", "Not available"))
                    rating = str(movie.get("imdb_rating", "Not available"))
                    # Try TMDB first, then the dataset's poster link
                    posters = [tmdb_poster(imdb_ids[title]) if title in imdb_ids else None, movie.get("poster_path")]
                    posters = [p for p in posters if isinstance(p, str) and p.startswith("http")]
                    search = quote_plus(re.sub(r"\s*\(.*?\)$", "", title))
                    links = f'<a href="https://www.justwatch.com/in/search?q={search}" target="_blank">📺 Where to watch</a>'
                    if title in imdb_ids:
                        links += f'</div><div class="card-line"><a href="https://www.imdb.com/title/{imdb_ids[title]}/" target="_blank">🎬 IMDb</a>'
                    # The "No poster" text sits behind the poster, so it shows when no poster loads.
                    # If the TMDB poster fails, the dataset poster underneath shows instead.
                    layers = ", ".join("url('" + escape(p.replace("'", "%27")) + "')" for p in posters)
                    image = f'<div class="poster-img" style="background-image: {layers};"></div>' if posters else ""
                    with st.container(border=True):
                        st.markdown(f"""
<div class="poster-box">🎞️ No poster{image}</div>
<div class="card-title">🎥 {escape(title)}</div>
<div class="card-line"><b>Genres:</b> {escape(genres)}</div>
<div class="card-line">⭐ <b>IMDb rating:</b> {escape(rating)}</div>
<div class="card-line">{links}</div>
""", unsafe_allow_html=True)
