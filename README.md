# AIGenPrompts4U

モダンなReact + TypeScript + FastAPIで構築されたシステムプロンプト管理・AI対話アプリケーション


https://github.com/user-attachments/assets/155dce51-5a10-4952-b5f3-f2dede300dec


## 概要

AIGenPrompts4Uは、様々なシーンで使用できるシステムプロンプトを簡単に管理・生成できるモダンなWebアプリケーションです。
1,120個以上のプロフェッショナルなプロンプトライブラリと、OpenAI GPT-5を活用した高度なAI対話機能を提供します。

### 技術スタック

- **フロントエンド**: Next.js 16.0.3 (App Router) + React 19 + TypeScript 6 + Tailwind CSS 4
- **バックエンド**: FastAPI 0.115.0 + Python 3.13
- **AI**: OpenAI GPT-5 (ストリーミング対応)
- **UI/UX**: OpenWebUI inspired モダンデザイン

### 主な機能

- ✨ **1,120個のプロンプトライブラリ**: 28カテゴリ、専門分野に特化したプロンプト集
- 🤖 **GPT-5対話**: ストリーミングレスポンス、リアルタイムAI応答
- 💬 **2つのモード**: プロンプト表示モード + チャットボットモード
- 🎲 **プロンプト表示モード**: カテゴリ選択で全プロンプトを自動生成、コピー機能付き
- 💬 **チャットボットモード**: OpenWebUI風のクリーンで直感的なチャットインターフェース
- 📁 **ファイルアップロード対応**: PDF/Word/Excel/CSV/テキスト解析
- 💾 **会話履歴管理**: 自動保存、読込、削除機能
- 🎨 **レスポンシブデザイン**: デスクトップ・タブレット・モバイル対応
- 📋 **マークダウンレンダリング**: コードハイライト、表組み対応
- 🔄 **リアルタイム更新**: React状態管理、即座のUI反映

## 利用可能なカテゴリ

| カテゴリ | 説明 | プロンプト数 | ファイル |
|---------|------|-------------|---------|
| industry | 業界別プロンプト | 100個 | industry.json |
| idea | アイデア創出用 | 100個 | idea.json |
| engineer | エンジニア用(全工程対応) | 150個 | engineer.json |
| management | マネジメント用 | 10個 | management.json |
| sales | 営業用 | 10個 | sales.json |
| summary | 要約用 | 10個 | summary.json |
| email | メール返信用 | 10個 | email.json |
| negotiation | 単価交渉用 | 10個 | negotiation.json |
| meeting | 会議カンペ作成用 | 10個 | meeting.json |
| consultant | コンサルタント用 | 10個 | consultant.json |
| medical | 医療用 | 10個 | medical.json |
| investment | 投資用 | 10個 | investment.json |
| dating | 恋愛・デート用 | 10個 | dating.json |
| job_interview | 面接・転職対策用 | 10個 | job_interview.json |
| education | 教育・学習支援用 | 10個 | education.json |
| legal | 法律・契約書用 | 10個 | legal.json |
| sns_content | SNS・コンテンツ作成用 | 10個 | sns_content.json |
| startup | 起業・スタートアップ用 | 10個 | startup.json |
| programmer | プログラマー実践用 | 50個 | programmer.json |
| python_engineer | Pythonエンジニア専門用 | 150個 | python_engineer.json |
| ai_engineer | AIエンジニア専門用 | 50個 | ai_engineer.json |
| chatgpt_api | ChatGPT API活用専門用 | 50個 | chatgpt_api.json |
| lawyer | 法律家・弁護士実践用 | 50個 | lawyer.json |
| it_lawyer | IT法務・テック法律家専門用 | 50個 | it_lawyer.json |
| ceo | 経営者・CEO実践用 | 50個 | ceo.json |
| stock_trader | 日本株トレーダー・投資家用 | 50個 | stock_trader.json |
| finance | 金融業界・銀行実践用 | 50個 | finance.json |
| qol | QOL向上・ライフスタイル改善用 | 50個 | qol.json |

