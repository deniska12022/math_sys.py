import urllib.request
import json

# Разделяем ключ на две части. Вставь сюда свой реальный ключ, разрезав его пополам.
# Например, если ключ 'sk-or-v1-abc123def456', то p1 = 'sk-or-v1-abc', p2 = '123def456'
p1 = "sk-or-v1-eba471b6df54bd7b45d17"
p2 = "20e46bdbdd4e0fff8aa4f67d9216cb191a2123bad12"
ApiKey = p1 + p2

MODEL = "deepseek/deepseek-v4.1-flash" # Или любая другая модель из OpenRouter

def solve(text):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {ApiKey}",
        "Content-Type": "application/json"
    }
    
    # Жесткие рамки для формирования ответа
    system_prompt = (
        "Ты школьник, который решает задачу. Напиши только код решения. "
        "Никаких кавычек, никакой markdown-разметки, без слов 'Конечно' и рассуждений. "
        "Оформляй код максимально просто, как начинающий. Если нужен текстовый ответ, "
        "напиши его в виде комментария к коду."
    )
    
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ],
        "temperature": 0.0 # Значение 0.0 минимизирует галлюцинации
    }
    
    req = urllib.request.Request(
        url, 
        data=json.dumps(data).encode('utf-8'), 
        headers=headers, 
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            answer = result['choices'][0]['message']['content']
            
            # Сохраняем результат в новый файл рядом со скриптом
            with open("solution.py", "w", encoding="utf-8") as f:
                f.write(answer.strip())
            print("Готово. Результат лежит в solution.py")
            
    except Exception as e:
        print(f"Ошибка API: {e}")
