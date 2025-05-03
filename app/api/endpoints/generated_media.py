from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import GeneratedMedia
from schemas.generated_media import GeneratedMediaCreate, GeneratedMediaResponse
from core.database import get_db

router = APIRouter()

@router.post("/generated-media")
async def create_generated_media(media_data: GeneratedMediaCreate, db: Session = Depends(get_db)):
    new_media = GeneratedMedia(
        message_id=media_data.message_id,
        emotion_id=media_data.emotion_id,
        media_url=media_data.media_url,
        media_type=media_data.media_type
    ) 
    db.add(new_media)
    db.commit()
    return new_media