**合計28カテゴリ、1,120個のプロンプト**

## インストール・セットアップ

### 前提条件

- **Node.js** 18以上
- **Python** 3.13以上
- **OpenAI API キー**

### クイックスタート

#### 1. リポジトリをクローン

```bash
git clone <repository-url>
cd AIGenPrompts4U
```

#### 2. バックエンドのセットアップ

```bash
cd backend

# 依存パッケージをインストール
pip install -r requirements.txt

# 環境変数を設定
# .envファイルを作成し、OpenAI APIキーを設定
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

#### 3. フロントエンドのセットアップ

```bash
cd ../frontend

# 依存パッケージをインストール
npm install

# 環境変数を設定（自動作成済み）
# .env.local に NEXT_PUBLIC_API_URL=http://localhost:8000 が設定されています
```

#### 4. アプリケーションの起動

**ターミナル1 (バックエンド):**
```bash
cd backend
python main.py
# → http://localhost:8000 で起動
```

**ターミナル2 (フロントエンド):**
```bash
cd frontend
npm run dev
# → http://localhost:3000 で起動
```

#### 5. ブラウザでアクセス

http://localhost:3000 を開いてください 🎉

### 依存パッケージ詳細

#### バックエンド (Python)

- **FastAPI 0.115.0**: 高速な非同期Webフレームワーク
- **uvicorn 0.32.0**: ASGIサーバー
- **OpenAI 2.8.1**: GPT-5 API連携
- **pandas 2.2.3**: データ処理（Excel/CSV）
- **openpyxl 3.1.5**: Excelファイル処理
- **pdfplumber 0.11.4**: PDFテキスト抽出
- **python-docx 1.1.2**: Wordファイル処理
- **python-dotenv 1.0.1**: 環境変数管理

#### フロントエンド (Node.js)

- **Next.js 16.0.3**: Reactフレームワーク（App Router）
- **React 19**: UIライブラリ
- **TypeScript 6**: 型安全な開発
- **Tailwind CSS 4**: ユーティリティファーストCSS
- **react-markdown**: マークダウンレンダリング

## 使い方

### 2つのモード

アプリケーションには**プロンプト表示モード**と**チャットボットモード**の2つのモードがあります。
サイドバー上部のボタンで簡単に切り替えられます。

#### 🎲 プロンプト表示モード

大量のプロンプトを一度に確認し、選択・コピーできるモードです。

1. サイドバー上部の **「🎲 プロンプト表示」** ボタンをクリック
2. カテゴリを選択（28カテゴリから選択）
3. **「🎲 プロンプト生成」** ボタンをクリック
4. 選択したカテゴリの**全プロンプト**が自動的に表示されます（最大150個）
5. 各プロンプトカードには以下の機能があります:
   - **📋 コピー**: プロンプトをクリップボードにコピー
   - **💬 チャット開始**: そのプロンプトを使ってチャットボットモードに切り替え

**生成されるプロンプト数**:
- カテゴリによって異なります（10個〜150個）
- 常に選択したカテゴリの**全プロンプト**が表示されます
- 例: engineer(150個)、python_engineer(150個)、idea(100個)など

#### 💬 チャットボットモード

選択したプロンプトをシステムプロンプトとして使用し、GPT-5と対話するモードです。

##### 1. プロンプトの選択

1. 左サイドバーの **「📋 プロンプトを選択」** ボタンをクリック
2. カテゴリを選択（28カテゴリから選択）
3. プロンプトを選択（各カテゴリ10〜150個）
4. 選択したプロンプトがシステムプロンプトとして設定されます

##### 2. チャット開始

- メッセージ入力欄にテキストを入力
- **Enter**キーまたは**送信**ボタンでメッセージ送信
- GPT-5がストリーミングでリアルタイム応答

##### 3. ファイルアップロード

1. **📎**ボタンをクリックしてファイルを選択
2. **対応形式**:
   - 📕 **PDFファイル** (.pdf): テキスト抽出、ページ解析
   - 📘 **Wordファイル** (.docx): 段落抽出、文書分析
   - 📊 **Excelファイル** (.xlsx, .xls): 全シート読込、表形式変換
   - 📄 **CSVファイル** (.csv): データ解析、UTF-8/Shift-JIS自動判別
   - 📝 **テキスト/コード** (.txt, .py, .js, .ts, .json, .md等): ソースコード分析
4. ファイルは自動的にメッセージに添付されます
5. **⚠️ サイズ制限**: 1ファイル約60KB（15,000トークン）まで

##### 4. 会話履歴の管理

- **💾 会話を保存**: 現在の会話にタイトルをつけて保存
- **📚 履歴**: 保存済みの会話一覧を表示
  - クリックで会話を読込
  - 🗑️ボタンで削除
- **🆕 新しい会話**: 会話をリセット（自動保存実行）

##### 5. 自動保存機能

以下のタイミングで自動保存されます:
- 新しい会話を開始する時
- 別のプロンプトを選択する時
- 会話履歴から別の会話を読み込む時

### API エンドポイント

バックエンドは以下のREST APIを提供しています:

| エンドポイント | メソッド | 説明 |
|-------------|---------|------|
| `/api/categories` | GET | カテゴリ一覧取得 |
| `/api/prompts/{category}` | GET | カテゴリ別プロンプト取得 |
| `/api/chat` | POST | GPT-5ストリーミングチャット |
| `/api/upload` | POST | ファイルアップロード・解析 |
| `/api/chat-history` | GET | 会話履歴一覧取得 |
| `/api/chat-history/{filename}` | GET | 会話履歴詳細取得 |
| `/api/chat-history` | POST | 会話履歴保存 |
| `/api/chat-history/{filename}` | DELETE | 会話履歴削除 |

**Swagger UI**: http://localhost:8000/docs でAPI仕様を確認できます

## プロジェクト構造

```
AIGenPrompts4U/
├── backend/                     # FastAPI バックエンド
│   ├── main.py                 # FastAPI アプリケーション (8エンドポイント)
│   ├── requirements.txt        # Python依存パッケージ
│   ├── .env                    # 環境変数 (OPENAI_API_KEY)
│   ├── chat_history/           # 会話履歴保存ディレクトリ
│   └── README.md               # バックエンドドキュメント
│
├── frontend/                    # Next.js フロントエンド
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx        # メインUI (575行) - 2モード対応
│   │   │   ├── layout.tsx      # レイアウト設定
│   │   │   └── globals.css     # グローバルスタイル
│   │   └── lib/
│   │       └── api.ts          # API通信ライブラリ (TypeScript)
│   ├── public/                 # 静的ファイル
│   ├── package.json            # Node.js依存パッケージ
│   ├── .env.local              # 環境変数 (API_URL)
│   ├── tsconfig.json           # TypeScript設定
│   ├── tailwind.config.ts      # Tailwind CSS設定
│   └── next.config.ts          # Next.js設定
│
├── prompts_data/                # プロンプトデータ (JSON)
│   ├── industry.json           # 業界別 (100個)
│   ├── idea.json               # アイデア創出 (100個)
│   ├── engineer.json           # エンジニア (150個)
│   ├── programmer.json         # プログラマー (50個)
│   ├── python_engineer.json    # Pythonエンジニア (150個)
│   ├── ai_engineer.json        # AIエンジニア (50個)
│   ├── chatgpt_api.json        # ChatGPT API (50個)
│   ├── lawyer.json             # 法律家 (50個)
│   ├── it_lawyer.json          # IT法務 (50個)
│   ├── ceo.json                # 経営者 (50個)
│   ├── stock_trader.json       # 日本株トレーダー (50個)
│   ├── finance.json            # 金融業界 (50個)
│   ├── consultant.json         # コンサルタント (50個)
│   ├── qol.json                # QOL向上 (50個)
│   └── (他14カテゴリ、各10個)
│
├── chat_history/                # 会話履歴 (自動生成)
├── output/                      # 旧形式の出力 (レガシー)
├── src/                         # 旧CLIツール (レガシー)
├── streamlit_app.py             # 旧Streamlitアプリ (レガシー)
├── requirements.txt             # 旧依存パッケージ (レガシー)
└── README.md                    # このファイル
```

### アーキテクチャ

```
┌─────────────────────────────────────────────────────────┐
│                    ブラウザ (localhost:3000)                │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Next.js 16.0.3 Frontend (React 19 + TypeScript 6)│  │
│  │  - 2モード切り替え (page.tsx)                       │
│  │    * 🎲 プロンプト表示モード                        │
│  │    * 💬 チャットボットモード                        │
│  │  - API通信 (api.ts)                                │
│  │  - Tailwind CSS 4 スタイリング                      │
│  └────────────────┬──────────────────────────────────┘  │
└────────────────────┼──────────────────────────────────────┘
                     │ HTTP/REST API
                     │ (CORS有効)
