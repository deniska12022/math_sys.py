import urllib.request, json, ssl, os, re, sys

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
            {"role": "system", "content": "Solve math task. Write only Python code. At the end of the code, add a comment with the exact format: # ANSWER: [number]"},
            {"role": "user", "content": text}
        ]
    }
    
    ctx = ssl._create_unverified_context()
    
    try:
        run_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    except:
        run_dir = os.getcwd() 
        
    save_path = os.path.join(run_dir, "solution.py")
    
    try:
        req = urllib.request.Request(api_url, data=json.dumps(payload).encode(), headers=headers)
        with urllib.request.urlopen(req, context=ctx) as r:
            res = json.loads(r.read().decode())
            
            out = ""
            if 'choices' in res and res['choices']:
                out = res['choices'][0].get('message', {}).get('content')
            
            if out is None:
                out = f"# Ошибка: АПИ прислало пустой ответ. Лог: {res}"

            out = str(out)

            with open(save_path, "w", encoding="utf-8") as f:
                f.write(out)
            
            ans_search = re.findall(r"ANSWER:\s*(\d+)", out)
            ans = ans_search[-1] if ans_search else "Смотри файл solution.py"
            
            print(f"\n[SYSTEM] ОТВЕТ: {ans}")
            print(f"[INFO] Файл создан тут: {save_path}")
            
    except urllib.error.HTTPError as e:
        err_msg = str(e.read().decode())
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(f"# Ошибка API: {e.code}\n{err_msg}")
        print(f"\n[!] Ошибка сервера ({e.code}). Проверь solution.py")
    except Exception as e:
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(f"# Ошибка Питона: {str(e)}")
        print(f"\n[!] Ошибка: {e}")
