# app.py
import os
import streamlit as st
from pydantic import BaseModel, Field
from openai import OpenAI

# ==============
# OpenAI client
# ==============
# OpenAI SDKは通常 OPENAI_API_KEY を見に行きます（環境変数推奨）:contentReference[oaicite:1]{index=1}
# もしうまく拾えない場合に備えて、明示的に読む形にも対応
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else OpenAI()

# ==============
# Output schema (Structured Outputs)
# ==============
class Suggestion(BaseModel):
    title: str = Field(..., description="提案の短いタイトル（30文字程度）")
    places: list[str] = Field(..., description="渋谷の具体的な店・スポット名を2〜5個")
    description: str = Field(..., description="魅力的な紹介文（1000文字以内）")

class RecoResponse(BaseModel):
    suggestions: list[Suggestion] = Field(..., description="提案は最大3つ")


# ==============
# UI
# ==============
st.set_page_config(page_title="Shibuya Activity Recommender", page_icon="🗺️", layout="centered")
st.title("🗺️ 渋谷アクティビティ提案（好み診断）")
st.caption("10個の好みを5段階で選ぶと、あなた向けの渋谷プランを最大3つ提案します。")

st.markdown("### 好みを選択（1=左寄り、5=右寄り）")

# 10個の嗜好軸（例）
AXES = [
    ("にぎやか", "静か"),
    ("高級", "庶民的"),
    ("王道", "ニッチ"),
    ("室内", "屋外"),
    ("短時間", "じっくり"),
    ("アクティブ", "まったり"),
    ("カルチャー/アート", "グルメ中心"),
    ("最新トレンド", "レトロ/味のある"),
    ("一人向け", "みんなで"),
    ("日本らしさ", "グローバル/多国籍"),
]

prefs = {}
for left, right in AXES:
    key = f"{left} ⇄ {right}"
    prefs[key] = st.slider(key, 1, 5, 3)

extra = st.text_input("補足（任意）例：予算、時間帯、苦手なこと、行きたい雰囲気など", "")

col1, col2 = st.columns([1, 1])
with col1:
    max_budget = st.selectbox("予算感（任意）", ["指定なし", "〜3,000円", "〜6,000円", "〜10,000円", "10,000円〜"])
with col2:
    duration = st.selectbox("滞在時間（任意）", ["指定なし", "1〜2時間", "半日", "1日"])

st.divider()

# ==============
# Prompt builder
# ==============
def build_prompt(prefs: dict, extra: str, max_budget: str, duration: str) -> str:
    lines = []
    lines.append("あなたは広告代理店のトップコピーライター兼、渋谷に詳しいコンシェルジュです。")
    lines.append("ユーザーの嗜好に合わせて、渋谷でのアクティビティ提案を最大3つ作成してください。")
    lines.append("")
    lines.append("【必須要件】")
    lines.append("- 提案は最大3つ。")
    lines.append("- 各提案には、渋谷エリアにある具体的な店名・施設名・スポット名を「2〜5個」含める。")
    lines.append("  （例：カフェ、バー、展望、ライブハウス、書店、ギャラリー、公園、銭湯、商業施設など）")
    lines.append("- 各提案の紹介文 description は「500文字以内」。")
    lines.append("- 文章は魅力的に。広告代理店が書くように、情景が浮かぶコピーで。")
    lines.append("- ただし誇張しすぎず、断定しない（混雑や価格は変動しうる）。")
    lines.append("- 安全・法令順守。危険行為や違法行為は提案しない。")
    lines.append("")
    lines.append("【ユーザー嗜好（1=左寄り、5=右寄り）】")
    for k, v in prefs.items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("【追加条件】")
    lines.append(f"- 予算感: {max_budget}")
    lines.append(f"- 滞在時間: {duration}")
    if extra.strip():
        lines.append(f"- 補足: {extra.strip()}")
    lines.append("")
    lines.append("【出力】")
    lines.append("- 指定スキーマに従って suggestions を返すこと。")
    lines.append("- places は固有名詞のリスト（2〜5件）。")
    lines.append("- title は短く、ワクワクする見出し。")
    return "\n".join(lines)

# ==============
# Run
# ==============
if st.button("この好みで提案する ▶", type="primary"):
    prompt = build_prompt(prefs, extra, max_budget, duration)

    with st.spinner("渋谷プランを考えています…"):
        try:
            # Structured Outputs (SDK parse) :contentReference[oaicite:2]{index=2}
            response = client.responses.parse(
                model="gpt-4o-mini",
                input=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                text_format=RecoResponse,
                max_output_tokens=900,
            )
            result: RecoResponse = response.output_parsed

        except Exception as e:
            st.error("OpenAI呼び出しでエラーが発生しました。APIキー/ネットワーク/モデル名をご確認ください。")
            st.exception(e)
            st.stop()

    st.success("提案ができました！")
    st.markdown("## あなた向けの渋谷アクティビティ（最大3つ）")

    # 表示
    for i, s in enumerate(result.suggestions[:3], start=1):
        st.markdown(f"### {i}. {s.title}")
        st.markdown("**具体スポット**：" + " / ".join(s.places))
        st.write(s.description)

    st.caption("※混雑状況・料金・営業時間は変動します。訪問前に公式情報の確認をおすすめします。")
else:
    st.info("好みを選んだら「提案する」を押してください。")
