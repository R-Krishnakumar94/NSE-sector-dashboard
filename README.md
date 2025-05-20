# 📊 NSE Sector Dashboard

## 🔎 Overview
This project is a **fully interactive data analytics dashboard** that provides sector-wise insights on the **Indian stock market (NSE)**. The tool merges real-time technical data with financial news sentiment analysis to help traders, analysts, and investors:

- Identify **top-performing and underperforming sectors**
- Gauge **market mood and sectoral sentiment** using NLP
- Use **relative strength** for actionable trade insights
- Build a **foundation for machine learning trend prediction**

Unlike basic price trackers, this dashboard provides a **360° view** of sector dynamics by combining:
- 📈 **Price Action and Momentum**
- 🌐 **News-Based Sentiment (India + Global)**
- 🧠 **Relative Strength vs NIFTY**
- 🚀 **Scalable ML-ready architecture**

---

## 🧠 Methodology & Approaches

### 1. **Technical Price-Based Movement Analysis**
We collect **daily price data** for major NSE sector indices using `yfinance`. Each sector’s daily momentum is computed using:

```math
% Change = ((Close_Today - Close_Yesterday) / Close_Yesterday) * 100
```

This identifies **momentum leaders and laggards**.

---

### 2. **Relative Strength (RS) Analysis vs NIFTY 50**
A core innovation in this project is **RS scoring**, which identifies outperforming sectors based on:

```math
RS Score = Sector % Change - NIFTY % Change
```

#### 🔮 Prediction Mapping
- RS > +0.5 → 🚀 **Strong Buy Watch**
- RS between -0.5 to +0.5 → ⚠️ **Weak/Neutral**
- RS < -0.5 → 🔻 **Underperforming Sector**

This is used for **next-session predictions**, especially useful for **short-term traders and swing setups**.

---

### 3. **FinBERT-Based Sentiment Analysis**
We integrate **FinBERT**, a transformer model trained on financial texts, to score news articles:

#### 🧠 Formula:
```math
Sentiment Score = P(Positive) - P(Negative)
```

We analyze articles from:
- 🇮🇳 Indian business sources (e.g., MoneyControl, ET)
- 🌍 Global financial media (via NewsAPI)

Each sector receives a **blended sentiment score**:

```math
Final Score = 0.6 × India_Sentiment + 0.4 × Global_Sentiment
```

Then categorized into:
- 😃 Bullish
- 😐 Neutral
- 😟 Bearish

This method lets us quantify **narrative-based sentiment impact** on different sectors.

---

## 📈 Sentiment Trend Prediction (Future Scope)
This section is currently a placeholder for an upcoming ML model that will predict **future sector movements based on historical sentiment trends**.

### 🚧 Planned Approach:
- Log **daily sentiment scores** for each sector
- Use those logs to create **rolling input windows** (e.g. 3-day sentiment trend)
- Train a **Logistic Regression / Random Forest / LSTM** to predict:
  - Will the sector rise or fall next session?

### 🧮 Example Features:
- `sentiment_day_1`, `sentiment_day_2`, `sentiment_day_3`
- `price_change_next_day (target)`

### 📊 Example Output:
| Sector     | Recent Sentiments | Prediction        |
|------------|--------------------|-------------------|
| NIFTY IT   | [-0.2, 0.1, 0.3]   | ⬆️ Uptrend Expected |
| NIFTY AUTO | [0.3, 0.2, -0.1]   | ⬇️ Downtrend Likely |

This would add a machine-learning layer to the dashboard and help forecast direction based on how **sentiment evolves over time**.

---

## 🎯 Why This Project Is Unique
- It merges **quantitative price movement** with **natural language-based sentiment**
- Uses **RS scoring** to simulate **capital rotation and sector momentum**
- Combines both **India-specific and global financial sentiment**
- Built to scale — future-ready for **ML classifiers** and **trend prediction models**
- Powered by a clean, intuitive **Streamlit UI** for real-time analysis

---

## 🧰 Technologies Used
- **Streamlit** – UI & dashboard framework
- **yfinance** – Historical sector index data
- **transformers / FinBERT** – Financial sentiment modeling
- **scikit-learn** – ML prep pipeline
- **pandas, numpy** – Data wrangling & computation

---

## 🧑‍💻 Author Skill Highlights
> This dashboard demonstrates expertise in:

- 🔍 **Data Analytics** – Sector scanning, trend scoring, and filtering
- 🧠 **Statistical & Mathematical Modeling** – RS, momentum, sentiment quantification
- 🐍 **Python Engineering** – Modular, API-integrated, efficient pipeline
- 💹 **Financial Insight** – Practical knowledge of sector behavior and technical signals
- 📊 **Visual Communication** – Simple, trader-friendly design

---

## 🖼 Dashboard Preview

![Dashboard Preview](https://raw.githubusercontent.com/R-Krishnakumar94/nse-sector-dashboard/main/preview.png)
---

## 🚀 How to Run Locally
1. Clone the repository
```bash
git clone https://github.com/yourusername/nse-sector-dashboard
cd nse-sector-dashboard
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Add your NewsAPI key via Streamlit secrets:
```toml
# .streamlit/secrets.toml
NEWSAPI_KEY = "your_actual_key"
```
4. Run the app:
```bash
streamlit run nse_dashboard.py
```

---

## 🌐 Live Demo
**Deployed at**: https://bit.ly/3ZtRT3d

---

Feel free to fork and expand this tool for:
- Intraday trading alerts
- Sector correlation visualization
- Custom watchlist sentiment tracking
