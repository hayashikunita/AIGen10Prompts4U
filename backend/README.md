# FastAPI Backend

このディレクトリにはFastAPIバックエンドが含まれています。

## セットアップ

```bash
# 仮想環境を作成（任意）
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# 依存関係をインストール
pip install -r requirements.txt
```

## 実行

```bash
# 開発モード
python main.py

# または uvicorn を直接使用
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API エンドポイント

### カテゴリ
- `GET /api/categories` - カテゴリ一覧取得
- `GET /api/prompts/{category}` - 指定カテゴリのプロンプト取得

### チャット
- `POST /api/chat` - チャット応答生成（ストリーミング）
- `POST /api/upload` - ファイルアップロード

### 履歴
- `GET /api/chat-history` - 履歴一覧取得
- `GET /api/chat-history/{filename}` - 履歴詳細取得
- `POST /api/chat-history` - 履歴保存
- `DELETE /api/chat-history/{filename}` - 履歴削除

## 環境変数

`.env` ファイルを作成してください：

```
OPENAI_API_KEY=your_api_key_here
```
