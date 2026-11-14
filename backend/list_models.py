import httpx

r = httpx.get("https://openrouter.ai/api/v1/models", timeout=60)
for m in r.json()["data"]:
    p = m.get("pricing", {})
    if m["id"].endswith(":free") or p.get("prompt") == "0":
        print(m["id"], "|", m.get("name"))