┌────────────────────▼──────────────────────────────────────┐
│              FastAPI Backend (localhost:8000)             │
│  ┌───────────────────────────────────────────────────┐  │
│  │  main.py (FastAPI 0.115.0 + Python 3.13)          │  │
│  │  - /api/categories (カテゴリ取得)                  │  │
│  │  - /api/prompts/{category} (プロンプト取得)        │  │
│  │  - /api/chat (ストリーミングチャット)              │  │
│  │  - /api/upload (ファイルアップロード)              │  │
│  │  - /api/chat-history (履歴CRUD)                   │  │
│  └────────────────┬──────────────────────────────────┘  │
└────────────────────┼──────────────────────────────────────┘
                     │ OpenAI API
                     │
┌────────────────────▼──────────────────────────────────────┐
│                    OpenAI GPT-5 API                       │
│         (ストリーミング応答、モデル: gpt-5)                 │
└────────────────────────────────────────────────────────────┘
```

## 開発

### 技術スタック詳細

#### フロントエンド
- **フレームワーク**: Next.js 16.0.3 (App Router)
- **UI**: React 19 + TypeScript 6
- **スタイリング**: Tailwind CSS 4
- **状態管理**: React Hooks (useState, useEffect, useRef)
- **HTTP通信**: Fetch API + Server-Sent Events (ストリーミング)
- **マークダウン**: react-markdown
- **モード切り替え**: プロンプト表示モード ⇄ チャットボットモード

#### バックエンド
- **フレームワーク**: FastAPI 0.115.0
- **サーバー**: Uvicorn (ASGI)
- **AI**: OpenAI 2.8.1 (GPT-5)
- **ファイル処理**: pdfplumber, python-docx, pandas, openpyxl
- **バリデーション**: Pydantic

### 新しいカテゴリを追加

1. `prompts_data/`に新しいJSONファイルを作成

```json
{
  "category": "新カテゴリ名",
  "prompts": [
    {
      "id": 1,
      "title": "プロンプトのタイトル",
      "system_prompt": "システムプロンプト内容",
      "recommended_attachments": ["推奨ファイル1", "推奨ファイル2"]
    }
  ]
}
```

2. `backend/main.py`の`file_map`に追加

```python
file_map = {
    # ... 既存のマッピング
    "new_category": "new_category.json",
}
```

3. `backend/main.py`の`category_names`に日本語名を追加

```python
category_names = {
    # ... 既存のマッピング
    "new_category": "新カテゴリ名",
}
```

### API開発

Swagger UIでAPIをテストできます:
- http://localhost:8000/docs

新しいエンドポイントを追加する場合は`backend/main.py`を編集してください。

### フロントエンド開発

```bash
cd frontend
npm run dev        # 開発サーバー起動
npm run build      # 本番ビルド
npm run start      # 本番サーバー起動
npm run lint       # ESLint実行
```

### デプロイ

#### Vercel (フロントエンド推奨)

```bash
cd frontend
vercel
```

#### AWS/GCP/Azure (バックエンド)

```bash
cd backend
# Dockerイメージ作成
docker build -t AIGenPrompts4U-backend .
docker run -p 8000:8000 -e OPENAI_API_KEY=xxx AIGenPrompts4U-backend
```

## 💡 使用例

### プロンプト表示モードの活用

#### シナリオ1: プロンプトライブラリの閲覧

```
1. サイドバー上部の「🎲 プロンプト表示」をクリック
2. 「Pythonエンジニア専門用」カテゴリを選択
3. 「🎲 プロンプト生成」をクリック
4. 150個のPython専門プロンプトが一覧表示される
5. 「FastAPI マイクロサービス設計専門家」を発見
6. 「📋 コピー」でプロンプトをコピーして外部ツールで使用
```

#### シナリオ2: プロンプトからチャットへ

```
1. プロンプト表示モードで「AIエンジニア専門用」を表示
2. 「MLOps パイプライン設計エキスパート」を発見
3. 「💬 チャット開始」ボタンをクリック
4. 自動的にチャットボットモードに切り替わり、プロンプトが設定される
5. そのままMLOpsについて質問を開始
```

### チャットボットモードの活用

#### 1. エラーログ分析
```
1. 「AIエンジニア専門用」カテゴリから「バグ原因特定エキスパート」を選択
2. PDFのエラーログファイルをアップロード (📕ボタン)
3. 「このエラーの原因と解決策を教えてください」と入力
→ AIがログを詳細分析して原因と複数の解決策を提示
```

#### 2. コードレビュー
```
1. 「プログラマー実践用」から「コードスメル検出・改善提案者」を選択
2. Pythonファイル(.py)を複数アップロード
3. 「リファクタリングの提案とベストプラクティスを教えてください」
→ コード品質分析、改善点、具体的なリファクタリング案を提示
```

#### 3. データ分析
```
1. 「Pythonエンジニア専門用」から「pandas最適化エキスパート」を選択
2. Excel/CSVファイルをアップロード (📊ボタン)
3. 「このデータの傾向分析と可視化コードを提案してください」
→ データ統計分析、グラフ作成コード、インサイト抽出
```

#### 4. 法律文書レビュー
```
1. 「法律家・弁護士実践用」から「契約書審査エキスパート」を選択
2. Word形式の契約書をアップロード (📘ボタン)
3. 「リスク条項と修正案を教えてください」
→ 契約リスク分析、問題条項指摘、修正案提示
```

#### 5. 経営戦略立案
```
1. 「CEO・エグゼクティブ用」から「中期経営計画策定アドバイザー」を選択
2. Excel形式の財務データをアップロード
3. 「向こう3年間の成長戦略を提案してください」
→ 市場分析、成長シナリオ、KPI設定、アクションプラン提示
```

#### 6. QOL改善プラン
```
1. 「QOL向上・ライフスタイル改善用」から「睡眠の質改善サポート」を選択
2. テキストファイルで睡眠記録をアップロード
3. 「睡眠改善の具体的なアドバイスをください」
→ 睡眠パターン分析、カスタマイズされた改善プラン提示
```

## トラブルシューティング

### バックエンド関連

#### エラー: ModuleNotFoundError: No module named 'fastapi'

→ バックエンドの依存パッケージをインストールしてください
```bash
cd backend
pip install -r requirements.txt
```

#### エラー: OpenAI API Keyが設定されていません

→ `backend/.env`ファイルを作成し、APIキーを設定してください
```bash
echo "OPENAI_API_KEY=your_actual_api_key_here" > backend/.env
```

#### バックエンドが起動しない

→ Pythonバージョンを確認してください（3.13以上推奨）
```bash
python --version
cd backend
python main.py
```

### フロントエンド関連

#### エラー: Cannot find module 'react-markdown'

→ フロントエンドの依存パッケージをインストールしてください
```bash
cd frontend
npm install
```

#### フロントエンドが起動しない

→ Node.jsバージョンを確認してください（18以上推奨）
```bash
node --version
cd frontend
npm run dev
```

#### ページが表示されない・真っ白

→ ブラウザのコンソールでエラーを確認してください（F12キー）
→ バックエンドが起動しているか確認してください（http://localhost:8000/docs）

### API通信関連

#### カテゴリやプロンプトが読み込まれない

→ CORS設定を確認してください（`backend/main.py`のCORSMiddleware）
→ バックエンドが http://localhost:8000 で起動しているか確認
→ フロントエンドの`.env.local`で`NEXT_PUBLIC_API_URL=http://localhost:8000`が設定されているか確認

