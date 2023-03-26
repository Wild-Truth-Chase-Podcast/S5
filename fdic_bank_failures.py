"""
An example of using the FDIC API failure endpoint
"""
from loguru import logger
from pathlib import Path
import requests
import pandas as pd
import plotly.express as px


def get_data():
    """Get failure data"""
    fromyr = 1900
    toyr = 2023
    fields = "NAME,CERT,FIN,CITYST,FAILYR,FAILDATE,SAVR,RESTYPE,RESTYPE1,QBFDEP,QBFASSET,COST"
    limit = 10_000
    totals = "QBFDEP,QBFASSET,COST"
    agg_sum_fields = "QBFASSET,QBFDEP,COST"

    root = "https://banks.data.fdic.gov/api/failures"
    url = f'{root}?filters=FAILYR:["{fromyr}" TO "{toyr}"]&fields={fields}'
    url += "&sort_by=FAILDATE&sort_order=DESC"
    url += f"&limit={limit}&offset=0"
    # url += '&total_fields={totals}&subtotal_by=RESTYPE'
    # url += '&agg_by=FAILYR&agg_term_fields=RESTYPE&agg_sum_fields={agg_sum_fields}&agg_limit=120'
    logger.info(url)

    response = requests.get(url)
    results = response.json()
    results = [x["data"] for x in results["data"]]
    df = pd.DataFrame.from_records(results)
    return df.sort_values("FAILYR")


csv_path = Path("FDIC", "data", "failures.csv")
overwrite = False
if overwrite or not csv_path.exists():
    logger.info("No existing data found, calling API")
    df = get_data()
    df.to_csv(csv_path)
else:
    logger.info("Data found on disk, reading data")
    df = pd.read_csv(csv_path)

print(df)
# do some grouping
df["FAILDATE"] = pd.to_datetime(df["FAILDATE"])
grouped = df.groupby(pd.Grouper(key="FAILDATE", axis=0, freq="3M"))
monthly_counts = grouped.count()
print(monthly_counts)
# plot
fig = px.bar(monthly_counts, y="ID")
fig.show()
