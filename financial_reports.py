import requests
import pandas as pd
import matplotlib.pyplot as plt


url = 'https://banks.data.fdic.gov/api/financials?filters=NAME:"SILICON VALLEY BANK"&fields=NAME,STNAME,REPYEAR,RISDATE,REPDTE,ASSET,LIAB&limit=200'


response = requests.get(url)
results = response.json()
results = [x["data"] for x in results["data"]]
df = pd.DataFrame.from_records(results)
df["REPDTE"] = pd.to_datetime(df["REPDTE"])
df["RISDATE"] = pd.to_datetime(df["RISDATE"])
df["REPYEAR"] = pd.to_datetime(df["REPYEAR"])
df["DIFF"] = df["ASSET"] - df["LIAB"]
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
plt.bar(df.index, (df["DIFF"] / df["ASSET"])*100)

plt.show()