#### チャットが応答しない

→ OpenAI APIキーが正しく設定されているか確認
→ OpenAI APIの利用制限やクレジットを確認
→ ブラウザのネットワークタブでAPIエラーを確認

### ファイルアップロード関連

#### PDFファイルからテキストが抽出できない

→ スキャンされた画像PDFはテキスト抽出できません（OCR処理が必要）
→ パスワード保護されたPDFは解除してください

#### Excelファイルが読み込めない

→ `.xls`形式は`.xlsx`形式に変換してください
→ ファイルが壊れていないか確認してください

#### ファイルアップロード後、エラーメッセージが表示される

→ ファイルのエンコーディングを確認してください（UTF-8、Shift-JIS、CP932に対応）
→ ファイルサイズを確認してください（1ファイル約60KB/15,000トークンまで）

### OpenAI API関連

#### エラー: Request too large / rate_limit_exceeded (429エラー)

OpenAI APIのトークン制限（30,000トークン/分）を超えています。

**対処方法**:
1. **ファイルサイズを減らす**
   - PDFファイル: 必要なページのみ抽出（10ページ以内推奨）
   - Excelファイル: 大きなシートは行数を減らす
   - テキストファイル: 関連部分のみをコピー

2. **アップロードファイル数を減らす**
   - 一度に2〜3ファイルまで
   - 大きなファイルは1ファイルずつ

