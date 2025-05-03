from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Emotion
from schemas.emotion import EmotionCreate, EmotionResponse
from core.database import get_db

router = APIRouter()

@router.get("/emotions")
async def get_emotions(db: Session = Depends(get_db)):
    emotions = db.query(Emotion).all()
    return emotions

@router.post("/emotions")
async def create_emotions(emotion_data: EmotionCreate, db: Session = Depends(get_db)):
    new_emotion = Emotion(emotion=emotion_data.emotion)
    db.add(new_emotion)
    db.commit()
    return new_emotion