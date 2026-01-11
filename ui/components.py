import streamlit as st

def render_progress_bar(current, total):
    """
    進捗バーと現在のステップを表示 ("1 / 5")
    """
    progress = current / total
    st.progress(progress)
    st.caption(f"質問 {current} / {total}")

def render_option_card(label, key, on_click):
    """
    2択質問のカード（ボタン）を描画
    """
    if st.button(label, key=key, width='stretch'):
        on_click()

def render_spot_card(spot, on_detail_click):
    """
    ホーム画面で表示する推奨スポットのカード
    """
    with st.container(border=True):
        st.subheader(spot['店舗名'])
        st.caption(spot['タイプ'])
        
        # プレースホルダ画像
        st.image("https://placehold.co/600x400?text=Shibu+Deep", width='stretch')
        
        # 説明（短め）
        st.write(spot['説明'])
        
        # キーワードタグ
        st.write("Keywords:")
        tags = spot['keywords_list']
        st.write(" ".join([f"`#{t}`" for t in tags]))
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("詳細を見る", key=f"detail_{spot['No']}", width='stretch'):
                on_detail_click(spot['No'])
        with col2:
            st.button("保存", key=f"save_{spot['No']}", width='stretch', disabled=True, help="保存機能は未実装です")

def render_header():
    """
    共通ヘッダー
    """
    st.title("Shibu Deep 🌃")
    st.caption("Be JOREN. 想像の外側へ。")
    st.divider()

def render_tags(tags):
    """
    タグのリストを表示
    """
    st.markdown(" ".join([f"<span style='background-color:#f0f2f6; padding:4px 8px; border-radius:4px; margin-right:4px;'>{tag}</span>" for tag in tags]), unsafe_allow_html=True)
