# Theta Data V3: Master Documentation Summary

## 1. Connection Standards
- **Local Port:** 25503 (V3 Default)
- **Base REST URL:** `http://127.0.0.1:25503/v3/`
- **Python Setup:** `client = ThetaClient(port=25503)`
- **Authentication:** Place `creds.txt` in the terminal directory. 
  - Line 1: Email
  - Line 2: Password

## 2. Global V3 Logic Changes
- **No Pagination:** All data is returned in a single response. Do not use `page` parameters or "next-page" logic.
- **REST Only:** Real-time streaming is currently handled via V2 (Port 25510). V3 is for Snapshots and History.
- **Data Formats:** Use `ndjson` for large datasets to pipe directly into Pandas:
  `df = pd.read_json("URL", lines=True)`

## 3. Market Data Endpoints (Equities & ETFs)
- **Quotes:** `/v3/market/quote?symbol=TICKER`
- **Trade History:** `/v3/market/history?symbol=TICKER&interval=1m&start_date=YYYYMMDD`
- **OHLC:** Includes Open, High, Low, Close, Volume, and Count.

## 4. Options Data Endpoints
- **Expirations:** `/v3/market/expirations?symbol=TICKER` (Returns list of YYYYMMDD).
- **Strikes:** `/v3/market/strikes?symbol=TICKER&expiration=YYYYMMDD`
- **Option History:** `/v3/market/history?symbol=TICKER&expiration=YYYYMMDD&strike=PRICE&right=C/P&interval=1m`
- **Greeks Snapshot:** `/v3/market/greeks?symbol=TICKER&expiration=YYYYMMDD` (Returns greeks for the entire chain).

## 5. Technical Requirements & Error Handling
- **Java:** Version 17+ (Ubuntu)
- **Python:** `thetadata` SDK (latest version)
- **Error 410 (Gone):** Occurs when a V2 endpoint path is used. Change `/v2/` to `/v3/`.
- **Error 400 (Bad Request):** Usually an invalid date format (Use YYYYMMDD) or invalid strike.
- **Error 405:** Method Not Allowed; check if you are using GET vs POST correctly.

## 6. Performance Tips
- Use `interval=1d` for long-term historical analysis to reduce payload size.
- For bulk data (entire option chains), always prefer `ndjson` over standard `json`.
