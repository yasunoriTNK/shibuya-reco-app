import os
import json
import streamlit as st
from openai import OpenAI
from ai.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

# ダミーレスポンス
DUMMY_RESPONSE = {
    "story_reason": "（デモ）渋谷の喧騒を離れ、まるでタイムスリップしたかのような体験ができる場所です。あなたの「静か」で「レトロ」な気分にぴったり寄り添う、特別な一杯が待っています。",
    "local_tip": "実はここ、マスターが一人で切り盛りしてるらしいよ。静かに過ごしたい時におすすめ。",
    "safety_info": "メニューは日本語のみの可能性が高いですが、指差し注文で通じます。現金を用意していくのが安心です。"
}

@st.cache_data(show_spinner=False)
def generate_spot_info(spot_data, user_tags):
    """
    OpenAI APIを使ってスポットの推薦文を生成する。
    同じスポット・同じタグの組み合わせならキャッシュを返す。
    APIキーが無い、またはエラー時はダミーを返す。
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return DUMMY_RESPONSE

    client = OpenAI(api_key=api_key)
    
    user_content = USER_PROMPT_TEMPLATE.format(
        name=spot_data['店舗名'],
        type=spot_data['タイプ'],
        description=spot_data['説明'],
        keywords=",".join(spot_data['keywords_list']),
        address=spot_data['住所'],
        url=spot_data['URL'],
        user_tags=",".join(user_tags)
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o", # または gpt-3.5-turbo
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content}
            ],
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        return json.loads(content)

    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return DUMMY_RESPONSE
