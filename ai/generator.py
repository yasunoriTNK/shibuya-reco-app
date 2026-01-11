import pandas as pd
import json
import os
import shutil
from openai import OpenAI
from collections import Counter
from data.load_spots import load_data

SYSTEM_PROMPT_GENERATOR = """
あなたは渋谷のスポットデータ分析官です。
与えられた「キーワードのリスト」を分析し、ユーザーの好みを分類するための「2択の質問」を5つ作成してください。

## 出力形式 (重要)
必ず以下のJSONオブジェクト形式で出力してください。
{
  "questions": [
    {
      "id": "q1",
      "text": "質問文（例：今の気分は？）",
      "image_key": "q1_mood",
      "options": [
        {
          "label": "選択肢Aラベル",
          "tags": ["タグ1", "タグ2"]
        },
        {
          "label": "選択肢Bラベル",
          "tags": ["タグ3", "タグ4"]
        }
      ]
    },
    ...
  ]
}

## 要件
- 出力はJSONオブジェクトのみ。余計な解説は不要。
- 各質問は、ユーザーが直感的に選べる短いもの。
- 選択肢（options）は、それぞれ対照的な属性や雰囲気を持つようにする。
- 各選択肢には、対応する「タグ（tags）」をマッピングする。このタグは、入力されたキーワードリストの中に実在するものから選ぶ。
- 質問IDは "q1" 〜 "q5" とする。
"""

def validate_questions(questions_list):
    """
    生成された質問リストが必要なキーを持っているかチェックする
    """
    if not isinstance(questions_list, list) or len(questions_list) == 0:
        return False, "質問リストが空、またはリスト形式ではありません。"
    
    required_keys = ["id", "text", "options"]
    option_required_keys = ["label", "tags"]

    for i, q in enumerate(questions_list):
        for key in required_keys:
            if key not in q:
                return False, f"質問 {i+1} に必要なキー '{key}' が不足しています。"
        
        if not isinstance(q["options"], list) or len(q["options"]) < 2:
            return False, f"質問 {i+1} の選択肢（options）が不足しています。"
        
        for j, opt in enumerate(q["options"]):
            for opt_key in option_required_keys:
                if opt_key not in opt:
                    return False, f"質問 {i+1} の選択肢 {j+1} に必要なキー '{opt_key}' が不足しています。"
    
    return True, "Success"

def generate_questions_from_data():
    """
    OpenAI APIを使って質問JSONを生成・バリデーション・保存する。
    """
    # 1. データ読み込み
    df = load_data()
    if df.empty:
        return {"success": False, "message": "データがありません。"}

    all_keywords = []
    for keywords in df['keywords_list']:
        all_keywords.extend(keywords)
    
    keyword_counts = Counter(all_keywords)
    top_keywords = [k for k, v in keyword_counts.most_common(20)]
    
    # 2. AI生成
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {"success": False, "message": "APIキーが設定されていません。"}

    client = OpenAI(api_key=api_key)
    user_prompt = f"以下のキーワードリストに基づき、2択質問を5つ生成してください。\nキーワード: {', '.join(top_keywords)}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT_GENERATOR},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        data = json.loads(content)
        
        # 3. データの抽出とバリデーション
        questions_list = data.get("questions", [])
        is_valid, error_msg = validate_questions(questions_list)
        
        if not is_valid:
            return {"success": False, "message": f"AI生成データのバリデーションに失敗しました: {error_msg}"}

        # 4. 保存 (バックアップ作成)
        output_path = 'config/questions.json'
        backup_path = output_path + '.bak'
        
        if os.path.exists(output_path):
            shutil.copy2(output_path, backup_path)
            
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(questions_list, f, ensure_ascii=False, indent=2)
            return {"success": True, "message": "質問を安全に更新しました。"}
        except Exception as write_err:
            if os.path.exists(backup_path):
                shutil.copy2(backup_path, output_path)
            return {"success": False, "message": f"書き込みエラー: {write_err}"}

    except Exception as e:
        return {"success": False, "message": f"AI生成エラー: {str(e)}"}
