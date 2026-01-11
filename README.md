# Shibu Deep / Be JOREN (渋谷ディープ / Be 常連)

渋谷初訪のインバウンド旅行者向けに、「想像の外側」のスポットをレコメンドするWebアプリプロトタイプです。

## 起動方法

1. **仮想環境の作成と有効化 (推奨)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **依存ライブラリのインストール**
   ```bash
   pip install -r requirements.txt
   ```

3. **環境変数の設定**
   OpenAI APIを使用するため、環境変数 `OPENAI_API_KEY` を設定してください。
   設定されていない場合、AI生成部分はダミーテキストにて動作します。
   ```bash
   export OPENAI_API_KEY="sk-..."
   ```

4. **アプリの起動**
   ```

5. **管理者パスワードの設定（任意）**
   サイドバーの管理メニューを保護するためのパスワードです。
   設定しない場合はデフォルトで `admin123` となります。
   ```bash
   export ADMIN_PASSWORD="your_secure_password"
   ```

## ディレクトリ構成
- `app.py`: アプリケーションのメインファイル
- `data/`: スポットデータ (Excel)
- `ui/`: 画面描画ロジックとコンポーネント
- `domain/`: ビジネスロジック (質問、スコアリング)
- `ai/`: OpenAI API連携
- `config/`: 設定ファイル (質問文言など)
- `assets/`: 画像アセット

## データの配置
`data/shibuya_spots.xlsx` に店舗データを配置してください。
必要なカラム: `No`, `店舗名`, `タイプ`, `キーワード`, `URL`, `説明`, `住所`, `記入者`