3. **時間を空けて再試行**
   - レート制限は1分単位でリセット
   - 1〜2分待ってから再試行

### その他

#### 会話履歴が保存されない

→ `chat_history/`ディレクトリが存在するか確認
→ ファイル書き込み権限を確認
→ ディスク容量を確認

#### パフォーマンスが遅い

→ 大量の会話履歴を削除してください
→ ブラウザのキャッシュをクリアしてください
→ 他のアプリケーションを終了してリソースを確保

## ライセンス

MIT License

## 作成者

Hayashi Work

## 更新履歴

- **2025-11-19 v2.0**: React + TypeScript + FastAPI完全リニューアル 🎉
  - **フロントエンド全面刷新**: Next.js 16.0.3 + React 19 + TypeScript 6 + Tailwind CSS 4
  - **バックエンド新規構築**: FastAPI 0.115.0 + Python 3.13、RESTful API設計
  - **2モード実装**: 
    - 🎲 **プロンプト表示モード**: カテゴリ選択で全プロンプト自動生成、コピー機能、チャット連携
    - 💬 **チャットボットモード**: GPT-5ストリーミング対話、ファイルアップロード、会話履歴
  - **UI/UX大幅改善**: OpenWebUI inspired モダンデザイン、レスポンシブ対応、読みやすいカラースキーム
  - **ストリーミングチャット**: GPT-5リアルタイム応答、Server-Sent Events実装
  - **会話履歴管理**: 自動保存、読込、削除機能完備
  - **API仕様**: 8エンドポイント、Swagger UI対応
  - **型安全**: TypeScript + Pydantic、フルスタック型定義
  - **開発体験向上**: ホットリロード、ESLint、高速ビルド
  - **本番環境対応**: Vercel/Docker対応、スケーラブル設計
  - **レガシー保持**: Streamlit版も引き続き利用可能

