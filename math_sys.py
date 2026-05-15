import urllib.request, json, ssl, os

# Твой актуальный ключ
_K = "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"
_M = "deepseek/deepseek-v4-flash:free"

def solve(text):
    # Мгновенно чистим консоль при вызове функции
    os.system('cls' if os.name == 'nt' else 'clear')
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {_K}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost"
    }
    
    # Инструкция для ИИ: писать только простой код и ответ
    payload = {
        "model": _M,
        "messages": [
            {"role": "system", "content": "You are a school math engine. Write SIMPLE Python code using variables like a, b, k, n, s. At the end, write 'ANSWER:' followed by the result. No yapping."},
            {"role": "user", "content": text}
        ]
    }
    
    ctx = ssl._create_unverified_context()

    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=headers)
        with urllib.request.urlopen(req, context=ctx) as r:
            res = json.loads(r.read().decode())
            out = res['choices'][0]['message']['content']
            
            # Парсим код и финальное число
            if "```python" in out:
                code = out.split("```python")[1].split("```")[0].strip()
            elif "```" in out:
                code = out.split("```")[1].split("```")[0].strip()
            else:
                code = out
                
            ans = out.split("ANSWER:")[1].strip() if "ANSWER:" in out else "Error"
            
            # Сохраняем код в файл для "отмазки" перед учителем
            with open("solution.py", "w", encoding="utf-8") as f:
                f.write(code + f"\n\n# ОТВЕТ: {ans}")
            
            # Выводим в консоль только чистый результат
            print(f"\n[CORE] Result: {ans}")
            print(f"[INFO] Logic saved to solution.py")
    except:
        print("\n[!] Connection Error")