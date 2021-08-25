import pandas as pd
import requests
import cloudscraper
from bs4 import BeautifulSoup
import datetime 

class Charts:
    def __init__(self):
        self.scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session
        self.today = datetime.date.today().strftime('%Y-%m-%d')

    def get_next_date(self, curr_date, frequency):
        if frequency=="daily":
            if type(curr_date)==type('s'):
                curr_date = datetime.datetime.strptime(curr_date, "%Y-%m-%d")
            next_day = curr_date + datetime.timedelta(days=1)
            return next_day.strftime('%Y-%m-%d')
        elif frequency=="weekly":
            start_of_week = curr_date[:10]
            end_of_week = curr_date[-10:]
            start_2 = datetime.datetime.strptime(start_of_week, "%Y-%m-%d") + datetime.timedelta(days=7)
            end_2 = datetime.datetime.strptime(end_of_week, "%Y-%m-%d") + datetime.timedelta(days=7)
            next_week = "{}--{}".format(start_2.strftime('%Y-%m-%d'), end_2.strftime('%Y-%m-%d'))
            return next_week
        else: 
            raise ValueError("frequency must be in ['daily', 'weekly'].")
            
    def dt(self, date):
        return datetime.datetime.strptime(date, "%Y-%m-%d")

    def scrape_charts(self, 
                    region, 
                    frequency="weekly", 
                    start_date=None, 
                    end_date=None,
                    verbose=False):
        # Argument checking
        assert(frequency in ["daily", "weekly"])
        if start_date is None:
            start_date = "2017-01-01" if frequency=="daily" else "2016-12-23--2016-12-30"
        if end_date is None:
            end_date = self.today

        curr_date = start_date
        all_outputs = []

        # Loop until we exceed end_date
        while self.dt(curr_date[-10:]) <= self.dt(end_date):
            try:
                curr_url = f"https://spotifycharts.com/regional/{region}/{frequency}/{curr_date}"
                outputs = self.scrape_chars_from_url(curr_url)
                all_outputs.extend(outputs)
                print("Successfully scraped for {}".format(curr_date))
            except:
                print("Error! Failed for {}".format(curr_date))
            curr_date = self.get_next_date(curr_date, frequency)
    
        return all_outputs

    
    def scrape_chars_from_url(self, url):
        region = url.split('/')[4]
        date = url.split('/')[6]
        content = self.scraper.get(url) # Replaced requests.get()
        
        # Beautiful Soup Scraper
        soup = BeautifulSoup(content.content, "html.parser")
        songs = soup.find("table", class_="chart-table").find("tbody").find_all("tr")
        
        # Empty list to contain year data
        year_data = []

        for song in songs:
            # get song track-id
            track_id = song.find("td", class_="chart-table-image").find("a", href=True)
            track_id = track_id['href']

            #get chart position
            position = song.find("td", class_="chart-table-position").text
            
            # get title
            title = song.find("strong").text

            # get artist
            artist = song.find("span").text
            artist = artist[3:]

            # get number of streams
            stream_stats = song.find("td", class_="chart-table-streams").text
            
            # consolidate data into dictionary
            song_data = {
                'track_id':track_id,
                'position':position, 
                'song_title':title, 
                'artist':artist, 
                'streams':stream_stats, 
                'region':region, 
                'date':date
                }
            year_data.append(song_data)
            
        return year_data

    def to_dataframe(self, charts):
        # load data into a dataframe and export into a csv file for access
        df = pd.DataFrame(charts)

        # clean columns
        import re

        # clean track_id
        df.track_id = [re.findall('(?<=https\:\/\/open\.spotify\.com\/track\/).*', track)[0] for track in df.track_id]

        # clean position, artist, song_title
        df.position = df.position.astype(int)
        df.artist = [re.sub('["]', '', x) for x in df.artist]
        df.song_title = [re.sub('["]', '', x) for x in df.song_title]

        # clean dates
        if len(df.date.iloc[0].split("--")) == 2:
            df.date = [x.split("--")[1] for x in df.date]
        df.date = df.date.astype('datetime64')
        return df