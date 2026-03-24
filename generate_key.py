import secrets
import string

def generate_api_key(prefix="yt_"):
    chars = string.ascii_letters + string.digits
    random_part = ''.join(secrets.choice(chars) for _ in range(32))
    return f"{prefix}{random_part}"

if __name__ == "__main__":
    print("Your new API keys:")
    for i in range(5):
        print(generate_api_key())
```

---

Tell me when saved. Then check your folder — you should have exactly these 6 files:
```
yt-transcript-api/
├── main.py
├── config.py
├── requirements.txt
├── Procfile
├── railway.json
└── generate_key.py