"""Visualize the data."""

import pandas as pd
from pathlib import Path


def main():
    # get the latest downloaded dataset
    csv_file = sorted((Path(__file__).parents[2] / "data/raw").glob("*.csv"))[-1]
    print(csv_file)
    df = pd.read_csv(csv_file)

    # preprocess the dataframe
    keep_columns = [
        "name",
        "distance",
        "moving_time",
        "elapsed_time",
        "total_elevation_gain",
        "type",
        "sport_type",
        "workout_type",
        "start_date",
        "start_date_local",
        "average_speed",
        "max_speed",
        "average_cadence",
        "average_heartrate",
        "max_heartrate",
        "elev_high",
        "elev_low",
    ]

    df = df[keep_columns]
    print(len(df))

    df.start_date_local = pd.to_datetime(df.start_date_local)
    week_agg = df.resample(rule='W', on='start_date_local')['distance'].sum()

    import plotly.express as px
    import plotly.graph_objects as go
    import plotly.subplots
    import plotly.io

    MILE_CONST = 1609.3435021011532626
    df["hrrs"] = df.average_speed / df.average_heartrate * 1e6

    week_agg = pd.concat(
        [
            df.resample(rule="W", on="start_date_local")["distance"].sum(),
            df.resample(rule="W", on="start_date_local")["hrrs"].mean(),
        ],
        axis=1,
    )

    week_agg_filt = week_agg.loc[week_agg.index > "2020"]
    # week_agg_filt = week_agg_filt.loc[week_agg_filt.distance > 0]
    week_agg_filt = week_agg_filt / MILE_CONST

    fig = plotly.subplots.make_subplots(rows=2, cols=1)
    fig.add_trace(go.Scatter(x=week_agg_filt.index, y=week_agg_filt.distance), row=1, col=1)
    fig.add_trace(
        go.Scatter(x=week_agg_filt.index, y=week_agg_filt.hrrs, mode="markers"),
        row=2,
        col=1,
    )

    output_folder = Path(__file__).parents[2] / "reports/figures"
    fig.write_html(output_folder / "test.html")
    fig.write_image(output_folder / "test.png")


if __name__ == "__main__":
    main()
