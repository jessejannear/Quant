# ThetaData v3 API Reference

This document outlines the key endpoints and usage for the ThetaData v3 REST API, as used in this project.

## Base URL
All requests are made to the local Theta Terminal instance:
`http://127.0.0.1:25503`

## Authentication
Authentication is handled by the Theta Terminal software. No API keys are required in the HTTP requests themselves.

## Endpoints

### 1. Stock / Option Roots
Retrieves the list of available option roots (symbols).

- **Endpoint**: `/v3/option/list/symbols`
- **Method**: `GET`
- **Parameters**:
    - `format`: Response format (default: `csv`, options: `json`, `ndjson`, `html`).
- **Example Response** (CSV):
    ```
    symbol
    "AAPL"
    "MSFT"
    ...
    ```

### 2. Expirations
Retrieves available expiration dates for a specific root.

- **Endpoint**: `/v3/option/list/expirations`
- **Method**: `GET`
- **Parameters**:
    - `symbol`: The root symbol (e.g., `AAPL`).
- **Returns**: List of dates in `YYYYMMDD` format.

### 3. Strikes
Retrieves available strike prices for a specific root and expiration.

- **Endpoint**: `/v3/option/list/strikes`
- **Method**: `GET`
- **Parameters**:
    - `symbol`: The root symbol (e.g., `AAPL`).
    - `expiration`: Expiration date in `YYYYMMDD` format.
- **Returns**: List of strike prices (e.g., `680.000`).

### 4. Historical Data (OHLC)
Retrieves historical Open-High-Low-Close data for a specific option contract.

- **Endpoint**: `/v3/option/history/ohlc`
- **Method**: `GET`
- **Parameters**:
    - `symbol`: Root symbol.
    - `expiration`: Expiration date (`YYYYMMDD`).
    - `strike`: Strike price in dollars (e.g., `680` for $680).
    - `right`: `C` (Call) or `P` (Put).
    - `interval`: Time interval (e.g., `1m`, `5m`, `1h`, `1d`).
    - `start_date` (optional): `YYYYMMDD`.
    - `end_date` (optional): `YYYYMMDD`.

### 5. Config / Snapshot
Retrieves current market data snapshot.

- **Endpoint**: `/v3/option/snapshot/quote`
- **Method**: `GET`
- **Parameters**:
    - `symbol`: Root symbol.
    - `expiration`: Expiration date.
    - `strike`: Strike price.
    - `right`: `C` or `P`.

### 6. Greeks
Retrieves current Greeks (Delta, Gamma, Theta, etc.).

- **Endpoint**: `/v3/option/snapshot/greeks/all`
- **Method**: `GET`
- **Parameters**: Same as Quote.

## Error Handling
- **404 Not Found**: Endpoint incorrect or data not found.
- **410 Gone**: Deprecated endpoint (v2 endpoints return this on v3 port).
- **Connection Refused**: Theta Terminal is not running.
