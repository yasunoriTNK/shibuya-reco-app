import json
import os

class QuestionManager:
    def __init__(self, config_path='config/questions.json'):
        self.questions = self._load_questions(config_path)

    def _load_questions(self, path):
        if not os.path.exists(path):
            return []
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            # 生成中などでファイルが壊れている、または空の場合
            print(f"Error decoding {path}")
            return []
        except Exception as e:
            print(f"Error loading questions: {e}")
            return []

    def get_questions(self):
        return self.questions

    def get_total_questions(self):
        return len(self.questions)

    def get_question_by_index(self, index):
        if 0 <= index < len(self.questions):
            return self.questions[index]
        return None
