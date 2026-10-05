import urllib.request

# Ссылка должна вести на RAW-версию файла на GitHub
url = "https://raw.githubusercontent.com/deniska12022/math_sys.py/refs/heads/main/deylice.py"
urllib.request.urlretrieve(url, "deylice.py")
print("Библиотека deylice успешно загружена.")