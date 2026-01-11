import os
import sys

# プロジェクトルートをパスに追加
sys.path.append(os.getcwd())

try:
    from ai.generator import generate_questions_from_data
    print("質問生成を開始します...")
    result = generate_questions_from_data()
    if result["success"]:
        print(f"成功: {result['message']}")
    else:
        print(f"失敗: {result['message']}")
except Exception as e:
    print(f"エラーが発生しました: {e}")
