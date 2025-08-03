import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from black_scholes_engine import (
    black_scholes_price,
    calculate_greeks,
    calculate_pnl,
    generate_price_grid,
    generate_pnl_grid,
    implied_volatility
)

# -------------------- Page Setup --------------------
st.set_page_config(page_title="Black-Scholes Dashboard", layout="wide")
st.markdown("<h1 style='text-align: center;'> Black-Scholes Option Pricing Dashboard - Auro</h1>", unsafe_allow_html=True)
st.write("")  # spacing

# -------------------- Sidebar --------------------
st.sidebar.markdown("## ⚙️ Model Inputs")
st.sidebar.markdown("Adjust parameters below to calculate option price and Greeks.")

S = st.sidebar.number_input("**Stock Price (S)**", value=100.0)
K = st.sidebar.number_input("**Strike Price (K)**", value=100.0)
T = st.sidebar.number_input("**Time to Maturity (T, years)**", value=1.0, min_value=0.001)
sigma = st.sidebar.number_input("**Volatility (σ)**", value=0.2, min_value=0.001)
r = st.sidebar.number_input("**Risk-Free Rate (r)**", value=0.05)
option_type = st.sidebar.radio("**Option Type**", ["call", "put"])
purchase_price = st.sidebar.number_input("**Purchase Price**", value=8.00)
market_price = st.sidebar.number_input("**Observed Market Price (for IV)**", value=10.00)

# -------------------- Test Case --------------------
with st.expander("🧪 **Test Case Example**", expanded=False):
    st.markdown("""
    Use these inputs to verify calculations:
    - Stock Price = `100`
    - Strike Price = `100`
    - Time to Maturity = `1`
    - Volatility = `0.2`
    - Risk-Free Rate = `0.05`
    - Purchase Price = `8`
    - Market Price = `10.45`
    Expected results:
    - **Option Price:** `10.45`
    - **Delta:** `0.6368`, **Gamma:** `0.0188`
    - **Vega:** `0.3752`, **Theta:** `-0.0176`, **Rho:** `0.5323`
    - **P&L:** `2.45`
    - **IV:** `0.20`
    """)

# -------------------- Section A --------------------
st.divider()
st.markdown("###  **Option Pricing & Greeks**")

if T <= 0 or sigma <= 0:
    st.error(" Time to maturity (T) and volatility (σ) must be positive.")
else:
    option_price = black_scholes_price(S, K, T, r, sigma, option_type)
    delta, gamma, vega, theta, rho = calculate_greeks(S, K, T, r, sigma, option_type)

    col_price, col_greeks = st.columns([1.2, 1.5])
    with col_price:
        st.success(f"**Option Price:** ${option_price:.2f}")
    with col_greeks:
        with st.expander(" **Greeks (Δ, Γ, Vega, Theta, Rho)**", expanded=False):
            st.markdown(f"**Delta (Δ):** {delta:.4f}")
            st.markdown(f"**Gamma (Γ):** {gamma:.4f}")
            st.markdown(f"**Vega:** {vega:.4f}")
            st.markdown(f"**Theta:** {theta:.4f}")
            st.markdown(f"**Rho:** {rho:.4f}")

# -------------------- Section B --------------------
st.divider()
st.markdown("###  **Profit or Loss (P&L)**")

pnl = calculate_pnl(S, K, T, r, sigma, purchase_price, option_type)
if pnl >= 0:
    st.success(f"**Profit:** ${pnl:.2f}")
else:
    st.error(f"**Loss:** ${pnl:.2f}")

# -------------------- Section C --------------------
st.divider()
st.markdown("### 🔍 **Shock Analysis (Sensitivity Heatmap)**")

enable_analysis = st.checkbox("Enable Sensitivity Analysis", value=False)

if enable_analysis:
    st.markdown("Adjust ranges to visualize option price or P&L sensitivity.")

    col1, col2 = st.columns(2)
    with col1:
        S_min = st.number_input("Min Stock Price", value=80.0)
        S_max = st.number_input("Max Stock Price", value=120.0)
    with col2:
        vol_min = st.number_input("Min Volatility", value=0.1)
        vol_max = st.number_input("Max Volatility", value=0.5)

    steps = st.slider("Resolution (Higher = More Detail)", min_value=5, max_value=50, value=20)
    heatmap_type = st.radio("Heatmap Type", ["Option Price", "P&L"])

    if st.button("Generate Heatmap"):
        S_range = np.linspace(S_min, S_max, steps)
        vol_range = np.linspace(vol_min, vol_max, steps)

        if heatmap_type == "Option Price":
            df = generate_price_grid(S_range, vol_range, K, T, r, option_type)
            title = "Option Price Heatmap"
            center_val = None
        else:
            df = generate_pnl_grid(S_range, vol_range, K, T, r, purchase_price, option_type)
            title = "P&L Heatmap"
            center_val = 0

        fig, ax = plt.subplots(figsize=(9, 5))
        sns.heatmap(df, cmap="coolwarm" if heatmap_type == "P&L" else "YlGnBu",
                    center=center_val, annot=False, fmt=".2f", ax=ax)
        ax.set_title(title, fontsize=14)
        st.pyplot(fig)

# -------------------- Section D --------------------
st.divider()
st.markdown("###  **Implied Volatility (IV)**")

iv = implied_volatility(market_price, S, K, T, r, option_type)
if iv is not None:
    st.info(f"**Implied Volatility:** {iv:.4f} ({iv*100:.2f}%)")
else:
    st.warning("Could not calculate IV. Adjust inputs.")

# -------------------- Footer --------------------
st.divider()
st.markdown("""
<h3 style='text-align: center;'>👤 About the Creator</h3>
<p style='text-align: center;'>
<b>Aurokrishnaa Ravindran Lakshmi</b><br>
MS in Finance (Quantitative Finance), University at Buffalo<br>
💡 Passionate about Financial Modeling, Derivatives & Python<br>
</p>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center;'>
<a href='https://www.linkedin.com/in/aurokrishnaa/' target='_blank'>
    <img src='https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin' alt='LinkedIn'>
</a>
<a href='https://www.aurokrishnaa.me' target='_blank'>
    <img src='https://img.shields.io/badge/Website-Visit-informational?style=for-the-badge&logo=google-chrome' alt='Website'>
</a>
</div>
""", unsafe_allow_html=True)

st.markdown("<p style='text-align:center;font-size:12px;'>*This app is for educational purposes only.*</p>", unsafe_allow_html=True)
