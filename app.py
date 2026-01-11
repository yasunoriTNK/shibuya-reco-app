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

    # サイドバー（管理用・パスワード保護）
    with st.sidebar:
        with st.expander("管理メニュー"):
            admin_password = st.text_input("管理者パスワード", type="password")
            # 環境変数 ADMIN_PASSWORD が未設定の場合は "admin123" をデフォルトとする（デモ用）
            correct_password = os.getenv("ADMIN_PASSWORD", "admin123")
            
            if admin_password == correct_password:
                st.success("認証成功")
                if st.button("質問データを更新（AI生成）", help="Excelのキーワードを元に、質問を再生成します。"):
                    from ai.generator import generate_questions_from_data
                    with st.spinner("AIが質問を考えています..."):
                        result = generate_questions_from_data()
                    if result["success"]:
                        st.success(result["message"])
                        st.cache_data.clear() # キャッシュクリア
                        import time
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(result["message"])
                st.caption("※Excel (data/shibuya_spots.xlsx) を更新してから押してください。")
            elif admin_password:
                st.error("パスワードが違います")

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