- 2025-11-16 v1.14: GPT-5モデル対応 + 法律家・経営者・投資・QOL向上カテゴリ追加
  - **AIモデル更新**: OpenAI GPT-5に対応、より高度な推論能力と応答品質を実現
  - **新規カテゴリ追加**: 
    - lawyer(50個) - 契約審査、訴訟戦略、コンプライアンス等、法律実務の全領域
    - it_lawyer(50個) - ソフトウェア開発契約、GDPR、サイバーセキュリティ等、IT法務特化
    - ceo(50個) - 戦略的意思決定、M&A、企業価値向上等、経営トップ向け包括サポート
    - stock_trader(50個) - ファンダメンタル分析、テクニカル分析、トレーディング戦略
    - finance(50個) - 融資審査、資産運用、リスク管理等、金融業界全業務
    - qol(50個) - 睡眠改善、時間管理、ストレス対策等、QOL向上50施策
  - **コンサルタントカテゴリ拡充**: 10個→50個に拡充(DX変革、サプライチェーン最適化等40領域追加)
  - **合計**: 28カテゴリ、1,120個のプロンプト

- 2025-11-15 v1.12: ファイルアップロード機能大幅拡張 + トークン制限対策
  - **PDFファイル対応**: pdfplumberによるテキスト抽出、ページ単位の解析
  - **Wordファイル対応**: python-docxによる.docx文書の段落抽出
  - **Excelファイル対応強化**: 全シート読み込み、表形式テキスト変換、行数・列数表示
  - **CSVファイル対応強化**: 複数エンコーディング自動判別（UTF-8/Shift-JIS/CP932）
  - **テキストファイル改善**: 複数エンコーディング対応（UTF-8/Shift-JIS/CP932/Latin-1）
  - **チャットボット機能強化**: アップロードされたファイル内容を自動的にプロンプトに統合
  - **トークン制限対策**: 自動切り詰め機能（1ファイル最大15,000トークン）、3段階警告システム（20,000/25,000トークン）実装
  - **エラーハンドリング強化**: OpenAI API レート制限エラー(429)への対応、ユーザーフレンドリーな警告表示
  - 📕 PDF、📘 Word、📊 Excel、📄 CSV、📝 テキストの各ファイルタイプに対応アイコン追加

