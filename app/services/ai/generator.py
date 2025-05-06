from tenacity import retry, wait_fixed, stop_after_attempt, retry_if_exception_type
from openai import OpenAI, OpenAIError, APIError, RateLimitError, AuthenticationError
import base64
import uuid
import random
import time
from fastapi import HTTPException
from sqlalchemy.orm import Session

from core.config import settings
from services.ai.prompts import CHARACTER_PROMPTS, EMOTION_IMAGE_PROMPTS
from models.session import CharacterModeEnum
from models.message import ResponseTypeEnum
from models.emotion import Emotion
from utils.s3 import upload_to_s3
from utils.timestamp import now_jst

# OpenAIクライアント初期化
client = OpenAI(api_key=settings.openai_api_key)

# AI応答のOpenAI呼び出し（リトライ付き）
@retry(
    wait=wait_fixed(10),  # 10秒待つ
    stop=stop_after_attempt(3),  # 最大3回まで試す
    retry=retry_if_exception_type(RateLimitError)
)
# キャラモードに応じたAI返答を生成
def generate_ai_response(
    character_mode: CharacterModeEnum,
    user_input: str
    )->tuple[str, ResponseTypeEnum]:
    
    # ===テスト
    # models = client.models.list()
    # print([m.id for m in models.data])
    # ====確認用

    if character_mode == CharacterModeEnum.saburo:
        prompt_data = CHARACTER_PROMPTS["saburo"]
        response_type = None
    
    elif character_mode == CharacterModeEnum.bijyo:
        if random.randint(1, 5) == 1:
            prompt_data = CHARACTER_PROMPTS["anger-mom"]
            response_type = ResponseTypeEnum.insult
        else:
            prompt_data = CHARACTER_PROMPTS["bijyo"]
            response_type = ResponseTypeEnum.praise
            
    else:
        raise ValueError("無効なキャラクターモードです")
    
    system_prompt = prompt_data["description"] + "\n" + prompt_data["prompt"]
    user_diary = f"ユーザーの日記: {user_input}"
    
    try:
        response =  client.chat.completions.create(
            model = settings.openai_model,
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_diary}
            ]
        )
        ai_reply = response.choices[0].message.content.strip()
        return ai_reply, response_type
    
    # except RateLimitError:
    #     raise HTTPException(status_code=429, detail="APIのレート制限を超えました。しばらくしてから再度お試しください")
    except AuthenticationError:
        raise HTTPException(status_code=401, detail="OpenAIの認証に失敗しました。APIキーを確認してください")
    except APIError as e:
        print(f"OpenAIサーバでエラー: {e}")
        raise HTTPException(status_code=502, detail="OpenAIサーバでエラーが発生しました")
    except Exception as e:
        print(f"AI生成中のエラー: {e}")
        raise HTTPException(status_code=500, detail=f"AI応答の生成中にエラーが発生しました: {str(e)}")


# 感情に応じたプロンプトを取得 
def get_prompt_for_emotion(
    emotion_id: int,
    db: Session
)->str:
    emotion = db.get(Emotion,emotion_id)
    if not emotion:
        raise ValueError("該当する選択肢がありません")
    return EMOTION_IMAGE_PROMPTS.get(emotion.name.lower(), "A bright and happy illustration that encourages positivity")


# 画像を生成
def generate_image_bytes(prompt:str)->bytes:
    try:
        response = client.images.create(
            prompt=prompt,
            n=1,
            size="512x512",
            response_format="b64_json"
        )
        
        return base64.b64decode(response.data[0].b64_json)
    
    except RateLimitError:
        raise HTTPException(status_code=429, detail="APIのレート制限を超えました。しばらくしてから再度お試しください")
    except AuthenticationError:
        raise HTTPException(status_code=401, detail="OpenAIの認証に失敗しました。APIキーを確認してください")
    except APIError:
        raise HTTPException(status_code=502, detail="OpenAIサーバでエラーが発生しました")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"画像生成中にエラーが発生しました: {str(e)}")


# 画像生成してS3にアップロードする
def generate_and_upload_image(prompt: str)->str:
    image_bytes = generate_image_bytes(prompt)
    unique_filename = f"emotion_{now_jst().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}.png"
    
    return upload_to_s3(
        file_bytes=image_bytes,
        filename=unique_filename,
        content_type="image/png"
    )


# 画像のURLを作成
def generate_emotion_image_url(
    emotion_id: int,
    db:Session
)->str:
    prompt = get_prompt_for_emotion(emotion_id, db)
    return generate_and_upload_image(prompt)



