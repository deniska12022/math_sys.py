import urllib.request, json, ssl, os, re

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
            {"role": "system", "content": "Solve math task. Write Python code. At the very end, write 'ANSWER: ' and only the final integer number."},
            {"role": "user", "content": text}
        ]
    }
    
    ctx = ssl._create_unverified_context()
    
    try:
        req = urllib.request.Request(api_url, data=json.dumps(payload).encode(), headers=headers)
        with urllib.request.urlopen(req, context=ctx) as r:
            res = json.loads(r.read().decode())
            out = res['choices'][0]['message']['content']
            
            with open("solution.py", "w", encoding="utf-8") as f:
                f.write(out)
            
            if "ANSWER:" in out:
                raw_ans = out.split("ANSWER:")[1].strip().split('\n')[0]
                ans = re.sub(r'[^0-9]', '', raw_ans)
                print(f"\n[SYSTEM] ОТВЕТ: {ans}")
            else:
                print("\n[SYSTEM] Готово. Проверь solution.py")
            
    except Exception as e:
        print(f"\n[!] Ошибка: {e}")
