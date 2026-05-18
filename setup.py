import urllib.request as r
import os
import sys
import ssl
import site 

URL = "https://raw.githubusercontent.com/deniska12022/math_sys.py/refs/heads/main/math_sys.py"

def inject():
    ctx = ssl._create_unverified_context()
    
    target_dir = site.getusersitepackages()
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)
        
    target = os.path.join(target_dir, 'math_sys.py')
    
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
# ШПАРГАЛКА:
# ====================================================
# import math_sys as ms
# ms.solve(""" ЗАДАЧА """)
