from typing import Any, Optional
from pydantic import BaseModel, Field, warnings, ConfigDict

class User(BaseModel):
    """MAX user"""

    user_id: int
    first_name: str
    username: Optional[str] = None
    is_bot: bool  # is user a bot?
    last_name: Optional[str] = None
    last_activity_time: Optional[int] = None
    name: Optional[str] = Field(
        default=None,
        json_schema_extra={"deprecated": True},  # deprecated в API
    )


class Update(BaseModel):
    """Update from chat. This can be new message,
    a user joined a group, button clicked or etc."""
    update_type: str
    timestamp: int


class Recipient(BaseModel):
    """Message recipient (получатель сообщения)"""

    chat_type: str
    chat_id: Optional[int] = None
    user_id: Optional[int] = None

class Button(BaseModel):
    """Inline keyboard button"""
    # Разрешаем принимать лишние поля
    model_config = ConfigDict(extra='allow')

    type: str # [callback|message|..]
    text: str 

class Keyboard(BaseModel):
    """inline-keyboard"""
    buttons: list[Button]

class Attachment(BaseModel):
    # Разрешаем принимать лишние поля
    model_config = ConfigDict(extra='allow')

    type: str
    payload: Any

class MessageBody(BaseModel):
    """body of message"""
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
    """Message in chat (сообщение в чате)"""

    recipient: Recipient
    timestamp: int
    body: MessageBody
    sender: Optional[User] = None
    link: Optional[LinkedMessage] = None
    stat: Optional[Any] = None  # Статистика сообщения.
    url: Optional[str] = None  # Публичная ссылка на пост в канале.


class UMessage(Update):
    """Update (new message)"""
    message: Message
    user_locale: Optional[str] = None

class Callback(BaseModel):
    """Callback from button"""
    timestamp: int
    callback_id: str
    payload: Optional[str] = None
    user: User # пользователь, нажавший кнопку

class UCallback(Update):
    """Update (new button callback)"""
    callback: Callback

if __name__ == "__main__":
    print("hello world")