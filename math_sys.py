import urllib.request, json, ssl, os, re, sys

# Блокировка кэша внутри модуля (на всякий случай)
sys.dont_write_bytecode = True

def _get_val():
    p1 = "sk-or-v1-1d26328dddd31cf3dce4724a63ee"
    p2 = "f154a9fa0c6c008d2fdc31f4f8010c529de2"
    return p1 + p2

_M = "deepseek/deepseek-v4-flash"

def solve(text):
    os.system('cls' if os.name == 'nt' else 'clear')
    api_url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {_get_val()}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "User-Agent": "Mozilla/5.0"
    }
    
    # Новый промпт под стиль "школьника"
    prompt_text = (
        "CRITICAL: Write ONLY RAW, simple Python code to solve the problem. DO NOT overcomplicate. "
        "CRITICAL RULES: "
        "1. Use ONLY extremely short, single-letter variable names (e.g., a, b, i, x, n). "
        "2. DO NOT write ANY comments in the code. Absolutely no explanations or text. "
        "3. NO markdown formatting, NO backticks (```). Just the working code. "
        "4. If a file is mentioned, assume it is in the current directory. "
        "5. At the very end of the script, calculate the result and add exactly this one mandatory comment: # ANSWER: [number]"
    )
    
    payload = {
        "model": _M,
        "messages": [
            {"role": "system", "content": prompt_text},
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
                out = f"# Ошибка: Модель не выдала код. Лог: {res}"

            out = str(out)

            with open(save_path, "w", encoding="utf-8") as f:
                f.write(out)
            
            ans_search = re.findall(r"ANSWER:\s*(\d+)", out)
            ans = ans_search[-1] if ans_search else "Смотри файл solution.py"
            
            print(f"\n[SYSTEM] ОТВЕТ: {ans}")
            print(f"[INFO] Код (без комментариев) создан тут: {save_path}")
            
    except urllib.error.HTTPError as e:
        err_msg = str(e.read().decode())
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(f"# Ошибка API: {e.code}\n{err_msg}")
        print(f"\n[!] Ошибка сервера ({e.code}). Проверь solution.py")
    except Exception as e:
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(f"# Ошибка Питона: {str(e)}")
        print(f"\n[!] Ошибка: {e}")
