# make_dataset.py

import json

import requests
from flask import Flask, request
import re
import subprocess
from pathlib import Path

from config import CLIENT_ID, CLIENT_SECRET

import logging

logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def index():
    code = re.findall(r'&code=(.+)&', request.url)[0]
    tokens = requests.post(
        url="https://www.strava.com/oauth/token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
        },
    )
    # Save json response as a variable
    token_file = Path(__file__).parent.absolute() / "tokens.json"
    with open(token_file, "w") as fp:
        json.dump(tokens.json(), fp)
        logger.info(f"Wrote to {token_file}")

    return f'Written to {token_file}. You may now close this window.'


if __name__ == '__main__':
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
