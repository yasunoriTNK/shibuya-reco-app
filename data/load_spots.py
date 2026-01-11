import pandas as pd
import streamlit as st
import os

@st.cache_data
def load_data(excel_path='data/shibuya_spots.xlsx'):
    """
    Excelファイルを読み込み、前処理を行ってDataFrameを返す関数
    """
    if not os.path.exists(excel_path):
        return pd.DataFrame() # ファイルがない場合は空のDFを返す

    try:
        df = pd.read_excel(excel_path)
    except Exception as e:
        st.error(f"データの読み込みに失敗しました: {e}")
        return pd.DataFrame()

    # 前処理
    # 店舗名が空の行を削除
    df = df.dropna(subset=['店舗名'])
    
    # キーワードの正規化とリスト化
    def normalize_keywords(kw_str):
        if not isinstance(kw_str, str):
            return []
        # 全角カンマ、読点などを半角カンマに置換
        normalized = kw_str.replace('，', ',').replace('、', ',')
        # 分割して空白除去
        return [k.strip() for k in normalized.split(',') if k.strip()]

    df['keywords_list'] = df['キーワード'].apply(normalize_keywords)

    return df

def get_spot_by_id(df, spot_id):
    """
    No（spot_id）を指定してスポット情報を取得する
    """
    if df.empty:
        return None
    
    spot = df[df['No'] == spot_id]
    if spot.empty:
        return None
    
    return spot.iloc[0]
