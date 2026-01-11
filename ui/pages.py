import streamlit as st
import time
from ui.components import render_progress_bar, render_option_card, render_spot_card, render_tags, render_header
from domain.questions import QuestionManager
from domain.scoring import recommend_spot
from data.load_spots import load_data, get_spot_by_id
from ai.client import generate_spot_info

def render_quiz():
    """
    クイズ画面の描画
    """
    render_header()
    
    qm = QuestionManager()
    current_index = st.session_state.get('current_question_index', 0)
    questions = qm.get_questions()
    total = len(questions)

    if current_index >= total:
        # 全問終了 -> 推薦処理へ
        process_recommendation()
        return

    q = questions[current_index]
    
    render_progress_bar(current_index + 1, total)
    
    st.header(q['text'])
    
    col1, col2 = st.columns(2)
    
    def next_question(selected_tags):
        st.session_state.user_tags.extend(selected_tags)
        st.session_state.current_question_index += 1
        st.rerun()

    with col1:
        opt1 = q['options'][0]
        render_option_card(opt1['label'], f"q_{current_index}_opt1", 
                          lambda: next_question(opt1['tags']))
    
    with col2:
        opt2 = q['options'][1]
        render_option_card(opt2['label'], f"q_{current_index}_opt2", 
                          lambda: next_question(opt2['tags']))

def process_recommendation():
    """
    推薦ロジックを実行し、ホーム画面へ遷移
    """
    df = load_data()
    spot_id = recommend_spot(df, st.session_state.user_tags)
    
    st.session_state.recommended_spot_id = spot_id
    st.session_state.screen = 'home'
    st.rerun()

def render_home():
    """
    ホーム画面（推薦結果）
    """
    render_header()
    
    st.success("あなたの気分にぴったりの場所が見つかりました！")
    
    spot_id = st.session_state.get('recommended_spot_id')
    df = load_data()
    spot = get_spot_by_id(df, spot_id)
    
    if spot is None:
        st.error("スポットが見つかりませんでした。")
        if st.button("最初に戻る"):
            st.session_state.clear()
            st.rerun()
        return

    def go_to_detail(sid):
        st.session_state.selected_spot_id = sid
        st.session_state.screen = 'detail'
        st.rerun()

    render_spot_card(spot, go_to_detail)
    
    st.divider()
    if st.button("診断をやり直す"):
        st.session_state.clear()
        st.rerun()

def render_detail():
    """
    店舗詳細画面
    """
    render_header()
    
    col_back, _ = st.columns([1, 4])
    with col_back:
        if st.button("← 戻る"):
            st.session_state.screen = 'home'
            st.rerun()

    spot_id = st.session_state.get('selected_spot_id')
    df = load_data()
    spot = get_spot_by_id(df, spot_id)
    
    if spot is None:
        st.error("エラーが発生しました")
        return

    st.title(spot['店舗名'])
    render_tags(spot['keywords_list'])
    
    # AI生成コンテンツ
    with st.spinner("AIが推薦ストーリーを生成中..."):
        ai_info = generate_spot_info(spot, st.session_state.user_tags)
    
    st.divider()
    
    st.subheader("💡 Why this spot?")
    st.info(ai_info.get("story_reason", ""))
    
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://placehold.co/600x400?text=Movie+Placeholder", caption="30秒動画（ダミー）", use_container_width=True)
    with col2:
        st.subheader("🗣️ 地元民の一言")
        st.write(f"「{ai_info.get('local_tip', '')}」")
        
        st.subheader("🛡️ 安心情報")
        st.caption(ai_info.get("safety_info", ""))

    st.divider()
    
    if st.button("🗺️ ここに行く（ルート案内）", type="primary", use_container_width=True):
        st.session_state.screen = 'route'
        st.rerun()

def render_route():
    """
    ルート案内画面
    """
    render_header()
    
    col_back, _ = st.columns([1, 4])
    with col_back:
        if st.button("← 戻る"):
            st.session_state.screen = 'detail'
            st.rerun()
            
    spot_id = st.session_state.get('selected_spot_id')
    df = load_data()
    spot = get_spot_by_id(df, spot_id)
    
    st.subheader(f"{spot['店舗名']} への行き方")
    
    st.write("1. 渋谷駅ハチ公口を出ます")
    st.write("2. スクランブル交差点を渡ります")
    st.write("3. ... (簡易案内)")
    
    # Google Maps Link
    import urllib.parse
    address = spot.get('住所', '')
    encoded_address = urllib.parse.quote(address)
    gmap_url = f"https://www.google.com/maps/search/?api=1&query={encoded_address}"
    
    st.markdown(f"[📍 Google Mapで開く]({gmap_url})")
    
    st.divider()
    
    if st.button("入店した（デモプレイ）", use_container_width=True):
        st.balloons()
        st.success("店舗に通知しました！良い時間を！")
        time.sleep(3)
        st.session_state.clear()
        st.rerun()

def render_saved():
    st.write("保存リスト画面（未実装）")
