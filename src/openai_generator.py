"""
OpenAI APIを使用したプロンプト生成機能
"""

import os
from typing import List, Dict, Optional
import json


class OpenAIPromptGenerator:
    """OpenAI APIを使用してプロンプトを生成するクラス"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError("OpenAI API Keyが設定されていません。")
        
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError("openaiライブラリがインストールされていません。pip install openai を実行してください。")
    
    def generate_prompts(self, theme: str, count: int = 10, category: str = None) -> List[Dict]:
        """指定されたテーマでプロンプトを生成"""
        
        system_message = """あなたは優秀なプロンプトエンジニアです。
指定されたテーマに基づいて、効果的なシステムプロンプトを生成してください。

各プロンプトには以下を含めてください:
1. title: プロンプトの簡潔なタイトル
2. system_prompt: 実際のシステムプロンプト(具体的で実用的な内容)
3. recommended_attachments: 推奨される添付ファイルのリスト(4-6個)

出力はJSON配列形式で返してください。
"""
        
        user_message = f"""テーマ: {theme}
カテゴリ: {category if category else '指定なし'}
生成数: {count}個

上記のテーマに基づいて、実用的で多様なシステムプロンプトを{count}個生成してください。
それぞれのプロンプトは異なる視点やアプローチを持つようにしてください。
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.8,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            result = json.loads(content)
            
            # レスポンスの形式を正規化
            if "prompts" in result:
                prompts = result["prompts"]
            elif isinstance(result, list):
                prompts = result
            else:
                prompts = [result]
            
            # IDを付与
            for i, prompt in enumerate(prompts, 1):
                prompt["id"] = i
            
            return prompts
            
        except Exception as e:
            print(f"OpenAI API呼び出しエラー: {e}")
            raise


def add_openai_args(parser):
    """OpenAI関連の引数をargparserに追加"""
    parser.add_argument('--use-openai', action='store_true',
                       help='OpenAI APIを使用して新規生成')
    parser.add_argument('--theme', type=str,
                       help='生成するプロンプトのテーマ')
    parser.add_argument('--api-key', type=str,
                       help='OpenAI API Key (環境変数OPENAI_API_KEYでも設定可)')
