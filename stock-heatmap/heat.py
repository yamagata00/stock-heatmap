import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
import time

# ページ設定
st.set_page_config(layout="wide", page_title="株価ヒートマップ")

# 🔽 銘柄をユーザーが入力（初期値付き）
tickers_input = st.text_input("銘柄コード（カンマ区切りで入力）", value="NEE, T, VZ, CSCO, TSLA, AMD")
tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

# 🔽 更新間隔を選択（デフォルト30秒）
interval = st.slider("更新間隔（秒）", min_value=10, max_value=300, value=30)

# 🔽 株価変化率を取得する関数
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

# 🔁 グラフ描画と定期更新
placeholder = st.empty()
while True:
    if not tickers:
        st.warning("銘柄を1つ以上入力してください。")
        time.sleep(interval)
        continue

    df = get_price_changes(tickers)
    if df.empty:
        st.warning("データ取得に失敗しました。銘柄コードを確認してください。")
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

