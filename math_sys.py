import urllib.request, json, ssl, os

_K = "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"
_M = "deepseek/deepseek-v4-flash:free"

def solve(text):
    os.system('cls' if os.name == 'nt' else 'clear')
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {_K}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "User-Agent": "Mozilla/5.0"
    }
    
    payload = {
        "model": _M,
        "messages": [
            {"role": "system", "content": "Write SIMPLE Python code. Use vars like a,b,k,n. At the end, write 'ANSWER:' and the number."},
            {"role": "user", "content": text}
        ]
    }
    
    ctx = ssl._create_unverified_context()
    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=headers)
        with urllib.request.urlopen(req, context=ctx) as r:
            res = json.loads(r.read().decode())
            out = res['choices'][0]['message']['content']
            
            # Парсинг
            code = out.split("```python")[1].split("```")[0].strip() if "```python" in out else out
            ans = out.split("ANSWER:")[1].strip() if "ANSWER:" in out else "Error"
            
            with open("solution.py", "w", encoding="utf-8") as f:
                f.write(code + f"\n\n# ОТВЕТ: {ans}")
            
            print(f"\n[SYSTEM] Result: {ans}")
    except Exception as e:
        print(f"\n[!] Connection Error: {e}")
