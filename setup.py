import os

# === ВЕСЬ КОД БИБЛИОТЕКИ ЗАШИТ ПРЯМО СЮДА ===
MATH_SYS_CODE = """import urllib.request, json, ssl, os, re, sys

# Жесткая блокировка создания папки __pycache__ внутри модуля
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
    
    # МАКСИМАЛЬНО ЖЕСТКИЙ ПРОМПТ
    prompt_text = (
        "CRITICAL: Write ONLY RAW Python code. VIOLATING THESE RULES CAUSES A SYSTEM FAILURE: "
        "1. FORBIDDEN: Words as variables. YOU MUST USE ONLY SINGLE-LETTER VARIABLES (e.g., a, b, f, m, c, i). "
        "2. FORBIDDEN: Comments. DO NOT use the '#' symbol ANYWHERE in the code to explain logic. ZERO comments. "
        "3. FORBIDDEN: Markdown. DO NOT wrap code in ```. Just pure text. "
        "4. If reading a file, assume it's in the current folder. "
        "5. The ONLY allowed text at the very end of the file is: # ANSWER: [number]"
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
            
            print(f"\\n[SYSTEM] ОТВЕТ: {ans}")
            print(f"[INFO] Код создан тут: {save_path}")
            
    except urllib.error.HTTPError as e:
        err_msg = str(e.read().decode())
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(f"# Ошибка API: {e.code}\\n{err_msg}")
        print(f"\\n[!] Ошибка сервера ({e.code}). Проверь solution.py")
    except Exception as e:
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(f"# Ошибка Питона: {str(e)}")
        print(f"\\n[!] Ошибка: {e}")
"""

def inject():
    # Находим папку, откуда запустили этот скрипт
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
    except:
        current_dir = os.getcwd()
        
    target = os.path.join(current_dir, "math_sys.py")
    
    try:
        # Создаем файл библиотеки прямо рядом
        with open(target, 'w', encoding='utf-8') as f:
            f.write(MATH_SYS_CODE)
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print("----------------------------------------")
        print("  SYSTEM READY. БИБЛИОТЕКА СОЗДАНА ТУТ: ")
        print(f"  {target}")
        print("----------------------------------------")
    except Exception as e:
        print(f"\n[!] Ошибка распаковки: {e}")

if __name__ == "__main__":
    inject()

# ====================================================
# ====================================================
# 1. Запустил этот скрипт (F5). Появится файл math_sys.py рядом.
# 2. Стер весь этот код.
# 3. Пишешь этот код для блокировки кэша и решения сложных задач:
#
# import sys
# sys.dont_write_bytecode = True
# import math_sys as ms
# ms.solve(""" СЮДА ТЕКСТ ЗАДАЧИ """)

# ====================================================
# ====================================================
"""
--- 5. ТАБЛИЦЫ ИСТИННОСТИ ---
# Знаки: -> (<=), ≡ (==), ∧ (and), ∨ (or), ¬ (not)
for x in 0, 1:
    for y in 0, 1:
        for z in 0, 1:
            for w in 0, 1:
                f = ((x <= z) and (z <= w)) or (y == (x <= z))
                if f == 0: print(x, y, z, w)

--- 6. КОМБИНАТОРИКА (СЛОВА) ---
from itertools import product
k = 0
for w in product("БДЕКНТЦЧЭ", repeat=6): # Строго по алфавиту!
    k += 1
    s = "".join(w)
    if k % 2 == 0 and s[0] != "Н" and s[-1] != "Н" and s.count("Е") >= 3:
        print(k); break

--- 7. IP И МАСКИ ---
# Прямая (номер узла):
ip_part = 227; mask_part = 248
print(ip_part & (255 - mask_part))
# Обратная (поиск маски):
ip_byte = 211; net_byte = 192
for m in [0, 128, 192, 224, 240, 248, 252, 254, 255]:
    if ip_byte & m == net_byte: print(m)

--- 8. ПАРОЛИ (ВЕС) ---
import math
pass_bytes = math.ceil((23 * 6) / 8) # Округление ВВЕРХ (байт/пароль)
max_users = (20 * 1024) // (pass_bytes + 10) # Округление ВНИЗ (люди)
print(max_users)

--- 10. СИСТЕМЫ СЧИСЛЕНИЯ С X ---
for x in "0123456789ABCDEFGHI":
    total = int(f"55{x}36", 19) + int(f"{x}2724", 19)
    if total % 11 == 0:
        print(total // 11); break

--- 11. ДОП. КОД (ОТРИЦАТЕЛЬНЫЕ) ---
print(bin(-92 & 0xFF)[2:]) # 0xFF для 8 бит, 0xFFFF для 16 бит
"""
