"""
AIGen10Prompts4U - システムプロンプト生成アプリケーション

このアプリケーションは、様々なカテゴリのシステムプロンプトを生成します。
- サンプルから10個をランダム抽出
- OpenAI APIを使用して新規作成(オプション)
"""

import json
import random
import os
from pathlib import Path
from typing import List, Dict, Optional
import argparse


class PromptGenerator:
    """システムプロンプト生成クラス"""
    
    def __init__(self, prompts_dir: str = "prompts_data", output_dir: str = "output"):
        self.prompts_dir = Path(prompts_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # 利用可能なカテゴリ
        self.categories = {
            "industry": "業界別",
            "idea": "アイデア用",
            "management": "マネジメント用",
            "sales": "営業用",
            "summary": "要約用",
            "engineer": "エンジニア用",
            "consultant": "コンサルタント用",
            "sales_talk": "セールストーク用",
            "investment": "投資用",
            "dating": "恋愛・デート用",
            "email": "メール返信用",
            "medical": "医療用",
            "negotiation": "単価交渉用",
            "meeting": "会議カンペ作成用"
        }
    
    def list_categories(self) -> Dict[str, str]:
        """利用可能なカテゴリを表示"""
        return self.categories
    
    def load_prompts(self, category: str) -> List[Dict]:
        """指定カテゴリのプロンプトを読み込む"""
        file_map = {
            "industry": "industry.json",
            "idea": "idea.json",
            "management": "management.json",
            "sales": "sales.json",
            "summary": "summary.json",
            "engineer": "engineer.json",
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
            "programmer": "programmer.json"
        }
        
        if category not in file_map:
            raise ValueError(f"カテゴリ '{category}' は現在準備中です。")
        
        file_path = self.prompts_dir / file_map[category]
        if not file_path.exists():
            raise FileNotFoundError(f"プロンプトファイルが見つかりません: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data.get("prompts", [])
    
    def generate_from_samples(self, category: str, count: int = 10) -> List[Dict]:
        """サンプルからランダムに抽出"""
        prompts = self.load_prompts(category)
        
        if len(prompts) < count:
            print(f"警告: 利用可能なプロンプトは{len(prompts)}個です。")
            count = len(prompts)
        
        selected = random.sample(prompts, count)
        return selected
    
    def save_output(self, prompts: List[Dict], category: str, filename: Optional[str] = None):
        """生成結果をファイルに保存"""
        if filename is None:
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{category}_{timestamp}.json"
        
        output_path = self.output_dir / filename
        
        output_data = {
            "category": self.categories.get(category, category),
            "generated_count": len(prompts),
            "prompts": prompts
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ 生成完了: {output_path}")
        return output_path
    
    def display_prompts(self, prompts: List[Dict]):
        """生成されたプロンプトを表示"""
        print("\n" + "="*80)
        print(f"生成されたシステムプロンプト ({len(prompts)}個)")
        print("="*80 + "\n")
        
        for i, prompt in enumerate(prompts, 1):
            print(f"[{i}] {prompt.get('title', '無題')}")
            print("-" * 80)
            print(f"システムプロンプト:")
            print(prompt.get('system_prompt', ''))
            print(f"\n推奨添付ファイル:")
            attachments = prompt.get('recommended_attachments', [])
            for att in attachments:
                print(f"  • {att}")
            print("\n")


def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(
        description='AIGen10Prompts4U - システムプロンプト生成アプリ',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # カテゴリ一覧を表示
  python src/main.py --list
  
  # 業界別プロンプトを10個生成
  python src/main.py --category industry
  
  # アイデア用プロンプトを5個生成
  python src/main.py --category idea --count 5
  
  # 結果を表示せずファイルのみ出力
  python src/main.py --category sales --no-display
        """
    )
    
    parser.add_argument('--list', action='store_true',
                       help='利用可能なカテゴリを表示')
    parser.add_argument('--category', type=str,
                       help='プロンプトのカテゴリを指定')
    parser.add_argument('--count', type=int, default=10,
                       help='生成するプロンプトの数 (デフォルト: 10)')
    parser.add_argument('--no-display', action='store_true',
                       help='画面への表示をスキップ')
    parser.add_argument('--output', type=str,
                       help='出力ファイル名を指定')
    
    args = parser.parse_args()
    
    generator = PromptGenerator()
    
    # カテゴリ一覧を表示
    if args.list:
        print("\n利用可能なカテゴリ:")
        print("-" * 50)
        for key, name in generator.list_categories().items():
            print(f"  {key:15s} : {name}")
        print("-" * 50)
        print("\n使用方法: python src/main.py --category <カテゴリ名>")
        return
    
    # カテゴリが指定されていない場合
    if not args.category:
        print("エラー: カテゴリを指定してください。")
        print("カテゴリ一覧: python src/main.py --list")
        return
    
    try:
        # プロンプトを生成
        print(f"\n{generator.categories.get(args.category, args.category)} のプロンプトを生成中...")
        prompts = generator.generate_from_samples(args.category, args.count)
        
        # 結果を表示
        if not args.no_display:
            generator.display_prompts(prompts)
        
        # ファイルに保存
        output_path = generator.save_output(prompts, args.category, args.output)
        
        print(f"\n生成されたプロンプト数: {len(prompts)}")
        print(f"出力ファイル: {output_path}")
        
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
