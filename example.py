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

    await bot.send_message(chat_id=msg.sender.user_id, text=f"Вы написали: '{txt}'!")


@bot.on_callback()
async def handle_cback(ucb: UCallback):
    """Реагирует на callback-и от кнопок"""
    payload = ucb.callback.payload # payload кнопки
    user = ucb.callback.user # пользователь, что нажал кнопку

    await bot.send_message(chat_id=user.user_id, text=f"Нажата кнопка: {payload}")
    

def start():
    try:
        asyncio.run(bot.start_polling())
    except KeyboardInterrupt:
        print("\nCTRL+C, stopping..")

if __name__ == "__main__":
    start()