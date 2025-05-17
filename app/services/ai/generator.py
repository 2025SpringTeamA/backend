from tenacity import retry, wait_fixed, stop_after_attempt, retry_if_exception_type
from botocore.exceptions import NoCredentialsError, ClientError, EndpointConnectionError
from openai import OpenAI, OpenAIError, APIError, RateLimitError, AuthenticationError
import base64
import uuid
import random
import boto3
import json
import re
from fastapi import HTTPException
from sqlalchemy.orm import Session

from core.config import settings
from services.ai.prompts import CHARACTER_PROMPTS
from models.session import CharacterModeEnum
from models.message import ResponseTypeEnum


# ============================================
# AWS Bedrock(Claude Instantモデル)版AI応答生成
# ===========================================

# bedrock = boto3.client("bedrock-runtime", region_name=settings.REGION)

# 起動時 or 初回リスエスト時に接続確認
def verify_bedrock_connection():
    try:
        mgmt_client = boto3.client("bedrock", region_name=settings.REGION)
        response = mgmt_client.list_foundation_models()
        print(f"✅ Bedrock接続確認：利用可能モデル数 = {len(response['modelSummaries'])}")
    except NoCredentialsError:
        raise RuntimeError("❌ AWS認証情報が見つかりません。")
    except EndpointConnectionError:
        raise RuntimeError("❌ Bedrock エンドポイントに接続できません。region_name=settings.REGION を確認してください。")
    except ClientError as e:
        raise RuntimeError(f"❌ Bedrockクライアントエラー: {e}")
    except Exception as e:
        raise RuntimeError(f"❌ Bedrock接続失敗: {e}")


# アプリ起動時にBedrock接続確認
verify_bedrock_connection()

@retry( # 関数失敗時にリトライ
    wait=wait_fixed(10), # 10秒まつ
    stop=stop_after_attempt(3) # 最大３回試行
    )
def generate_ai_response_via_bedrock(
    character_mode: CharacterModeEnum,
    user_input: str
    )->tuple[str, ResponseTypeEnum]:
    
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
    
    # Claude形式のプロンプトを作成
    prompt = f"Human: {prompt_data['description']}\n{prompt_data['prompt']}\nユーザーの日記：{user_input}\nAssistant:"
    
    try:
        response = bedrock.invoke_model(
            modelId = settings.MODEL_ID,
            body = json.dumps({
                "prompt": prompt,
                "max_tokens_to_sample": 128,  # 最大出力トークン（1文字=約1.5トークン。50文字の出力を想定）
                "temperature": 0.7, # 返答の自由さ（１に近いほど自由）
                "stop_sequences": ["\n\n", "Human", "ユーザー:"] # AIの出力を終了する区切り
            }),
            contentType ="application/json",
            accept = "application/json"
        )
        response_body = json.loads(response["body"].read())
        bedrock_reply = response_body["completion"].strip()
        
        # 句点で切る
        ai_reply = stop_generate_sentence(bedrock_reply)
        
        return ai_reply, response_type
    
    except bedrock.exceptions.AccessDeniedException:
        raise HTTPException(status_code=403, detail="Bedrockへのアクセスが拒否されました")
    except Exception as e:
        print(f"Bedrockエラー: {e}")
        raise HTTPException(status_code=500, detail=f"AI応答の生成中にエラーが発生しました: {str(e)}")


# Bedrockの出力を句点で切る
def stop_generate_sentence(text: str)-> str:
    # （。！？）までを残す
    match = re.search(r'[。！？](?!.*[。！？])', text)
    if match:
        return text[:match.end()]
    return text



# =========================
# OpenAIキー版　AI応答生成
# =========================

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
    
    
    except AuthenticationError:
        raise HTTPException(status_code=401, detail="OpenAIの認証に失敗しました。APIキーを確認してください")
    except APIError as e:
        print(f"OpenAIサーバでエラー: {e}")
        raise HTTPException(status_code=502, detail="OpenAIサーバでエラーが発生しました")
    except Exception as e:
        print(f"AI生成中のエラー: {e}")
        raise HTTPException(status_code=500, detail=f"AI応答の生成中にエラーが発生しました: {str(e)}")