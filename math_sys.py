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
            {"role": "system", "content": "Solve math task. Write only Python code. At the end of the code, add a comment with the answer like this: # ANSWER: [number]"},
            {"role": "user", "content": text}
        ]
    }
    
    ctx = ssl._create_unverified_context()
    
    try:
        req = urllib.request.Request(api_url, data=json.dumps(payload).encode(), headers=headers)
        with urllib.request.urlopen(req, context=ctx) as r:
            res = json.loads(r.read().decode())
            
            # Проверка на наличие контента
            if 'choices' in res and res['choices']:
                out = res['choices'][0].get('message', {}).get('content', "")
            else:
                out = f"# Error: No response from API\n# Full response: {res}"

            # Если out каким-то чудом None, превращаем в строку
            if out is None:
                out = "# Error: Received None from API"

            # Создаем файл с кодом и ответом
            with open("solution.py", "w", encoding="utf-8") as f:
                f.write(out)
            
            # Пытаемся вытащить число для консоли (ищем после слова ANSWER)
            ans_search = re.findall(r"ANSWER:\s*(\d+)", out)
            ans = ans_search[-1] if ans_search else "Check solution.py"
            
            print(f"\n[SYSTEM] ОТВЕТ: {ans}")
            print(f"[INFO] Решение сохранено в solution.py")
            
    except Exception as e:
        error_msg = f"# Connection Error: {str(e)}"
        with open("solution.py", "w", encoding="utf-8") as f:
            f.write(error_msg)
        print(f"\n[!] Ошибка: {e}")
