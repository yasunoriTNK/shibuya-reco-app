import streamlit as st
import os
from ui.pages import render_quiz, render_home, render_detail, render_route, render_saved

# ページ設定（必ず最初に呼ぶ）
st.set_page_config(
    page_title="Shibu Deep / Be JOREN",
    page_icon="🌃",
    layout="centered"
)

def main():
    # session_state の初期化
    if 'screen' not in st.session_state:
        st.session_state.screen = 'quiz'
    if 'user_tags' not in st.session_state:
        st.session_state.user_tags = []
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0
    if 'recommended_spot_id' not in st.session_state:
        st.session_state.recommended_spot_id = None
    if 'selected_spot_id' not in st.session_state:
        st.session_state.selected_spot_id = None

    # ルーティング
    screen = st.session_state.screen

    # サイドバーは削除（ローカル運用のため）

    if screen == 'quiz':
        render_quiz()
    elif screen == 'home':
        render_home()
    elif screen == 'detail':
        render_detail()
    elif screen == 'route':
        render_route()
    elif screen == 'saved':
        render_saved()
    else:
        st.error(f"Unknown screen: {screen}")

if __name__ == "__main__":
    main()
