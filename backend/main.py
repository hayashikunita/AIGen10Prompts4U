from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
from pathlib import Path
from datetime import datetime
import os
from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd
import io
import pdfplumber
from docx import Document as DocxDocument
import asyncio

# 環境変数を読み込む
load_dotenv()

app = FastAPI(title="AIGenPrompts4U API", version="1.0.0")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.jsのデフォルトポート
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ディレクトリ設定
PROMPTS_DIR = Path(__file__).parent.parent / "prompts_data"  # 親ディレクトリのprompts_data
CHAT_HISTORY_DIR = Path("chat_history")
CHAT_HISTORY_DIR.mkdir(exist_ok=True)

# OpenAI クライアント
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Pydantic モデル
class PromptData(BaseModel):
    id: int
    title: str
    system_prompt: str
    recommended_attachments: List[str]

class CategoryResponse(BaseModel):
    category: str
    prompts: List[PromptData]

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    system_prompt: Optional[str] = None

class ChatHistoryItem(BaseModel):
    filename: str
    title: str
    timestamp: str
    message_count: int

class SaveChatRequest(BaseModel):
    title: str
    messages: List[ChatMessage]
    selected_prompt: Optional[Dict[str, Any]] = None


# ユーティリティ関数
def estimate_tokens(text: str) -> int:
    """テキストのトークン数を概算"""
    return len(text) // 4

def truncate_content(content: str, max_tokens: int = 15000) -> tuple[str, bool]:
    """コンテンツが大きすぎる場合に切り詰める"""
    current_tokens = estimate_tokens(content)
    if current_tokens <= max_tokens:
        return content, False
    
    # 切り詰める
    max_chars = max_tokens * 4
    truncated = content[:max_chars]
    return truncated, True

async def read_file_content(file: UploadFile) -> tuple[str, str]:
    """アップロードされたファイルの内容を読み取る"""
    file_extension = Path(file.filename).suffix.lower()
    content = ""
    file_type = "text"
    
    try:
        # PDFファイル
        if file_extension == ".pdf":
            file_type = "pdf"
            file_bytes = await file.read()
            with io.BytesIO(file_bytes) as pdf_buffer:
                with pdfplumber.open(pdf_buffer) as pdf:
                    pages_text = []
                    for i, page in enumerate(pdf.pages, 1):
                        page_text = page.extract_text()
                        if page_text:
                            pages_text.append(f"--- ページ {i} ---\n{page_text}")
                    content = "\n\n".join(pages_text)
        
        # Wordファイル
        elif file_extension == ".docx":
            file_type = "word"
            file_bytes = await file.read()
            with io.BytesIO(file_bytes) as docx_buffer:
                doc = DocxDocument(docx_buffer)
                paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
                content = "\n\n".join(paragraphs)
        
        # Excelファイル
        elif file_extension in [".xlsx", ".xls"]:
            file_type = "excel"
            file_bytes = await file.read()
            excel_file = pd.ExcelFile(io.BytesIO(file_bytes))
            sheets_content = []
            
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(excel_file, sheet_name=sheet_name)
                sheet_text = f"=== シート: {sheet_name} ===\n"
                sheet_text += f"行数: {len(df)}, 列数: {len(df.columns)}\n\n"
                sheet_text += df.to_string(index=False)
                sheets_content.append(sheet_text)
            
            content = "\n\n".join(sheets_content)
        
        # CSVファイル
        elif file_extension == ".csv":
            file_type = "csv"
            file_bytes = await file.read()
            
            # エンコーディングを試す
            for encoding in ['utf-8', 'shift_jis', 'cp932']:
                try:
                    text = file_bytes.decode(encoding)
                    df = pd.read_csv(io.StringIO(text))
                    content = f"行数: {len(df)}, 列数: {len(df.columns)}\n\n"
                    content += df.to_string(index=False)
                    break
                except (UnicodeDecodeError, pd.errors.ParserError):
                    continue
        
        # テキストファイル
        else:
            file_bytes = await file.read()
            for encoding in ['utf-8', 'shift_jis', 'cp932', 'latin-1']:
                try:
                    content = file_bytes.decode(encoding)
                    break
                except UnicodeDecodeError:
                    continue
    
    except Exception as e:
        return f"error: {str(e)}", "error"
    
    return content, file_type


# API エンドポイント

@app.get("/")
async def root():
    return {"message": "AIGenPrompts4U API", "version": "1.0.0"}

