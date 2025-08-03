# Black Scholes Option Pricing Dashboard

A professional, interactive Black-Scholes Option Pricing and Risk Analysis dashboard built by **Aurokrishnaa Ravindran Lakshmi** using Python and Streamlit.

This tool calculates **European option prices**, visualizes **Greeks**, models **P&L**, generates **Sensitivity Heatmaps**, and estimates **Implied Volatility** — all in one elegant dashboard.

---

##  About the Author

**Aurokrishnaa Ravindran Lakshmi**  
 MS in Finance (Quantitative Finance) – University at Buffalo  
🌐 [aurokrishnaa.me](https://www.aurokrishnaa.me)  
🔗 [LinkedIn → @aurokrishnaa](https://www.linkedin.com/in/aurokrishnaa/)

> *Actively seeking roles in Finance, Quantitative Analysis, Financial Analysis.*

---

##  Features

-  **European Option Pricing (Call & Put)**
-  Full calculation of **Greeks**: Delta, Gamma, Vega, Theta, Rho
-  **Profit/Loss Calculator** based on purchase price
-  **Sensitivity Heatmaps** for Stock Price vs Volatility
-  **Implied Volatility Estimator**
-  Clean UI with sidebar controls, tooltips, and polished layout
-  Deployment ready

---

## Screenshots

| Feature | Preview |
|--------|---------|
| **Model Inputs** | ![](model_screenshots/model_inputs.png) |
| **Pricing & Greeks Output** | ![](model_screenshots/pricing_and_greeks.png) |
| **Profit/Loss Calculation** | ![](model_screenshots/profit_loss_calculation.png) |
| **Shock Analysis – Heatmap** | ![](model_screenshots/shock_analysis_heatmap.png) |
| **Option Price Heatmap** | ![](model_screenshots/option_price_heatmap.png) |
| **Implied Volatility** | ![](model_screenshots/implied_volatility.png) |
| **Footer Branding** | ![](model_screenshots/footer.png) |

---

##  Real World Test Case: AAPL Call Option (August 2025)

To demonstrate the practical application of this dashboard, I tested it using a real European-style option on **Apple Inc. (AAPL)** from August 2025. The parameters were sourced from actual option chain data.

| Parameter              | Value                        |
|------------------------|------------------------------|
| Underlying Price (S)   | $196.25                      |
| Strike Price (K)       | $195.00                      |
| Expiry Date            | August 9, 2025               |
| Evaluation Date        | August 3, 2025               |
| Time to Maturity (T)   | 6/365 ≈ **0.0164 years**     |
| Implied Volatility (σ) | ~22% → **0.22**              |
| Risk-Free Rate (r)     | **5%**                       |
| Market Option Price    | **$2.25**                    |
| Purchase Price (P₀)    | **$2.00** (for P&L testing)  |

This example validates that the Black-Scholes output aligns closely with market pricing and allows for robust **P&L analysis**, **Greeks interpretation**, and **sensitivity visualization** using real financial data.

> A great showcase of how this dashboard can assist in **option valuation, strategy development**, and **financial modeling interviews**.

---

##  How to Run Locally

You can run this app locally using Python and Streamlit:

### 1. Clone the Repository

```bash
git clone https://github.com/Aurokrishnaa/black-scholes-option-dashboard-aurokrishnaa.git
cd black-scholes-option-dashboard-aurokrishnaa
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Running the app

```bash
streamlit run app.py
```


## Deployment:
This app will be hosted online
Link will be added here after deployment.

## Why This Project?
This dashboard showcases both quantitative finance knowledge and Python technical skills. It’s a personal project developed to strengthen understanding of option theory while building a full stack finance tool.
