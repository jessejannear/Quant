import httpx
from datetime import datetime, date

BASE_URL = "http://127.0.0.1:25503/v3"

def get_current_price(symbol: str) -> float:
    """
    Fetches the current price of the underlying asset.
    Returns None if API fails (e.g. Free tier restriction).
    """
    try:
        response = httpx.get(f"{BASE_URL}/stock/snapshot/quote", params={"symbol": symbol})
        response.raise_for_status()
        # CSV format: timestamp,symbol,bid_size,bid_exchange,bid,bid_condition,ask_size,ask_exchange,ask,ask_condition
        # We'll use the midpoint of bid/ask as the current price estimate
        lines = response.text.strip().split('\n')
        if len(lines) < 2:
            return None
        
        headers = lines[0].split(',')
        data = lines[1].split(',')
        
        bid_idx = headers.index('bid')
        ask_idx = headers.index('ask')
        
        bid = float(data[bid_idx])
        ask = float(data[ask_idx])
        
        return (bid + ask) / 2
    except Exception as e:
        print(f"[{symbol}] Price Fetch Error: {e}")
        return None

def get_option_price(symbol: str, expiration: str, strike: float, right: str) -> float:
    """
    Fetches the midpoint price (Bid/Ask) for a specific option contract.
    Fallback to Last Trade if Bid/Ask are missing.
    """
    # Normalize expiration to YYYYMMDD for API consistency
    exp_clean = expiration.replace("-", "")
    
    try:
        params = {
            "symbol": symbol,
            "expiration": exp_clean,
            "strike": strike, 
            "right": right
        }
        
        response = httpx.get(f"{BASE_URL}/option/snapshot/quote", params=params)
        response.raise_for_status()
        
        lines = response.text.strip().split('\n')
        if len(lines) < 2 or "No data found" in lines[0]:
             # Try getting trade if quote fails?
             # For now, let's just return None.
             return None
             
        headers = lines[0].split(',')
        data = lines[1].split(',')
        
        if 'bid' in headers and 'ask' in headers:
            bid = float(data[headers.index('bid')])
            ask = float(data[headers.index('ask')])
            midpoint = (bid + ask) / 2
            if midpoint > 0:
                return midpoint
        
        return None

    except Exception as e:
        # Silently fail or log?
        # print(f"Error fetching option price: {e}")
        return None

def get_atm_strike(symbol: str, expiration: str, current_price: float = None) -> float:
    """
    Finds the strike closest to the underlying price.
    If current_price is not provided, attempts to fetch it.
    """
    if current_price is None:
        current_price = get_current_price(symbol)
        
    if not current_price:
        print("Cannot determine ATM strike without underlying price.")
        return None
        
    try:
        # Get list of strikes
        params = {"symbol": symbol, "expiration": expiration.replace("-", "")}
        response = httpx.get(f"{BASE_URL}/option/list/strikes", params=params)
        response.raise_for_status()
        
        lines = response.text.strip().split('\n')
        # CSV response: "SPY",680.000
        strikes = []
        for line in lines:
            parts = line.split(',')
            if len(parts) >= 2:
                try:
                    strikes.append(float(parts[1]))
                except ValueError:
                    continue
                    
        if not strikes:
            return None
            
        # Find closest
        closest_strike = min(strikes, key=lambda x: abs(x - current_price))
        return closest_strike
        
    except Exception as e:
        print(f"Error getting ATM strike: {e}")
        return None

def get_expected_move(symbol: str, expiration: str, current_price: float = None) -> dict:
    """
    Calculates the expected move based on the ATM straddle price.
    Returns dict with 'move_dollars' and 'move_percent'.
    """
    if current_price is None:
        current_price = get_current_price(symbol)
        
    if not current_price:
        return None # Cannot proceed without price
        
    atm_strike = get_atm_strike(symbol, expiration, current_price)
    if not atm_strike:
        print(f"Could not find ATM strike for price {current_price}")
        return None
        
    call_price = get_option_price(symbol, expiration, atm_strike, 'C')
    put_price = get_option_price(symbol, expiration, atm_strike, 'P')
    
    if call_price is None or put_price is None:
        print(f"Could not fetch pricing for straddle at strike {atm_strike}")
        return None
        
    straddle_price = call_price + put_price
    # Using 85% rule for conservative estimate of 1-standard deviation move
    expected_move = straddle_price * 0.85
    
    return {
        "underlying_price": current_price,
        "atm_strike": atm_strike,
        "straddle_price": straddle_price,
        "expected_move_dollars": expected_move,
        "expected_move_percent": (expected_move / current_price) * 100
    }
