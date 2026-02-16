from src.quant_utils import get_current_price, get_option_price, get_expected_move

def test_spy():
    symbol = "SPY"
    expiration = "2026-02-17" # Tomorrow
    manual_price = 680.0 # Approximate price based on previous steps
    
    print(f"--- Testing {symbol} ---")
    
    # 1. Price (Will likely fail on Free tier, verify graceful failure)
    price = get_current_price(symbol)
    if price:
         print(f"Current Price (API): {price}")
    else:
         print(f"Current Price (API): Failed (Expected on Free Tier)")
         print(f"Using Manual Price: {manual_price}")

    # 2. Specific Option
    strike = 680
    call_price = get_option_price(symbol, expiration, strike, 'C')
    print(f"Call {strike} Exp {expiration}: {call_price}")
    
    # 3. Expected Move (Injecting manual price)
    move = get_expected_move(symbol, expiration, current_price=manual_price)
    if move:
        print(f"ATM Strike: {move['atm_strike']}")
        print(f"Straddle Cost: {move['straddle_price']:.2f}")
        print(f"Expected Move: +/- ${move['expected_move_dollars']:.2f} ({move['expected_move_percent']:.2f}%)")
    else:
        print("Could not calculate expected move")

if __name__ == "__main__":
    test_spy()
