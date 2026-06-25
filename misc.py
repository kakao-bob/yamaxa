from typing import Any, Optional
from pydantic import BaseModel, Field, warnings, ConfigDict

class User(BaseModel):
    """Пользователь"""

    user_id: int
    first_name: str
    username: Optional[str] = None
    is_bot: bool  # Исправлено: теперь это правильная аннотация типа
    last_name: Optional[str] = None
    last_activity_time: Optional[int] = None
    name: Optional[str] = Field(
        default=None,
        json_schema_extra={"deprecated": True},  # Помечает поле как deprecated в схеме API
    )


class Update(BaseModel):
    update_type: str
    timestamp: int


class Recipient(BaseModel):
    """Получатель сообщения"""

    chat_type: str
    chat_id: Optional[int] = None
    user_id: Optional[int] = None

class Button(BaseModel):
    # Разрешаем принимать лишние поля
    model_config = ConfigDict(extra='allow')

    type: str # [callback|message|..]
    text: str 

class Keyboard(BaseModel):
    """inline-клавиатура"""
    buttons: list[Button]

class Attachment(BaseModel):
    # Разрешаем принимать лишние поля
    model_config = ConfigDict(extra='allow')

    type: str
    payload: Any

class MessageBody(BaseModel):
    mid: str  # Уникальный ID сообщения
    seq: int  # ID последовательности сообщения в чате
    text: Optional[str] = None
    attachments: Optional[Attachment] = None
    markup: Optional[Any] = None


class LinkedMessage(BaseModel):
    type: str
    message: MessageBody
    sender: Optional[User] = None
    chat_id: Optional[int] = None


class Message(BaseModel):
    """Сообщение в чате"""

    recipient: Recipient
    timestamp: int
    body: MessageBody
    sender: Optional[User] = None
    link: Optional[LinkedMessage] = None
    stat: Optional[Any] = None  # Статистика сообщения.
    url: Optional[str] = None  # Публичная ссылка на пост в канале.


class UMessage(Update):
    message: Message
    user_locale: Optional[str] = None

class Callback(BaseModel):
    timestamp: int
    callback_id: str
    payload: Optional[str] = None
    user: User # пользователь, нажавший кнопку

class UCallback(Update):
    callback: Callback

if __name__ == "__main__":
    print("hello world")