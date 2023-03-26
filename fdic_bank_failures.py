import requests
import pandas as pd
import matplotlib.pyplot as plt

fromyr = 1900
toyr = 2023
fields = "NAME,CERT,FIN,CITYST,FAILDATE,SAVR,RESTYPE,RESTYPE1,QBFDEP,QBFASSET,COST"
totals = "QBFDEP,QBFASSET,COST"
agg_sum_fields = "QBFASSET,QBFDEP,COST"

root = "https://banks.data.fdic.gov/api/failures"
url = f'{root}?filters=FAILYR:["{fromyr}" TO "{toyr}"]&fields={fields}&sort_by=FAILDATE&sort_order=DESC&limit=2000&offset=0&total_fields={totals}'
url += "&subtotal_by=RESTYPE"
url += "&agg_by=FAILYR&agg_term_fields=RESTYPE&agg_sum_fields={agg_sum_fields}&agg_limit=120"
print(url)

response = requests.get(url)
results = response.json()
results = [x["data"] for x in results["data"]]
df = pd.DataFrame.from_records(results)
df = df.sort_values("FAILYR")
print(df)

plt.plot(df["FAILYR"], df["count"])
plt.xticks(rotation = 45)
plt.show()