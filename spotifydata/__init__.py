import pandas as pd
from spotifydata.charts import *
from spotifydata.features import *

def extract_charts(region="global", frequency="weekly"):
    sp = Charts()
    outputs = sp.scrape_charts(region=region, frequency=frequency)
    df = sp.to_dataframe(outputs)
    df = df[df.position <= 50]
    df.to_csv(f"data/charts-{region}-{frequency}.csv", index=False)
    return df

def get_mainfeat(sp):
    outputs = sp.get_main_features()
    df = sp.to_dataframe(outputs)
    df.to_csv(f"data/tracks-mainfeatures.csv", index=False)
    return df

def run_scraper():
    charts = extract_charts()
    sp = Features(charts)
    features = get_mainfeat(sp)
    print("JOB: MERGING DATASET")
    df = charts.merge(features, on="track_id", how="left")
    df.to_csv("data/charts-features.csv", index=False)
    print("SUCCESS: Datasets have been Merged")
    print("Done Scraping Data!")
    return df