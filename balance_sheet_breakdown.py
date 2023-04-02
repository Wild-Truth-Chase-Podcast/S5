from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

summary_path = Path("balance_sheets", "summary.csv")
df = pd.read_csv(summary_path, skiprows=2, index_col=0)
df = df.transpose()
df = df.sort_index()
# get a nice year column
df["Year Ending"] = df.index

assets = [
    "Cash and cash equivalents",
    "Available-for-sale securities, at fair value",
    "Held-to-maturity securities",
    "Non-marketable and other equity securities",
    "Net loans",
    "Premises and equipment, net of accumulated depreciation and amortization",
    "Goodwill",
    "Other intangible assets, net",
    "Lease right-of-use assets",
    "Accrued interest receivable and other assets",
]

liabilities = [
    "Noninterest-bearing demand deposits",
    "Interest-bearing deposits",
    "Total deposits",
    "Short-term borrowings",
    "Lease liabilities",
    "Other liabilities",
    "Long-term debt",
]


# normalise assets by total assets 
for asset in assets:
    df[asset] = (df[asset] / df["Total assets"])*100

# draw an area graph
fig = go.Figure()
for asset in assets:
    fig.add_trace(go.Scatter(
        x=df["Year Ending"], y=df[asset],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5),
        stackgroup='one',
        name=asset
    ))
fig.update_layout(yaxis_range=(0, 100))
fig.show()

# normalise liabilities by total liabilities 
for liability in liabilities:
    df[liability] = (df[liability] / df["Total liabilities"])*100

fig = go.Figure()
for liability in liabilities:
    fig.add_trace(go.Scatter(
        x=df["Year Ending"], y=df[liability],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5),
        stackgroup='one',
        name=liability
    ))
fig.update_layout(yaxis_range=(0, 100))
fig.show()


