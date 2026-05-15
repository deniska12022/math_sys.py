import urllib.request as r
import os
import sys
import ssl

URL = "https://raw.githubusercontent.com/deniska12022/math_sys.py/refs/heads/main/math_sys.py"

def inject():
    ctx = ssl._create_unverified_context()
    target = os.path.join(sys.prefix, 'Lib', 'math_sys.py')
    
    try:
        print("[...] Загрузка системных компонентов...")
        with r.urlopen(URL, context=ctx) as response:
            with open(target, 'wb') as f:
                f.write(response.read())
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print("----------------------------------------")
        print("  SYSTEM READY. DELETE THIS SCRIPT.  ")
        print("----------------------------------------")
    except Exception as e:
        print(f"\n[!] Ошибка: {e}")

if __name__ == "__main__":
    inject()

# ====================================================
# ШПАРГАЛКА (КАК ИСПОЛЬЗОВАТЬ НА ЭКЗАМЕНЕ):
# ====================================================
# 1. Запустил этот скрипт один раз (F5).
# 2. Увидел SYSTEM READY — стирай всё из этого файла.
#
# 3. Когда видишь задачу, пиши это:
#
# import math_sys as ms
#
# ms.solve("""
# Сюда вставляешь текст задачи целиком.
# Можно с переносами строк, кавычки стерпят всё.
# """)
#
# 4. Жмешь F5. 
# В консоли будет только цифра ответа.
# Рядом появится файл solution.py с кодом решения 
# (на случай, если препод попросит показать, как решал).
# ====================================================
