from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS設定
origins = [
    "http://localhost:3000",  # Reactのデフォルトポート
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the X-Post App Backend!"}

import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv() # .envファイルから環境変数を読み込む

# Gemini APIキーの設定
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY is not set. Please check your .env file.")
    # Optionally, you can raise an exception here to stop the server if the key is critical.
genai.configure(api_key=GEMINI_API_KEY)

@app.post("/generate_post")
async def generate_post(data: dict):
    poster_persona = data.get("poster_persona", "")
    reader_persona = data.get("reader_persona", "")
    post_theme = data.get("post_theme", "")
    keywords = data.get("keywords", "")

    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')

    # プロンプトの作成
    prompt = f"""
あなたはX（旧Twitter）の投稿文案を、マーケティング戦略に基づいて作成するAIアシスタントです。
以下の情報と制約事項を考慮し、読者の心に響く、戦略的なXの投稿文案を生成してください。

---
投稿者ペルソナ: {poster_persona}
読者ペルソナ: {reader_persona}
投稿テーマ: {post_theme}
キーワード: {keywords}
---

制約事項:
- **マーケティング視点**: 投稿の目的（例: 認知度向上、エンゲージメント獲得、ウェブサイトへの誘導、商品購入促進など）を意識し、読者の行動を促す内容にしてください。
- **読者への訴求**: 読者ペルソナの興味・関心、悩み、願望に深く寄り添い、共感や発見を促す言葉を選んでください。
- **フックの導入**: 投稿の冒頭で読者の注意を引きつける「フック」（問いかけ、驚き、共感、具体的なメリット提示など）を意識してください。
- **多様な表現**: 同じテーマでも、異なる切り口やトーン（例: 親しみやすい、専門的、ユーモラス、感動的など）を試み、表現の幅を広げてください。
- **具体的な行動喚起 (CTA)**: 必要に応じて、読者に具体的な行動（例: 「詳しくはこちら」「コメントで教えて」「リポストお願いします」など）を促す言葉を含めてください。
- 専門用語は避け、もし使う場合は簡単な言葉で説明を加えてください。
- ポジティブで、AIへの興味や活用を促す内容にしてください。
- ハッシュタグを3〜5個程度含めてください。
- 投稿は140文字程度に収まるようにしてください。
- 絵文字は最小限に留めてください。

生成する投稿文案:

生成する投稿文案:
"""
    try:
        response = model.generate_content(prompt)
        generated_text = response.text
    except Exception as e:
        print(f"Error generating content from Gemini API: {e}")
        generated_text = "AIによる投稿文案の生成中にエラーが発生しました。設定を見直してください。"

    return {"generated_text": generated_text}

@app.post("/upload_media")
async def upload_media():
    # ここにメディアアップロードのロジックを実装します
    # 現時点ではダミーのレスポンスを返します
    return {"message": "メディアアップロードのダミー処理が完了しました。"}
