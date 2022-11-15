"""Download data from Strava."""

import json
import logging
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests

logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).parents[2]
DATA_DIR = ROOT_DIR / "data"
TOKEN_FILE = Path(__file__).parent / "tokens.json"


def get_activities(token, max_requests=5):
    """Get activities from Strava."""
    activities_url = "https://www.strava.com/api/v3/athlete/activities"

    page = 1
    activities = []
    while page < max_requests:
        r = requests.get(
            f"{activities_url}?access_token={token}&per_page=200&page={page}"
        )
        if not r.json():
            break
        activities.extend(r.json())
        page += 1
    logger.info(f"Downloaded {len(activities)} workout entries")
    return activities


def load_token():
    try:
        with open(TOKEN_FILE, "r") as fp:
            data = json.load(fp)
        return data
    except FileNotFoundError as e:
        logger.info(f"No token file exists at {TOKEN_FILE}")
        return


def check_needs_refresh():
    data = load_token()
    expires_at = data["expires_at"]
    now = time.time()
    if now > expires_at:
        return True
    else:
        return False


def main():
    if check_needs_refresh():
        logger.info("Access token needs refresh, re-run connect_strava.py script")
        return

    # Read token from file
    data = load_token()
    access_token = data["access_token"]
    # Download activities from Strava
    activities = get_activities(access_token)
    # Load into a dataframe for easy export
    df = pd.DataFrame(activities)
    # Export activities to csv
    fname = datetime.now().strftime("%Y%m%d-T%H%M%S_activities.csv")
    fpath = DATA_DIR / "raw" / fname
    df.to_csv(fpath)

    logger.info(f"Wrote activities to {fpath.absolute()}")


if __name__ == "__main__":
    main()
