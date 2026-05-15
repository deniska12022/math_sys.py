import urllib.request, json, ssl, os

def _get_val():
    # Твой текущий ключ
    p1 = "sk-or-v1-ea44eb416aaf3555c202ce9a16284de9"
    p2 = "e743e4032fed2270cde487da31f807c7"
    return p1 + p2

_M = "deepseek/deepseek-v4-flash:free"

def solve(text):
    # Чистим консоль
    os.system('cls' if os.name == 'nt' else 'clear')
    
    api_url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {_get_val()}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "User-Agent": "Mozilla/5.0"
    }
    
    # Просим ИИ выдать только код и ответ в нужном формате
    payload = {
        "model": _M,
        "messages": [{"role": "user", "content": text + "\nWrite simple Python code. Format: ANSWER: [number]"}]
    }
    
    ctx = ssl._create_unverified_context()
    
    try:
        req = urllib.request.Request(api_url, data=json.dumps(payload).encode(), headers=headers)
        with urllib.request.urlopen(req, context=ctx) as r:
            res = json.loads(r.read().decode())
            
            # Проверка структуры ответа
            if 'choices' not in res or not res['choices']:
                print(f"\n[!] Ошибка сервера или лимитов. Ответ: {res}")
                return

            out = res['choices'][0].get('message', {}).get('content', "")
            
            if not out:
                print("\n[!] Модель вернула пустой ответ.")
                return

            # Сохраняем полный ответ в solution.py для подстраховки
            with open("solution.py", "w", encoding="utf-8") as f:
                f.write(out)
            
            # Пытаемся достать только цифру
            if "ANSWER:" in out:
                ans = out.split("ANSWER:")[1].strip().split('\n')[0].replace('*', '').strip()
                print(f"\n[SYSTEM] Result: {ans}")
            else:
                print("\n[SYSTEM] Готово. Код и ответ сохранены в solution.py")
            
    except Exception as e:
        print(f"\n[!] Ошибка соединения или ключа: {e}")
