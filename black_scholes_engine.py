import numpy as np
import pandas as pd
from scipy.stats import norm
from scipy.optimize import root_scalar

# /opt/anaconda3/bin/python3 /Users/aurokrishnaaravindranlakshmi/Documents/black_scholes_dashboard/black_scholes_engine.py

# -------------------------
# Black-Scholes Price
# -------------------------
def black_scholes_price(S, K, T, r, sigma, option_type='call'):
    if T <= 0 or sigma <= 0:
        return 0.0
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type.lower() == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type.lower() == 'put':
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("Invalid option type. Use 'call' or 'put'.")
    return price

# -------------------------
# Full Greeks
# -------------------------
def calculate_greeks(S, K, T, r, sigma, option_type='call'):
    if T <= 0 or sigma <= 0:
        return 0.0, 0.0, 0.0, 0.0, 0.0

    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type.lower() == 'call':
        delta = norm.cdf(d1)
        theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) 
                 - r * K * np.exp(-r * T) * norm.cdf(d2)) / 365
        rho = K * T * np.exp(-r * T) * norm.cdf(d2) / 100
    elif option_type.lower() == 'put':
        delta = norm.cdf(d1) - 1
        theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) 
                 + r * K * np.exp(-r * T) * norm.cdf(-d2)) / 365
        rho = -K * T * np.exp(-r * T) * norm.cdf(-d2) / 100
    else:
        raise ValueError("Invalid option type")

    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T) / 100

    return delta, gamma, vega, theta, rho

# -------------------------
# P&L Calculator
# -------------------------
def calculate_pnl(S, K, T, r, sigma, purchase_price, option_type='call'):
    current_value = black_scholes_price(S, K, T, r, sigma, option_type)
    return current_value - purchase_price

# -------------------------
# Sensitivity Grid: Option Price
# -------------------------
def generate_price_grid(S_range, vol_range, K, T, r, option_type='call'):
    grid = []
    for sigma in vol_range:
        row = []
        for S in S_range:
            price = black_scholes_price(S, K, T, r, sigma, option_type)
            row.append(price)
        grid.append(row)

    df = pd.DataFrame(grid, index=[f"{v:.2f}" for v in vol_range], columns=[f"{s:.2f}" for s in S_range])
    df.index.name = 'Volatility'
    df.columns.name = 'Stock Price'
    return df

# -------------------------
# Sensitivity Grid: P&L
# -------------------------
def generate_pnl_grid(S_range, vol_range, K, T, r, purchase_price, option_type='call'):
    grid = []
    for sigma in vol_range:
        row = []
        for S in S_range:
            price = black_scholes_price(S, K, T, r, sigma, option_type)
            pnl = price - purchase_price
            row.append(pnl)
        grid.append(row)

    df = pd.DataFrame(grid, index=[f"{v:.2f}" for v in vol_range], columns=[f"{s:.2f}" for s in S_range])
    df.index.name = 'Volatility'
    df.columns.name = 'Stock Price'
    return df

# -------------------------
# Implied Volatility Calculator
# -------------------------
def implied_volatility(market_price, S, K, T, r, option_type='call'):
    def objective(sigma):
        if sigma <= 0:
            return market_price
        price = black_scholes_price(S, K, T, r, sigma, option_type)
        return price - market_price

    try:
        result = root_scalar(objective, bracket=[1e-5, 3], method='brentq')
        return result.root if result.converged else None
    except:
        return None

# -------------------------
# Example Test Block
# -------------------------
if __name__ == "__main__":
    # Example input values
    S = 100
    K = 100
    T = 1
    r = 0.05
    sigma = 0.2
    option_type = 'call'
    purchase_price = 8

    # Pricing
    price = black_scholes_price(S, K, T, r, sigma, option_type)
    print(f"\nOption Price: ${price:.2f}")

    # Greeks
    delta, gamma, vega, theta, rho = calculate_greeks(S, K, T, r, sigma, option_type)
    print(f"Delta: {delta:.4f}, Gamma: {gamma:.4f}, Vega: {vega:.4f}, Theta: {theta:.4f}, Rho: {rho:.4f}")

    # P&L
    pnl = calculate_pnl(S, K, T, r, sigma, purchase_price, option_type)
    print(f"P&L: ${pnl:.2f}")

    # Implied Volatility
    iv = implied_volatility(market_price=10, S=S, K=K, T=T, r=r, option_type=option_type)
    print(f"Implied Volatility: {iv:.4f}")

    # Sensitivity Grid
    S_range = np.linspace(80, 120, 10)
    vol_range = np.linspace(0.1, 0.5, 10)

    df_price_grid = generate_price_grid(S_range, vol_range, K, T, r, option_type)
    df_pnl_grid = generate_pnl_grid(S_range, vol_range, K, T, r, purchase_price, option_type)

    print("\nOption Price Grid (Preview):")
    print(df_price_grid.head())

    print("\nP&L Grid (Preview):")
    print(df_pnl_grid.head())




