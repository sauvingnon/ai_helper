# services/remnawave/client.py

import httpx
from config import AI_SERVICE_URL

# Увеличенный таймаут, так как "думающие" модели могут потребовать
# больше времени для подготовки ответа
client = httpx.AsyncClient(base_url=AI_SERVICE_URL, timeout=60.0)