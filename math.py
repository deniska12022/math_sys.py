import urllib.request
import os

# 1. Получаем путь к папке, в которой лежит этот запускаемый скрипт
current_dir = os.path.dirname(os.path.abspath(__file__))
# 2. Склеиваем путь к папке с именем файла
save_path = os.path.join(current_dir, "deylice.py")

url = "https://raw.githubusercontent.com/deniska12022/math_sys.py/refs/heads/main/deylice.py"

# 3. Сохраняем скачанный файл по точному пути
urllib.request.urlretrieve(url, save_path)
print(f"Библиотека deylice успешно загружена в: {current_dir}")
