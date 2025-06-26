import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
import time

# ページレイアウト（横幅最大化）
st.set_page_config(layout="wide", page_title="株価ヒートマップ")

# 銘柄リスト（固定）
tickers = ["NEE", "T", "VZ", "CSCO", "TSLA", "AMD"]

# 更新間隔スライダーのみ
interval = st.slider("更新間隔（秒）", min_value=10, max_value=300, value=30)

# 株価取得・処理関数
def get_price_changes(tickers):
    raw_data = yf.download(tickers, period="2d", interval="1d", group_by="ticker")
    records = []
    for ticker in tickers:
        try:
            closes = raw_data[ticker]["Close"]
            change = ((closes.iloc[-1] - closes.iloc[-2]) / closes.iloc[-2]) * 100
            change = round(change, 2)
            label = f"{ticker}<br>{change:+.2f}%"
            records.append({
                "銘柄": ticker,
                "ラベル": label,
                "変化率 (%)": change,
                "サイズ": 1
            })
        except:
            continue
    return pd.DataFrame(records)

# MARKETSPEED風カラー
custom_colors = [
    [0.0, "#AA0000"],
    [0.5, "#222222"],
    [1.0, "#00AA00"]
]

# 描画ループ
placeholder = st.empty()
while True:
    df = get_price_changes(tickers)
    if df.empty:
        st.warning("データ取得に失敗しました。")
    else:
        fig = px.treemap(
            df,
            path=["ラベル"],
            values="サイズ",
            color="変化率 (%)",
            color_continuous_scale=custom_colors,
            range_color=[-5, 5]
        )

        fig.update_traces(
            textinfo="label",
            textfont_size=28,
            textfont_color="white",
            textposition="middle center"
        )

        fig.update_layout(
            margin=dict(t=20, l=5, r=5, b=5),
            height=600,
            paper_bgcolor="black",
            plot_bgcolor="black"
        )

        placeholder.plotly_chart(fig, use_container_width=True)

    time.sleep(interval)

