# The next greatest hit @ Spotify
A project created in fulfillment for our DATA102 class in De La Salle Univeristy (AY 2020-2021).

Authors:
- Lorenzo Mercado
- Nathan Roleda
- Bea Teope
- James Candelario

# About
The project aims to predict the next top 10 Spotify songs based on Spotify Top 50 Charts and Music Features data. The charts data used in this project came from `SpotifyCharts.com` extracted using `BeautifulSoup`. While the music features of each song were extracted from `Spotify's WEBAPI` via `Spotipy`. The original dataset contained Top200 songs but were cut by the authors of this repository for the purpose of reducing computing requirements.

# Virtual Environment
The project was developed in a virtual environment using `virtualenv`. The authors highly suggest the usage of a virual environment to run this project.

# Requirements
The project was developed using the following libraries:
```
jupyter
cloudscraper
spotipy
beautifulsoup4
yellowbrick
scikit-learn
pandas
numpy
seaborn
matplotlib
plotly
```

To install the libraries, run the following command:
```pip install requirements.txt```

# Scraping Data
Run the following command to scrape the data from `SpotifyCharts.com` and `Spotify's WEBAPI`:
```
python3 main.py
```

# Data Exploration & Prediction
You may view how we explored the data and made predictions using through `spotify_eda_prediction.ipynb`.

# References
- Giridih, J. (2020). Spotify Analysis (Starman). Retrieved from https://www.kaggle.com/darkstardream/spotify-analysis-starman
- Surat, Gu. (2021). Music Recommendation System using Spotify Dataset. Retrieved from https://www.kaggle.com/vatsalmavani/music-recommendation-system-using-spotify-dataset