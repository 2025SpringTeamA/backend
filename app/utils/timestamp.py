# app/utils/time.py
from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9以降

def now_jst():
    """日本時間 (JST) の現在時刻を返す"""
    return datetime.now(ZoneInfo("Asia/Tokyo"))
