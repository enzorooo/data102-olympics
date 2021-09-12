import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import pandas as pd
import time

load_dotenv()

class Features:
    def __init__(self, charts):
        self.charts = charts
        # Spotify Scraper
        auth_manager = SpotifyClientCredentials()
        self.sp = spotipy.Spotify(auth_manager=auth_manager, requests_timeout=60)
    
    def get_unique_tracks(self):
        charts = self.charts['track_id'].unique().tolist()
        return charts

    def batch_tracks(self, batch_size=50):
        track_ids = self.get_unique_tracks()
        batches = [track_ids[x:x+batch_size] for x in range(0, len(track_ids), batch_size)]
        print(f"No. of Unique Songs:                     {len(track_ids)}")
        print(f"No. of Batches (<=100 track_ids/batch):  {len(batches)}")
        return batches

    def get_main_features(self):
        batches = self.batch_tracks(batch_size=100)
        sp = self.sp

        all_track_features = []
        for i, batch in enumerate(batches):
            try:
                print(f"EXTRACT:Extracting Main Features - Batch {i+1} of {len(batches)}")
                track_features = sp.audio_features(tracks=batch)
                for track_feature in track_features:
                    track_feature['track_id'] = track_feature['id']
                    del track_feature['id']
                all_track_features = all_track_features + track_features
            except Exception as e:
                print(f"FAILED: Failed to Extract Main Features - Batch {i+1} of {len(batches)}")
                print(f"ERROR:  {e}")
        print(f"SUCCESS: {len(all_track_features)} tracks extracted with main acoustic features.")
        return all_track_features

    def to_dataframe(self,data):
        df = pd.DataFrame(data)
        return df