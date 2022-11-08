import logging
from aiogram import Bot,\
    Dispatcher,\
    executor,\
    types

import json
import datetime
import asyncio

f = open('cfg.txt', 'r', encoding='utf-8')
cfg = f.read()
f.close()
cfg = json.loads(cfg)

API_TOKEN = cfg['token']


adding = False
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

chat = -1001786478434
user = 667970295

inline_btn_1 = types.inline_keyboard.InlineKeyboardButton(cfg['names'][0], url=cfg['url'][0])
inline_btn_2 = types.inline_keyboard.InlineKeyboardButton(cfg['names'][1], url=cfg['url'][1])
inline_btn_3 = types.inline_keyboard.InlineKeyboardButton(cfg['names'][2], url=cfg['url'][2])
inline_btn_4 = types.inline_keyboard.InlineKeyboardButton('Я подписался', callback_data='done')

inline_kb1 = types.inline_keyboard.InlineKeyboardMarkup().add(inline_btn_1, inline_btn_2, inline_btn_3)
inline_kb1.add(inline_btn_4)




@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """

    await message.answer('Подпишись на 3 канала, чтобы получить доступ к 2.000 книг абсолютно бесплатно', reply_markup=inline_kb1)

@dp.message_handler(content_types=types.message.ContentType.DOCUMENT)
async def photo(message: types.Message):
    if globals()["adding"]:
        cfg['file_id'] = message.document.file_id
        f = open('cfg.txt', 'w', encoding='utf-8')
        f.write(json.dumps(cfg, indent=6, ensure_ascii=False))
        f.close()
        await message.answer('Файл сохранен')
        globals()["adding"] = False



@dp.message_handler()
async def echo(message: types.Message):
    print(message)
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    if message.text == 'hgiuei0esdepoawdoaw':

        globals()["adding"] = True
        await message.answer('Отправьте файл для сохранения')

@dp.callback_query_handler(lambda c: c.data == 'done')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    try:
        v = []
        for i in range(3):
            m = await bot.get_chat_member(cfg['channels_ids'][i], callback_query.from_user.id)
            v.append(m['status'] != 'left')
        if v[0] and v[1] and v[2]:
            await bot.send_document(callback_query.from_user.id, cfg['file_id'])
        else:
            await bot.send_message(callback_query.from_user.id, 'Вы не подписаны, попробуйте еще раз')
    except:
        await bot.send_message(callback_query.from_user.id, 'Вы не подписаны, попробуйте еще раз')


if __name__ == '__main__':
    executor.start_polling(dp)
