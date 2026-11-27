# Deploy on Streamlit Community Cloud (with Git LFS)

Nothing in your app was changed. Only 3 files were added:
`requirements.txt`, `.gitattributes`, and this `DEPLOY.md`.

`similarity.pkl` is 132 MB. GitHub refuses normal files over 100 MB and the
website upload button stops at 25 MB, so you must upload with Git + Git LFS
from your computer.

## 1. Install the tools (once)
- Git: https://git-scm.com/downloads
- Git LFS: https://git-lfs.com (Git for Windows already includes it)

## 2. Create an empty GitHub repo
github.com → **+** → **New repository** → name `movie-recommender`, **Public**,
do NOT add a README → **Create repository**.

## 3. Upload from this folder
Open a terminal inside this folder (the one with `app.py`) and run:

```bash
git init
git lfs install
git lfs track "*.pkl"
git add .
git commit -m "Movie recommender"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/movie-recommender.git
git push -u origin main
```

Check on GitHub: `similarity.pkl` should say **"Stored with Git LFS"**.

## 4. Deploy
1. Go to https://share.streamlit.io and sign in with GitHub.
2. **Create app** → **Deploy a public app from GitHub**.
3. Repository: `YOUR-USERNAME/movie-recommender`, Branch: `main`, Main file path: `app.py`.
4. Click **Deploy** and wait 2–3 minutes.

## Notes
- Free GitHub LFS gives 1 GB of download per month. Each Streamlit (re)deploy
  downloads the 132 MB file, so that's roughly 7 redeploys a month. If you run
  out, the app shows "Run the notebook first..." because the .pkl is missing.
- If the app shows an error, click **Manage app** (bottom right) to read the logs.
- In the notebook, `pd.read_csv('dataset/bollywood_full.csv')` uses a small `d`
  but the folder is `Dataset`. This doesn't affect the website, but if you rerun
  the notebook on Mac/Linux change it to `Dataset/`.
