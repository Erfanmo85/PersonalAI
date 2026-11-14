import os, httpx
from dotenv import load_dotenv
load_dotenv()

key = os.getenv("BEATAPI_API_KEY", "")
body = {"model": "glm-5.3-flash", "messages": [{"role": "user", "content": "hi"}], "max_tokens": 300}
hosts = ["https://direct.beatapi.io/v1", "https://api.beatapi.io/v1"]
uas = {"default": None,
       "browser": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"}

for h in hosts:
    for name, ua in uas.items():
        headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                   "Accept": "application/json"}
        if ua:
            headers["User-Agent"] = ua
        try:
            r = httpx.post(f"{h}/chat/completions", json=body, headers=headers, timeout=60)
            print(h, name, r.status_code, r.text[:200].replace("\n", " "))
        except Exception as e:
            print(h, name, r.status_code, r.text[:500])