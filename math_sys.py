import urllib.request, json, ssl, os

def _get_val():
    p1 = "sk-or-v1-ea44eb416aaf3555c202ce9a16284de9"
    p2 = "e743e4032fed2270cde487da31f807c7"
    return p1 + p2

_M = "deepseek/deepseek-v4-flash:free"

def solve(text):
    os.system('cls' if os.name == 'nt' else 'clear')
    api_url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {_get_val()}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "User-Agent": "Mozilla/5.0"
    }
    
    payload = {
        "model": _M,
        "messages": [
            {"role": "system", "content": "You are a math solver. Write Python code and then 'ANSWER: [number]'."},
            {"role": "user", "content": text}
        ]
    }
    
    ctx = ssl._create_unverified_context()
    try:
        req = urllib.request.Request(api_url, data=json.dumps(payload).encode(), headers=headers)
        with urllib.request.urlopen(req, context=ctx) as r:
            res = json.loads(r.read().decode())
            
            if 'choices' not in res:
                print(f"[!] Ошибка API: {res}")
                return

            out = res['choices'][0]['message']['content']
            
            # Умный поиск кода
            code = "No code found"
            if "```python" in out:
                code = out.split("```python")[1].split("```")[0].strip()
            elif "```" in out:
                code = out.split("```")[1].split("```")[0].strip()
            
            # Умный поиск ответа
            ans = "Not found"
            if "ANSWER:" in out:
                ans = out.split("ANSWER:")[1].strip().split('\n')[0]
            
            with open("solution.py", "w", encoding="utf-8") as f:
                f.write(out) # Сохраняем весь текст для анализа
            
            print(f"\n[SYSTEM] Done. Result: {ans}")
            print(f"[INFO] Full response saved to solution.py")
            
    except Exception as e:
        print(f"\n[!] Error: {e}")
