import pandas as pd
import json
import os
import random
from openai import OpenAI
from collections import Counter
from data.load_spots import load_data

SYSTEM_PROMPT_GENERATOR = """
あなたは渋谷のスポットデータ分析官です。
与えられた「キーワードのリスト」を分析し、ユーザーの好みを分類するための「2択の質問」を5つ作成してください。

## 要件
- 出力はJSON形式のリストのみ。
- 各質問は、ユーザーが直感的に選べる短いもの。
- 選択肢（options）は、それぞれ対照的な属性や雰囲気を持つようにする。
- 各選択肢には、対応する「タグ（tags）」をマッピングする。このタグは、入力されたキーワードリストの中に実在するものから選ぶ（あるいは近い概念）。
- 質問IDは "q1" 〜 "q5" とする。
- 画像キー（image_key）は適当な識別子をつける（例: "q1_mood"）。

## 出力スキーマ
[
  {
    "id": "q1",
    "text": "質問文（例：今の気分は？）",
    "image_key": "q1_mood",
    "options": [
      {
        "label": "選択肢Aラベル（例：にぎやか）",
        "tags": ["タグ1", "タグ2"]
      },
      {
        "label": "選択肢Bラベル（例：静か）",
        "tags": ["タグ3", "タグ4"]
      }
    ]
  },
  ...
]
"""

def generate_questions_from_data():
    """
    Excelデータからキーワードを抽出し、OpenAI APIを使って質問JSONを生成・保存する。
    """
    # 1. データ読み込み
    df = load_data()
    if df.empty:
        return {"success": False, "message": "データがありません。"}

    # 2. キーワード収集
    all_keywords = []
    for keywords in df['keywords_list']:
        all_keywords.extend(keywords)
    
    # 頻出キーワードを確認（デバッグ用）
    keyword_counts = Counter(all_keywords)
    top_keywords = [k for k, v in keyword_counts.most_common(20)]
    
    # 3. AI生成
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {"success": False, "message": "APIキーが設定されていません。"}

    client = OpenAI(api_key=api_key)
    
    user_prompt = f"""
    以下のキーワードリストは、渋谷にあるおすすめスポットの特徴タグです。
    これらを元に、スポットを推薦するための「2択質問」を5つ生成してください。
    
    ## キーワードリスト（頻出順）
    {", ".join(top_keywords)}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT_GENERATOR},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        # JSONパース（ルートがリストか、オブジェクト { "questions": [...] } かを確認）
        content = response.choices[0].message.content
        data = json.loads(content)
        
        # スキーマ揺れ対応
        if isinstance(data, dict):
             # {"questions": [...]} の形式できた場合
             for key in data:
                 if isinstance(data[key], list):
                     questions_list = data[key]
                     break
             else:
                 questions_list = []
        elif isinstance(data, list):
            questions_list = data
        else:
            return {"success": False, "message": "AIの出力形式が予期しない形式でした。"}

        if not questions_list:
             return {"success": False, "message": "質問リストが空でした。"}

        # 4. 保存
        output_path = 'config/questions.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(questions_list, f, ensure_ascii=False, indent=2)
            
        return {"success": True, "message": f"質問を再生成しました！（キーワード: {len(top_keywords)}個）"}

    except Exception as e:
        return {"success": False, "message": f"エラーが発生しました: {str(e)}"}
