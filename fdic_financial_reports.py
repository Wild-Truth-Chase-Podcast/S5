"""
An example of using the FDIC API financials endpoint
"""
from loguru import logger
from pathlib import Path
import requests
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def get_data():
    """Get financials data"""
    bank = "SILICON VALLEY BANK"
    fields = "NAME,STNAME,REPYEAR,RISDATE,REPDTE"
    # add fields about assets
    fields += ",ASSET"
    # add fields about liabilities
    fields += ",DEP,LIAB"
    # add any other fields
    fields += ""
    limit = 200

    root = "https://banks.data.fdic.gov/api/financials"
    url = f'{root}?filters=NAME:"{bank}"&fields={fields}&limit={limit}'
    logger.info(url)

    response = requests.get(url)
    results = response.json()
    results = [x["data"] for x in results["data"]]
    df = pd.DataFrame.from_records(results)
    df["REPDTE"] = pd.to_datetime(df["REPDTE"])
    df["RISDATE"] = pd.to_datetime(df["RISDATE"])
    df["REPYEAR"] = pd.to_datetime(df["REPYEAR"])
    df["DIFF"] = df["ASSET"] - df["LIAB"]
    return df


csv_path = Path("FDIC", "data", "financials.csv")
overwrite = False
if overwrite or not csv_path.exists():
    logger.info("No existing data found, calling API")
    df = get_data()
    df.to_csv(csv_path)
else:
    logger.info("Data found on disk, reading data")
    df = pd.read_csv(csv_path)


print(df)
fig = make_subplots(rows=2, cols=1, shared_xaxes=True)
fig.add_trace(
    go.Scatter(
        x=df["REPDTE"],
        y=df["ASSET"],
        mode="lines+markers",
        name="Total assets",
    ),
    row=1,
    col=1,
)
fig.add_trace(
    go.Scatter(
        x=df["REPDTE"],
        y=df["LIAB"],
        mode="lines+markers",
        name="Total liabilities",
    ),
    row=1,
    col=1,
)
fig.add_trace(
    go.Bar(
        x=df["REPDTE"],
        y=(df["LIAB"] / df["ASSET"]) * 100,
        name="Liabilities/Assets",
    ),
    row=2,
    col=1,
)
fig.update_layout(
    yaxis=dict(title="Dollars $", type="log"), yaxis2=dict(title="Liabilities/Assets %")
)
fig.show()