- 2025-11-13 v1.11: ChatGPT API活用専門カテゴリ追加
  - chatgpt_api(50個) - API基本統合、プロンプトエンジニアリング、RAG統合等
  - 合計22カテゴリ、780個

- 2025-11-13 v1.10: AIエンジニア専門カテゴリ追加
  - ai_engineer(50個) - 機械学習、深層学習、LLM、MLOps等
  - 合計21カテゴリ、730個

- 2025-11-13 v1.9: Pythonエンジニアカテゴリ最終拡充
  - python_engineer: 100個→150個(NumPy/pandas Advanced、asyncpg等追加)
  - 合計20カテゴリ、680個

- 2025-11-13 v1.8: Pythonエンジニアカテゴリ大幅拡充
  - python_engineer: 50個→100個(Flask/Django詳細、GraphQL等追加)
  - 合計20カテゴリ、630個

- 2025-11-13 v1.7: Pythonエンジニア専門カテゴリ追加
  - python_engineer(50個) - パフォーマンスチューニング、asyncio等
  - 合計20カテゴリ、580個

- 2025-11-13 v1.6: プログラマー実践カテゴリ追加
  - programmer(50個) - アルゴリズム、デバッグ、リファクタリング等
  - 合計19カテゴリ、530個

- 2025-11-13 v1.5: エンジニアカテゴリ大幅拡充
  - engineer: 100個→150個(TypeScript、React、Next.js等追加)
  - 合計18カテゴリ、480個

- 2025-11-12 v1.4: 教育・法律・SNS・起業カテゴリ追加
  - education, legal, sns_content, startup(各10個)
  - 合計18カテゴリ、430個

- 2025-11-11 v1.3: 面接・転職対策カテゴリ追加
  - job_interview(10個)
  - 合計14カテゴリ、390個

- 2025-11-11 v1.2: さらなるカテゴリ拡充
  - consultant, medical, investment, dating(各10個)
  - 合計13カテゴリ、380個

- 2025-11-11 v1.1: カテゴリ大幅拡充
  - engineer(100個), email, negotiation, meeting(各10個)
  - idea.json拡充(100個)
  - 合計9カテゴリ、340個

- 2025-11-11 v1.0: 初版リリース (Streamlit版)
  - サンプル抽出機能
  - OpenAI連携機能
  - 5カテゴリ対応(業界別100個、その他各10個)
