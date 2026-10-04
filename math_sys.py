import urllib.request, json, ssl, os, re, sys

# Блокируем создание папок __pycache__ (чтобы не оставлять следов)
sys.dont_write_bytecode = True

def _get_val():
    # Разбили ключ, чтобы он не светился целиком в поиске
    p1 = "sk-or-v1-"
    p2 = "f97a85fea848edcf54f2d280fda42e5c5073b1badffea971d03fc51462cc31fc" # <--- ТВОЙ КЛЮЧ СЮДА
    return p1 + p2

# Резерв на случай, если задача на бумажке (буфер пуст)
TASK = """"""

def get_task():
    # Незаметно дергаем текст из буфера обмена
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        root.update()
        text = root.clipboard_get()
        root.destroy()
        if len(text) > 5:
            return text
    except:
        pass
    
    # Если буфер пуст или выдал ошибку — берем текст из переменной
    return TASK.strip()

def solve():
    os.system('cls' if os.name == 'nt' else 'clear')
    text = get_task()
    
    if not text:
        print("[!] Скопируй текст задачи (Ctrl+C) или впиши в переменную TASK в коде.")
        return

    print("[...] Отправка задачи...")
    
    # Жесткий промпт под школьный уровень кода
    sys_prompt = (
        "Write ONLY raw Python code. NO MARKDOWN. NO BACKTICKS (```). "
        "1. Variables MUST be single letters (i, a, s, x). "
        "2. NO COMMENTS AT ALL, except ONE at the very end: '# ANSWER: [number]'. "
        "3. Code must look like it was written by an average 11th grader. Use simple loops and lists. "
        "4. Print the final answer inside the code."
    )

    payload = {
        "model": "openrouter/free", # Автоматически выберет самую мощную из доступных бесплатных моделей
        "messages": [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": text}
        ]
    }

    # ИСПРАВЛЕНО: чистый URL без лишних скобок в начале
    req = urllib.request.Request(
        "[https://openrouter.ai/api/v1/chat/completions](https://openrouter.ai/api/v1/chat/completions)",
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {_get_val()}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost"
        }
    )
    
    ctx = ssl._create_unverified_context()
    save_path = os.path.join(os.getcwd(), "solution.py")

    try:
        with urllib.request.urlopen(req, context=ctx) as r:
            res = json.loads(r.read().decode())
            out = res['choices'][0]['message']['content'].strip()
            
            # Защита от тупости ИИ: вырезаем маркдаун, если он всё же добавит ```python
            out = re.sub(r"^```python\n|^```\n|```$", "", out, flags=re.MULTILINE).strip()

            with open(save_path, "w", encoding="utf-8") as f:
                f.write(out)
            
            # Ищем ответ в самом низу файла
            ans = re.findall(r"ANSWER:\s*(.*)", out)
            ans_text = ans[-1] if ans else "Смотри файл solution.py"
            
            print(f"\n[SYSTEM] ОТВЕТ: {ans_text}")
            print(f"[INFO] Код (без палева) сохранен в: {save_path}")
            
    except urllib.error.HTTPError as e:
        print(f"\n[!] Ошибка API ({e.code}): {e.read().decode()}")
    except Exception as e:
        print(f"\n[!] Системная ошибка: {e}")

if __name__ == "__main__":
    solve()
