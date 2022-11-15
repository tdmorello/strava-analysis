"""Nox sessions."""

import nox
from nox.sessions import Session
import subprocess

from pathlib import Path

ROOT_DIR = Path(__file__).parent
SRC_DIR = ROOT_DIR / "src"

@nox.session
def refresh_token(session: Session) -> None:
    """Refresh access token for Strava API"""
    subprocess.run(["python", SRC_DIR / "data/connect_strava.py"])

@nox.session
def download_data(session: Session) -> None:
    """Download data from Strava"""
    subprocess.run(["python", SRC_DIR / "data/download_data.py"])

@nox.session
def run_analysis(session: Session) -> None:
    """Plot and save figures"""
    subprocess.run(["python", SRC_DIR / "visualization/visualize.py", *session.posargs])
