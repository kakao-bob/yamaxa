import asyncio
import httpx
from datetime import datetime, timezone
import os
import ssl
from .misc import *
from .crtmngr import *


class MaxBot:
    def __init__(self, token: str, auto_download_cert=False, cert_download_url="default", log=False):
        self.api_url = "https://platform-api2.max.ru/updates"
        self.token = token
        self.marker = None
        self.log = log

        # handlers
        self._H_Update = []
        self._H_Message = []
        self._H_Callback = []

        self.ssl_context = get_ssl_context(auto_download_cert, cert_download_url)

    # Декораторы для регистрации функций-обработчиков (как @dp.message в aiogram)
    def on_update(self):
        def decorator(func):
            self._H_Update.append(func)
            return func
        return decorator
    def on_message(self):
        def decorator(func):
            self._H_Message.append(func)
            return func
        return decorator
    def on_callback(self):
        def decorator(func):
            self._H_Callback.append(func)
            return func
        return decorator
    
    async def send_message(self, text: str, attachments: list[Attachment] = [], user_id: int = None, chat_id: int = None):
        """Отправить сообщение"""
        headers = {
            "Authorization": self.token,
        }
        params = {"user_id": user_id} if user_id else {"chat_id": chat_id}
        
        atts = []
        for attachment in attachments:
            atts.append( attachment.model_dump() )

        # Тело запроса (JSON-данные)
        json_data = {
            "text": text,
            "attachments": atts,
            "link": None
        }

        if self.log: print(f"Sending with data: {json_data}")

        # 2. Используем контекстный менеджер для управления сессией
        async with httpx.AsyncClient(verify=self.ssl_context) as client:
            response = await client.post(
                "https://platform-api2.max.ru/messages", 
                headers=headers, 
                params=params, 
                json=json_data
            )
            
            # 3. Обрабатываем ответ
            if self.log: print("Статус-код:", response.status_code)
            if self.log: print("Ответ сервера (JSON):", response.json())

    # Главный асинхронный цикл Long Polling
    async def start_polling(self, timeout: int = 30):
        print("[yamaxa] Bot started...")
        
        # Используем один клиент для удержания HTTP-сессии
        async with httpx.AsyncClient(verify=self.ssl_context) as client:
            while True:
                try:
                    # Формируем параметры запроса
                    params = {
                        "timeout": timeout
                        }
                    if self.marker:
                        params["marker"] = self.marker
                    
                    headers = {
                        "Authorization": self.token
                    }

                    # Отправляем Long Polling запрос
                    response = await client.get(self.api_url, params=params, headers=headers, timeout=timeout + 5)
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Обновляем маркер для следующего шага
                        self.marker = data.get("marker")
                        updates = data.get("updates", [])

                        
                        for update in updates:
                            # обработка default-хэндлера
                            for handler in self._H_Update:
                                asyncio.create_task(handler(update))

                            # --- особые события ---

                            # on_message
                            if update.get("update_type") == "message_created":
                                payload = UMessage.model_validate(update)
                                for handler in self._H_Message:
                                    asyncio.create_task(handler(payload))

                            # on_callback
                            elif update.get("update_type") == "message_callback":
                                payload = UCallback.model_validate(update)
                                for handler in self._H_Callback:
                                    asyncio.create_task(handler(payload))
                                
                    else:
                        print(f"Server error: {response.status_code}")
                        try:
                            print(f"├ Server says: {response.text}")
                        except:
                            print("Failed to fetch text")
                        print("└ Retrying in 5 secs...")
                        await asyncio.sleep(5)

                except httpx.RequestError as e:
                    print(f"Network error: {e}. Retrying in 5 secs...")
                    await asyncio.sleep(5)
