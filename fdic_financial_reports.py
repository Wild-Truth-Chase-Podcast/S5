"""
An example of using the FDIC API financials endpoint
"""
from loguru import logger
from pathlib import Path
import requests
import pandas as pd
import matplotlib.pyplot as plt


def get_data():
    """Get financials data"""
    bank = "SILICON VALLEY BANK"
    fields = "NAME,STNAME,REPYEAR,RISDATE,REPDTE,ASSET,LIAB"
    limit = 200

    root = 'https://banks.data.fdic.gov/api/financials'
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
plt.figure()
plt.semilogy(df["REPDTE"], df["ASSET"], label="total assets")
plt.semilogy(df["REPDTE"], df["LIAB"], label="total liabilities")
plt.legend(loc="upper left")
plt.twinx()
plt.bar(df["REPDTE"], df["DIFF"], label="Assets - Liabilities")
plt.gca().set_yscale("log")
plt.legend(loc="upper right")


plt.figure()
# plt.bar(df.index, df["DIFF"])
plt.bar(df.index, (df["DIFF"] / df["ASSET"]) * 100)

plt.show()
