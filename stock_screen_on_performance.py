#This is my coding...





import yfinance as yf
import pandas as pd

print("Hello from tickerscreen1.py!")

def get_price(ticker, date):
    """Fetch the adjusted close price on or nearest after a given date."""
    data = yf.download(ticker, start=date, end=date, progress=False)
    if data.empty:
        # If the market was closed, fetch next available trading day
        data = yf.download(ticker, start=date, progress=False)
    return data['Adj Close'].iloc[0] if not data.empty else None


def performance_screen(tickers, date1, date2, date3, drop_pct, rise_pct):
    results = []

    for ticker in tickers:
        p1 = get_price(ticker, date1)
        p2 = get_price(ticker, date2)
        p3 = get_price(ticker, date3)

        if None in (p1, p2, p3):
            continue

        # Percent change calculations
        pct_drop   = (p2 - p1) / p1 * 100
        pct_rebound = (p3 - p2) / p2 * 100

        # Check conditions
        if pct_drop <= -abs(drop_pct) and pct_rebound >= rise_pct:
            results.append({
                "Ticker": ticker,
                "Drop % (date1→date2)": pct_drop,
                "Rise % (date2→date3)": pct_rebound,
                "Price1": p1,
                "Price2": p2,
                "Price3": p3,
            })
    print("Second Hello from tickerscreen1.py!")
    return pd.DataFrame(results)
print("Third Hello from tickerscreen1.py!")

# ------------------------------
# Example use
# ------------ ------------------
tickers = ["AAPL", "MSFT", "NVDA", "TSLA", "AMZN"]
# tickers = ["KMB",	"NOK",	"UAL",	"CCL",	"XYL",	"NTRA",	"OTIS",	"CUK",	"SOFI",	"SNDK",	"QSR",	"MDB",	"PCG",	"ACGL",	"BBD",	"BBDO",	"KGC",	"TEVA",	"SLF",	"ODFL",	"KVUE",	"MT",	"LYV",	"EXPE",	"CHT",	"ASX",	"FMX",	"RJF",	"KB",	"ERIC",	"CRDO",	"WDS",	"IR",	"TER",	"NRG",	"HUM",	"VRSK",	"HPE",	"WTW",	"IX",	"LEN",	"LEN.B",	"FOXA",	"WIT",	"FITB",	"MTB",	"CHTR",	"VIK",	"VOD",	"LPLA",	"VICI",	"ROL",	"TME",	"EXE",	"DG",	"NTR",	"SYF",	"K",	"MTD",	"CSGP",	"KHC",	"IBKR",	"EXR",	"FOX",	"TSCO",	"COHR",	"CIEN",	"ADM",	"BE",	"EME",	"ATO",	"FSLR",	"ASTS",	"DTE",	"ALAB",	"BR",	"CQP",	"AEE",	"BRO",	"ULTA",	"BIIB",	"HBAN",	"CBOE",	"AXIA",	"SHG",	"DOV",	"RKLB",	"ZM",	"FE",	"IOT",	"EFX",	"STE",	"MKL",	"PHG",	"FTS",	"DXCM",	"TW",	"VLTO",	"WRB",	"OWL"}

date1 = "2024-04-14"
date2 = "2024-11-05
date3 = "2024-12-05"

drop_threshold = -5   # Must fall at least 10%
rise_threshold = 1   # Must rise at least 5%

df = performance_screen(tickers, date1, date2, date3, drop_threshold, rise_threshold)
print(df)

if df.empty:
    print("No data returned for")
