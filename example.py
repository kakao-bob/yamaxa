from yamaxa import *


bot = MaxBot("my-super-secret-token-from-platform") # сюда токен


@bot.on_update()
async def handle_event(update: Update):
    """Реагирует на каждый апдейт"""
    print(f"New event: {update}")


@bot.on_message()
async def handle_msg(umsg: UMessage):
    """Реагирует на сообщение"""
    msg = umsg.message
    txt = msg.body.text

    if txt == '/start':
        btns = [
            [
                Button(type="callback", text="КНОПКА 1️⃣", payload="button1"), 
                Button(type="callback", text="КНОПКА 2️⃣", payload="button2")
            ]
        ]
        att1 = Attachment(type="inline_keyboard", payload={"buttons": btns})
        await bot.send_message(chat_id=msg.recipient.chat_id, 
                               text=f"ℹ️ Добро пожаловать! Inline-клавиатура:", attachments=[att1])

    else:
        await bot.send_message(chat_id=msg.recipient.chat_id, text=f"Вы написали: '{txt}'!")


@bot.on_callback()
async def handle_cback(ucb: UCallback):
    """Реагирует на callback-и от кнопок"""
    payload = ucb.callback.payload # payload кнопки
    user = ucb.callback.user # пользователь, что нажал кнопку

    await bot.send_message(user_id=user.user_id, text=f"Нажата кнопка: {payload}")
    

def start():
    try:
        asyncio.run(bot.start_polling())
    except KeyboardInterrupt:
        print("\nCTRL+C, stopping..")

if __name__ == "__main__":
    start()