# AIGen10Prompts4U

システムプロンプトを自動生成するアプリケーション

## 概要

AIGen10Prompts4Uは、様々なシーンで使用できるシステムプロンプトを簡単に生成できるツールです。
100個以上のサンプルプロンプトから、用途に応じて10個を抽出したり、OpenAI APIを使って新しいプロンプトを生成することができます。

### 主な機能

- ✨ **サンプルからの抽出**: 100個以上の事前準備されたプロンプトから10個をランダム抽出
- 🤖 **AI生成**: OpenAI APIを使用してカスタムテーマのプロンプトを生成
- 📁 **豊富なカテゴリ**: 業界別、アイデア用、マネジメント用、営業用など多様なカテゴリ
- 📎 **添付ファイル推奨**: 各プロンプトに最適な添付ファイルの種類を提案
- 💾 **JSON出力**: 生成結果をJSON形式で保存し、再利用可能

## 利用可能なカテゴリ

| カテゴリ | 説明 | プロンプト数 | ファイル |
|---------|------|-------------|---------|
| industry | 業界別プロンプト | 100個 | industry.json |
| idea | アイデア創出用 | 100個 | idea.json |
| engineer | エンジニア用(全工程対応) | 100個 | engineer.json |
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

**合計14カテゴリ、390個のプロンプト**

## インストール

### 必要な環境

- Python 3.8以上

### セットアップ

1. リポジトリをクローン

```bash
git clone <repository-url>
cd AIGen10Prompts4U
```

2. 必要なパッケージをインストール

```bash
pip install -r requirements.txt
```

3. (オプション) OpenAI APIを使用する場合

`.env`ファイルを作成し、APIキーを設定:

```bash
cp .env.example .env
# .envファイルを編集してAPIキーを設定
```

## 使い方

### 基本的な使い方

1. **カテゴリ一覧を表示**

```bash
python src/main.py --list
```

2. **サンプルから10個のプロンプトを生成**

```bash
python src/main.py --category industry
```

3. **生成数を指定**

```bash
python src/main.py --category sales --count 5
```

4. **画面表示をスキップしてファイルのみ出力**

```bash
python src/main.py --category management --no-display
```

5. **出力ファイル名を指定**

```bash
python src/main.py --category idea --output my_prompts.json
```

### OpenAI APIを使用した生成

```bash
python src/main.py --use-openai --theme "スタートアップのマーケティング戦略" --count 10
```

環境変数でAPIキーを設定していない場合:

```bash
python src/main.py --use-openai --theme "データ分析アドバイザー" --api-key YOUR_API_KEY
```

## 出力例

生成されたプロンプトは`output/`ディレクトリに保存されます。

```json
{
  "category": "業界別",
  "generated_count": 10,
  "prompts": [
    {
      "id": 1,
      "title": "製造業DX戦略アドバイザー",
      "system_prompt": "あなたは製造業のデジタルトランスフォーメーション専門家です...",
      "recommended_attachments": [
        "工場レイアウト図",
        "現状の生産フロー図",
        "品質データCSV",
        "設備リスト"
      ]
    }
  ]
}
```

## プロジェクト構造

```
AIGen10Prompts4U/
├── src/
│   ├── main.py              # メインアプリケーション
│   └── openai_generator.py  # OpenAI API連携
├── prompts_data/
│   ├── industry.json        # 業界別プロンプト(100個)
│   ├── idea.json           # アイデア用プロンプト(100個)
│   ├── engineer.json       # エンジニア用プロンプト(100個)
│   ├── management.json     # マネジメント用プロンプト(10個)
│   ├── sales.json          # 営業用プロンプト(10個)
│   ├── summary.json        # 要約用プロンプト(10個)
│   ├── email.json          # メール返信用プロンプト(10個)
│   ├── negotiation.json    # 単価交渉用プロンプト(10個)
│   ├── meeting.json        # 会議カンペ作成用プロンプト(10個)
│   ├── consultant.json     # コンサルタント用プロンプト(10個)
│   ├── medical.json        # 医療用プロンプト(10個)
│   ├── investment.json     # 投資用プロンプト(10個)
│   ├── dating.json         # 恋愛・デート用プロンプト(10個)
│   └── job_interview.json  # 面接・転職対策用プロンプト(10個)
├── output/                  # 生成結果の出力先
├── requirements.txt         # 依存パッケージ
├── .env.example            # 環境変数のテンプレート
└── README.md               # このファイル
```

## 開発

### 新しいカテゴリを追加

1. `prompts_data/`に新しいJSONファイルを作成
2. `src/main.py`の`categories`辞書に追加
3. `load_prompts()`メソッドの`file_map`に追加

### プロンプトの形式

```json
{
  "category": "カテゴリ名",
  "prompts": [
    {
      "id": 1,
      "title": "プロンプトのタイトル",
      "system_prompt": "実際のシステムプロンプト内容",
      "recommended_attachments": [
        "推奨される添付ファイル1",
        "推奨される添付ファイル2"
      ]
    }
  ]
}
```

## トラブルシューティング

### エラー: プロンプトファイルが見つかりません

→ `prompts_data/`ディレクトリにJSONファイルが存在することを確認してください。

### エラー: OpenAI API Keyが設定されていません

→ `.env`ファイルを作成し、`OPENAI_API_KEY`を設定してください。

### モジュールが見つかりません

→ `pip install -r requirements.txt`を実行してください。

## ライセンス

MIT License

## 作成者

Hayashi Work

## 更新履歴

- 2025-11-11 v1.3: 面接・転職対策カテゴリ追加
  - **新規カテゴリ追加**: job_interview(10個)
  - **合計**: 14カテゴリ、390個のプロンプト

- 2025-11-11 v1.2: さらなるカテゴリ拡充
  - **新規カテゴリ追加**: consultant(10個), medical(10個), investment(10個), dating(10個)
  - **合計**: 13カテゴリ、380個のプロンプト
  
- 2025-11-11 v1.1: カテゴリ大幅拡充
  - **新規カテゴリ追加**: engineer(100個), email(10個), negotiation(10個), meeting(10個)
  - **既存カテゴリ拡充**: idea.jsonを100個に拡充
  - **合計**: 9カテゴリ、340個のプロンプト
  
- 2025-11-11 v1.0: 初版リリース
  - サンプル抽出機能
  - OpenAI連携機能
  - 5カテゴリ対応(業界別100個、その他各10個)