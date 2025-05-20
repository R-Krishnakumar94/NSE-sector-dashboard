# NSE Dashboard with Relative Strength Sector Prediction

import streamlit as st
import pandas as pd
import requests
from datetime import date
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
import yfinance as yf

# ------------------------------
# Config
# ------------------------------
st.set_page_config("📊 NSE Sector Dashboard", layout="wide")
NEWSAPI_KEY = "2fe4800b3d6d442ca1baad5a1ac18b27"

@st.cache_resource()
def load_finbert():
    tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")
    model = AutoModelForSequenceClassification.from_pretrained("yiyanghkust/finbert-tone")
    return tokenizer, model

tokenizer, finbert_model = load_finbert()

# ------------------------------
# Sector Mappings
# ------------------------------
sector_yf_symbols = {
    "NIFTY IT": "^CNXIT",
    "NIFTY BANK": "^NSEBANK",
    "NIFTY PHARMA": "^CNXPHARMA",
    "NIFTY AUTO": "^CNXAUTO",
    "NIFTY FMCG": "^CNXFMCG"
}

sector_keywords = {
    "NIFTY IT": ["software", "digital", "AI", "cloud", "infotech"],
    "NIFTY BANK": ["bank", "rbi", "interest rate", "loan"],
    "NIFTY PHARMA": ["pharma", "drug", "biotech", "fda"],
    "NIFTY AUTO": ["auto", "EV", "vehicle", "car"],
    "NIFTY FMCG": ["fmcg", "consumer", "fast moving goods"]
}

# ------------------------------
# Helper Functions
# ------------------------------
def get_finbert_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = finbert_model(**inputs)
        logits = outputs.logits
        probs = torch.softmax(logits, dim=1).numpy().flatten()
    labels = ["Negative", "Neutral", "Positive"]
    label = labels[np.argmax(probs)]
    score = probs[2] - probs[0]  # Positive - Negative
    return round(score, 2), label

def fetch_sector_price_changes():
    results = []
    for sector, symbol in sector_yf_symbols.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="2d")
            if len(hist) >= 2:
                today = hist['Close'].iloc[-1]
                yesterday = hist['Close'].iloc[-2]
                change = today - yesterday
                pct = round((change / yesterday) * 100, 2)
                results.append({
                    "Sector": sector,
                    "Price Today": round(today, 2),
                    "Change (Pts)": round(change, 2),
                    "% Change": pct
                })
        except:
            results.append({
                "Sector": sector,
                "Price Today": "-", "Change (Pts)": "-", "% Change": "-"
            })
    df = pd.DataFrame(results)
    return df.sort_values("% Change", ascending=False).reset_index(drop=True)

def predict_relative_strength(change_df):
    try:
        nifty = yf.Ticker("^NSEI")
        hist = nifty.history(period="2d")
        if len(hist) >= 2:
            nifty_today = hist['Close'].iloc[-1]
            nifty_yesterday = hist['Close'].iloc[-2]
            nifty_change = ((nifty_today - nifty_yesterday) / nifty_yesterday) * 100
        else:
            nifty_change = 0
    except:
        nifty_change = 0

    change_df = change_df.copy()
    change_df["NIFTY Change"] = round(nifty_change, 2)
    change_df["RS Score"] = change_df["% Change"] - change_df["NIFTY Change"]
    change_df["Prediction"] = change_df["RS Score"].apply(
        lambda x: "🚀 Strong Buy Watch" if x > 0.5 else ("⚠️ Weak/Neutral" if x > -0.5 else "🔻 Underperform"))
    return change_df.sort_values("RS Score", ascending=False).reset_index(drop=True)

def fetch_combined_newsapi_sentiment():
    indian_sources = "moneycontrol.com,livemint.com,business-standard.com,economictimes.indiatimes.com"
    results = []

    for sector, keywords in sector_keywords.items():
        query = " OR ".join(keywords)

        def get_sentiment_from_news(query, domains=None):
            domain_param = f"&domains={domains}" if domains else ""
            url = (
                f"https://newsapi.org/v2/everything?q={query}&language=en"
                f"{domain_param}&sortBy=publishedAt&pageSize=5&apiKey={NEWSAPI_KEY}"
            )
            try:
                r = requests.get(url)
                articles = r.json().get("articles", [])
                scores = []
                for a in articles:
                    text = f"{a.get('title', '')} {a.get('description', '')}"
                    score = get_finbert_sentiment(text)[0]
                    scores.append(score)
                if scores:
                    return round(sum(scores) / len(scores), 2)
                else:
                    return None
            except:
                return None

        india_score = get_sentiment_from_news(query, domains=indian_sources)
        global_score = get_sentiment_from_news(query, domains=None)

        weights = {"India": 0.6, "Global": 0.4}
        valid_scores = {
            "India": india_score if india_score is not None else 0,
            "Global": global_score if global_score is not None else 0
        }
        available_weights = {
            k: weights[k] for k in valid_scores if valid_scores[k] != 0
        }

        if available_weights:
            norm_factor = sum(available_weights.values())
            final_score = round(sum(valid_scores[k] * weights[k] for k in available_weights) / norm_factor, 2)
            label = "😃 Bullish" if final_score > 0.1 else "😟 Bearish" if final_score < -0.1 else "😐 Neutral"
        else:
            final_score, label = "-", "⚠️ No Data"

        results.append([
            sector,
            india_score if india_score is not None else "-",
            global_score if global_score is not None else "-",
            final_score,
            label
        ])

    return pd.DataFrame(results, columns=[
        "Sector", "India Sentiment", "Global Sentiment", "Combined Score", "Sentiment"
    ])

# ------------------------------
# Streamlit UI
# ------------------------------
st.title("📊 NSE Sector Dashboard")

# 1. 📈 Sentiment Trend Prediction (ML placeholder)
st.header("📈 Sentiment Trend Prediction (Placeholder)")
st.info("This section would use past sentiment logs to train an ML model for predicting up/down trends.")

# 2. Top Gainers / Losers by Sector
st.header("📊 Sector-Wise Top Gainers & Losers (Last Session)")
price_changes = fetch_sector_price_changes()
col1, col2 = st.columns(2)
col1.subheader("Top Gainers")
col1.dataframe(price_changes.head(3))
col2.subheader("Top Losers")
col2.dataframe(price_changes.tail(3))

# 3. Relative Strength-Based Prediction
st.header("📈 Relative Strength-Based Prediction (vs NIFTY)")
rs_df = predict_relative_strength(price_changes)
st.dataframe(rs_df, use_container_width=True)

# 4. 🌍 Global & Indian NewsAPI Sector Sentiment (FinBERT)
st.header("🌍 Combined Global & Indian Sector Sentiment (FinBERT)")
newsapi_df = fetch_combined_newsapi_sentiment()
st.dataframe(newsapi_df, use_container_width=True)
