from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
from config import VALID_API_KEYS, FREE_TRIAL_KEY, FREE_TIER_LIMIT
import re
import time
import os
from collections import defaultdict

app = FastAPI(
    title="YT Transcript API",
    description="Get full transcripts from any YouTube video. Instant JSON. Built for AI developers.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

free_tier_usage = defaultdict(lambda: {"count": 0, "reset_time": time.time() + 86400})

class TranscriptRequest(BaseModel):
    url: str
    language: str = "en"

def extract_video_id(url: str) -> str:
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})',
        r'(?:shorts\/)([0-9A-Za-z_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise HTTPException(status_code=400, detail="Invalid YouTube URL")

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key == FREE_TRIAL_KEY:
        now = time.time()
        usage = free_tier_usage[FREE_TRIAL_KEY]
        if now > usage["reset_time"]:
            usage["count"] = 0
            usage["reset_time"] = now + 86400
        if usage["count"] >= FREE_TIER_LIMIT:
            raise HTTPException(status_code=429, detail="Free tier daily limit reached. Upgrade on RapidAPI.")
        usage["count"] += 1
        return x_api_key
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

@app.get("/health")
def health():
    return {"status": "ok", "message": "YT Transcript API is running"}

COOKIES_FILE = "cookies.txt" if os.path.exists("cookies.txt") else None

PROXY_USERNAME = "ltymrejf"
PROXY_PASSWORD = "k81u2as19zyf"
PROXY_HOST = "31.59.20.176"
PROXY_PORT = "6754"

PROXIES = {
    "https": f"https://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}"
}

@app.post("/transcript")
def get_transcript(request: TranscriptRequest, api_key: str = Depends(verify_api_key)):
    video_id = extract_video_id(request.url)
    try:
        ytt_api = YouTubeTranscriptApi(proxies=PROXIES)
```

Save. Then push:
```
git add .
git commit -m "add proxy support"
git push
        fetched = ytt_api.fetch(video_id, languages=[request.language, 'en', 'en-US', 'en-GB'])
        snippets = fetched.snippets
        full_text = " ".join([s.text for s in snippets])
        duration = sum([s.duration for s in snippets])
        segments = [{"text": s.text, "start": s.start, "duration": s.duration} for s in snippets]
        return {
            "success": True,
            "video_id": video_id,
            "duration_seconds": round(duration),
            "word_count": len(full_text.split()),
            "transcript": full_text,
            "segments": segments
        }
    except TranscriptsDisabled:
        raise HTTPException(status_code=404, detail="Transcripts are disabled for this video")
    except NoTranscriptFound:
        raise HTTPException(status_code=404, detail="No transcript found for this video")
    except VideoUnavailable:
        raise HTTPException(status_code=404, detail="Video is unavailable")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/languages/{video_url:path}")
def get_available_languages(video_url: str, api_key: str = Depends(verify_api_key)):
    video_id = extract_video_id(video_url)
    try:
        ytt_api = YouTubeTranscriptApi(cookie_path=COOKIES_FILE) if COOKIES_FILE else YouTubeTranscriptApi()
        transcript_list = ytt_api.list(video_id)
        languages = []
        for t in transcript_list:
            languages.append({
                "language": t.language,
                "language_code": t.language_code,
                "is_generated": t.is_generated
            })
        return {"video_id": video_id, "available_languages": languages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