@app.get("/api/categories")
async def get_categories():
    """利用可能なカテゴリ一覧を取得"""
    file_map = {
        "industry": "industry.json",
        "idea": "idea.json",
        "engineer": "engineer.json",
        "management": "management.json",
        "sales": "sales.json",
        "summary": "summary.json",
        "email": "email.json",
        "negotiation": "negotiation.json",
        "meeting": "meeting.json",
        "consultant": "consultant.json",
        "medical": "medical.json",
        "investment": "investment.json",
        "dating": "dating.json",
        "job_interview": "job_interview.json",
        "education": "education.json",
        "legal": "legal.json",
        "sns_content": "sns_content.json",
        "startup": "startup.json",
        "programmer": "programmer.json",
        "python_engineer": "python_engineer.json",
        "ai_engineer": "ai_engineer.json",
        "chatgpt_api": "chatgpt_api.json",
        "lawyer": "lawyer.json",
        "it_lawyer": "it_lawyer.json",
        "ceo": "ceo.json",
        "stock_trader": "stock_trader.json",
        "finance": "finance.json",
        "qol": "qol.json"
    }
    
    category_names = {
        "industry": "業界分析・市場調査用",
        "idea": "アイデア創出用",
        "management": "マネジメント用",
        "sales": "営業・セールス用",
        "summary": "要約・まとめ用",
        "engineer": "エンジニア用",
        "email": "メール返信用",
        "negotiation": "価格交渉用",
        "meeting": "会議準備用",
        "consultant": "コンサルティング用",
        "medical": "医療・健康相談用",
        "investment": "投資・資産運用用",
        "dating": "恋愛・デート用",
        "job_interview": "面接・転職対策用",
        "education": "教育・学習支援用",
        "legal": "法律・契約書用",
        "sns_content": "SNS・コンテンツ作成用",
        "startup": "起業・スタートアップ用",
        "programmer": "プログラマー実践用",
        "python_engineer": "Pythonエンジニア専門用",
        "ai_engineer": "AIエンジニア専門用",
        "chatgpt_api": "ChatGPT API活用専門用",
        "lawyer": "法律家・弁護士実践用",
        "it_lawyer": "IT法務・テック法律家専門用",
        "ceo": "経営者サポート・エグゼクティブ用",
        "stock_trader": "日本株トレーダー・投資家用",
        "finance": "金融業界・銀行実践用",
        "qol": "QOL向上・ライフスタイル改善用"
    }
    
    return {
        "categories": [
            {"key": key, "name": category_names.get(key, key), "file": file}
            for key, file in file_map.items()
        ]
    }

@app.get("/api/prompts/{category}")
async def get_prompts(category: str):
    """指定カテゴリのプロンプト一覧を取得"""
    file_path = PROMPTS_DIR / f"{category}.json"
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Category not found")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """チャット応答を生成（ストリーミング）"""
    if not openai_client.api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
    
    messages = []
    
    # システムプロンプトを追加
    if request.system_prompt:
        messages.append({"role": "system", "content": request.system_prompt})
    
    # ユーザーメッセージを追加
    for msg in request.messages:
        messages.append({"role": msg.role, "content": msg.content})
    
    async def generate():
        try:
            stream = openai_client.chat.completions.create(
                model="gpt-5",
                messages=messages,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield f"data: {json.dumps({'content': chunk.choices[0].delta.content})}\n\n"
            
            yield "data: [DONE]\n\n"
        
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """ファイルをアップロードして内容を取得"""
    content, file_type = await read_file_content(file)
    
    if file_type == "error":
        raise HTTPException(status_code=400, detail=content)
    
    # コンテンツを切り詰める
    truncated_content, was_truncated = truncate_content(content, max_tokens=15000)
    
    return {
        "filename": file.filename,
        "file_type": file_type,
        "content": truncated_content,
        "truncated": was_truncated,
        "size": len(content)
    }

@app.get("/api/chat-history")
async def get_chat_history():
    """チャット履歴一覧を取得"""
    histories = []
    
    for filepath in sorted(CHAT_HISTORY_DIR.glob("*.json"), reverse=True):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                histories.append({
                    "filename": filepath.name,
                    "title": data.get("title", "無題"),
                    "timestamp": data.get("timestamp", ""),
                    "message_count": len(data.get("messages", []))
                })
        except Exception:
            continue
    
    return {"histories": histories}

@app.get("/api/chat-history/{filename}")
async def get_chat_history_detail(filename: str):
    """特定のチャット履歴を取得"""
    filepath = CHAT_HISTORY_DIR / filename
    
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="History not found")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data

@app.post("/api/chat-history")
async def save_chat_history(request: SaveChatRequest):
    """チャット履歴を保存"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{request.title}_{timestamp}.json"
    filepath = CHAT_HISTORY_DIR / filename
    
    history_data = {
        "title": request.title,
        "timestamp": timestamp,
        "messages": [{"role": m.role, "content": m.content} for m in request.messages],
        "selected_prompt": request.selected_prompt
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(history_data, f, ensure_ascii=False, indent=2)
    
    return {"filename": filename, "message": "Chat history saved successfully"}

@app.delete("/api/chat-history/{filename}")
async def delete_chat_history(filename: str):
    """チャット履歴を削除"""
    filepath = CHAT_HISTORY_DIR / filename
    
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="History not found")
    
    filepath.unlink()
    return {"message": "Chat history deleted successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
