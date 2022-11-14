"""Download data from strava."""

import json
import requests
from pathlib import Path
from datetime import datetime

import pandas as pd


def main():

    # Read the token from the saved file
    with open((Path(__file__).parent / "tokens.json"), "r") as fp:
        data = json.load(fp)

    # Get the access token
    access_token = data["access_token"]

    activities_url = "https://www.strava.com/api/v3/athlete/activities"

    page = 1
    max_page = 5

    entries = []
    while page < max_page:
        r = requests.get(
            f"{activities_url}?access_token={access_token}&per_page=200&page={page}"
        )
        if not r.json():
            break
        entries.extend(r.json())
        page += 1

    df = pd.DataFrame(entries)
    out_file = Path(__file__).parents[2] / "data/raw" / datetime.now().strftime("%Y%m%d-T%H%M%S_download.csv")
    df.to_csv(out_file)

if __name__ == "__main__":
    main()
