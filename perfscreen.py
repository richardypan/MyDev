
import yfinance as yf
import pandas as pd

print("Hello from tickerscreen1.py!")

def get_price(ticker, date):
    """Fetch the adjusted close price on or nearest after a given date."""
    # normalize date
    date = pd.to_datetime(date)
    end = date + pd.Timedelta(days=1)

    # Request the single calendar day range (end is exclusive in yfinance)
    data = yf.download(ticker,
                       start=date.strftime('%Y-%m-%d'),
                       end=end.strftime('%Y-%m-%d'),
                       progress=False,
                       auto_adjust=False)

    if data.empty:
        # If no data for that day (market closed), fetch a small forward window
        window_end = (date + pd.Timedelta(days=7)).strftime('%Y-%m-%d')
        data = yf.download(ticker,
                           start=date.strftime('%Y-%m-%d'),
                           end=window_end,
                           progress=False,
                           auto_adjust=False)

    if data.empty:
        return None

    def _to_scalar(val):
        if pd.isna(val):
            return None
        try:
            return float(val)
        except Exception:
            try:
                return float(val.item())
            except Exception:
                return val

    # Look at the first available row and pick the best-matching column.
    row = data.iloc[0]

    # Handle MultiIndex or single-level index for columns
    if isinstance(row.index, pd.MultiIndex):
        for idx in row.index:
            if idx[-1] == 'Adj Close':
                return _to_scalar(row[idx])
        for idx in row.index:
            if idx[-1] == 'Close':
                return _to_scalar(row[idx])
    else:
        for name in ('Adj Close', 'Close'):
            if name in row.index:
                return _to_scalar(row[name])

    # Fallback: return the first numeric value in the row
    for name, val in row.items():
        if pd.api.types.is_number(val) or pd.api.types.is_numeric_dtype(type(val)):
            return _to_scalar(val)

    return None


def performance_screen(tickers, date1, date2, date3, drop_pct, rise_pct, verbose=False):
    results = []

    for ticker in tickers:
        p1 = get_price(ticker, date1)
        p2 = get_price(ticker, date2)
        p3 = get_price(ticker, date3)

        if verbose:
            print(f"Ticker {ticker}: p1={p1!s}, p2={p2!s}, p3={p3!s}")

        if None in (p1, p2, p3):
            if verbose:
                missing = [name for name, val in (('p1', p1), ('p2', p2), ('p3', p3)) if val is None]
                print(f"  -> Skipped: missing {', '.join(missing)}")
            continue

        # Percent change calculations
        pct_drop = (p2 - p1) / p1 * 100
        pct_rebound = (p3 - p2) / p2 * 100

        if verbose:
            print(f"  pct_drop={pct_drop:.2f}%, pct_rebound={pct_rebound:.2f}%")

        # Check conditions
        if pct_drop <= -abs(drop_pct) and pct_rebound >= rise_pct:
            if verbose:
                print("  -> Matched filter — adding to results")
            results.append({
                "Ticker": ticker,
                "Drop % (date1→date2)": pct_drop,
                "Rise % (date2→date3)": pct_rebound,
                "Price1": p1,
                "Price2": p2,
                "Price3": p3,
            })
        else:
            if verbose:
                reasons = []
                if not (pct_drop <= -abs(drop_pct)):
                    reasons.append(f"drop condition failed (need <= -{abs(drop_pct)}%)")
                if not (pct_rebound >= rise_pct):
                    reasons.append(f"rebound condition failed (need >= {rise_pct}%)")
                print(f"  -> Skipped: {', '.join(reasons)}")

    return pd.DataFrame(results)
#print("Third Hello from tickerscreen1.py!")

# ------------------------------
# Example use
# ------------ ------------------
def _example_run():
    #tickers = ["AAPL", "MSFT", "NVDA", "TSLA", "AMZN"]
    tickers = ["KMB",	"NOK",	"UAL",	"CCL",	"XYL",	"NTRA",	"OTIS",	"CUK",	"SOFI",	"SNDK",	"QSR",	"MDB",	"PCG",	"ACGL",	"BBD",	"BBDO",	"KGC",	"TEVA",	"SLF",	"ODFL",	"KVUE",	"MT",	"LYV",	"EXPE",	"CHT",	"ASX",	"FMX",	"RJF",	"KB",	"ERIC",	"CRDO",	"WDS",	"IR",	"TER",	"NRG",	"HUM",	"VRSK",	"HPE",	"WTW",	"IX",	"LEN",	"LEN.B",	"FOXA",	"WIT",	"FITB",	"MTB",	"CHTR",	"VIK",	"VOD",	"LPLA",	"VICI",	"ROL",	"TME",	"EXE",	"DG",	"NTR",	"SYF",	"K",	"MTD",	"CSGP",	"KHC",	"IBKR",	"EXR",	"FOX",	"TSCO",	"COHR",	"CIEN",	"ADM",	"BE",	"EME",	"ATO",	"FSLR",	"ASTS",	"DTE",	"ALAB",	"BR",	"CQP",	"AEE",	"BRO",	"ULTA",	"BIIB",	"HBAN",	"CBOE",	"AXIA",	"SHG",	"DOV",	"RKLB",	"ZM",	"FE",	"IOT",	"EFX",	"STE",	"MKL",	"PHG",	"FTS",	"DXCM",	"TW",	"VLTO",	"WRB",	"OWL"]

    date1 = "2025-04-14"
    date2 = "2025-11-05"
    date3 = "2025-12-05"

    drop_threshold = 5   # Minimum percent drop (positive value, e.g. 5 means 5%)
    rise_threshold = 1   # Minimum percent rise (percent, e.g. 1 means 1%)

    df = performance_screen(tickers, date1, date2, date3, drop_threshold, rise_threshold, verbose=True)
    print(df)

   # if df.empty:
   #     print("No data returned")


if __name__ == '__main__':
    _example_run()


