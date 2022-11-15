"""Get access token from Strava API."""

import json
import logging
import re
import subprocess
from pathlib import Path

import requests
from config import CLIENT_ID, CLIENT_SECRET
from flask import Flask, request

logger = logging.getLogger(__name__)

app = Flask(__name__)

TOKEN_FILE = Path(__file__).parent.absolute() / "tokens.json"

@app.route("/")
def index():
    """Extract code from URL and save tokens to file."""

    # Find code in the URL
    code = re.findall(r"&code=(.+)&", request.url)[0]
    # Check that a code was found
    if not code:
        logger.error("Access code not found.")
        return "Access code not found"
    # Generate the POST data
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
    }
    # get token from Strava
    tokens = requests.post(
        url="https://www.strava.com/oauth/token",
        data=data,
    )

    # Save json response as a variable
    with open(TOKEN_FILE, "w") as fp:
        json.dump(tokens.json(), fp)
        logger.info(f"Written to {TOKEN_FILE}")

    return f"Written to {TOKEN_FILE}. You may now close this window and shut down the server."


if __name__ == "__main__":
    # Initial Settings
    redirect_uri = "http://127.0.0.1:5000/"
    # Authorization URL
    request_url = (
        f"http://www.strava.com/oauth/authorize?client_id={CLIENT_ID}"
        f"&response_type=code&redirect_uri={redirect_uri}"
        f"&approval_prompt=force"
        f"&scope=profile:read_all,activity:read_all"
    )

    subprocess.run(["open", "-a", "Safari", request_url])
    print("Please visit this url:", request_url)

    app.run()
