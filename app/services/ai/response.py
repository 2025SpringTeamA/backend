import openai
import random
from core.config import settings
from services.ai.characters import CHARACTER_PROMPTS
from models.session import CharacterModeEnum
from models.message import ResponseTypeEnum

openai.api_key = settings.openai_api_key

# キャラモードに応じたAI返答を生成。
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
    
    response = openai.ChatCompletion.create(
        model = settings.openai_model,
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_diary}
        ]
    )
    ai_reply = response.choices[0].message.content.strip()
    return ai_reply, response_type

