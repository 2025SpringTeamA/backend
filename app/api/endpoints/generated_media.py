from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import GeneratedMedia
from app.models import GeneratedMedia
from app.schemas.generated_media import GeneratedMediaCreate, GeneratedMediaResponse
from app.core.database import get_db

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