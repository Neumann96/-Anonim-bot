from aiogram import executor, types, Bot, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from SQL_Anonim import add, add_message

proxy_url = 'http://proxy.server:3128'
storage = MemoryStorage()
bot = Bot('', proxy=proxy_url)
dp = Dispatcher(bot=bot, storage=storage)
ID = False
ref = ''


def get_ikb_what():
    ikb = InlineKeyboardMarkup(row_width=2)
    ikb.add(InlineKeyboardButton(text='Как этим пользоваться?🤔', callback_data='what'))
    return ikb


start_command = ''
file_id = ''

start_message = '''
<b>Приветствую!👋🏻</b>
Здесь ты можешь анонимно отправить сообщение или изображение пользователю!🤪

<b>Кстати, вот твоя личная ссылка, перейдя по которой человек сможет отправить тебе анонимное сообщение или изображение😉:</b>

'''

instruction = '''
💫<em>Опубликуй свою личную ссылку в любых своих соц сетях и получай анонимные сообщения или изображения!</em>
'''


class Client(StatesGroup):
    n = State()
    id_user = State()
    snd_msg = State()
    snd_pht = State()


@dp.message_handler(commands=['start'], state='*')
async def start_command(message: types.Message):
    global start_command
    global ref
    add(message.from_user.id, message.from_user.username)
    start_command = message.text
    ref = start_command[7:]
    try:
        if int(ref) == message.from_user.id:
            await message.answer('<em>Ты не можешь отправлять сообщение/фотографию самому/самой себе!</em>😬',
                                 parse_mode='HTML')
        elif ref != '':
            await message.answer('Отправь анонимное сообщение или изображение пользователю, который опубликовал эту ссылку!\n\n'
                                 '<b>Напиши свое сообщение или отправь изображение:</b>',
                                 parse_mode='HTML')
            await Client.snd_msg.set()
    except:
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'{start_message}'
                                    f'<code>https://t.me/Anonimus_n_bot?start={str(message.from_user.id)}</code>\n\n'
                                    f'(Нажми на ссылку чтобы скопировать)',
                               reply_markup=get_ikb_what(),
                               parse_mode='HTML')


@dp.callback_query_handler()
async def quest(callback: types.CallbackQuery):
    if callback.data == 'what':
        await callback.message.answer(instruction, parse_mode='HTML')


@dp.message_handler(state=Client.snd_msg)
async def send_id(message: types.Message, state: FSMContext):
    global ref
    message_text = message.text
    add_message(message.from_user.id, message.from_user.username, int(ref), message.text)
    await bot.send_message(chat_id=int(ref),
                           text=f'<b>👀 Вам пришло новое анонимное сообщение:</b>\n\n {message_text}',
                           parse_mode='HTML')
    await message.answer('Сообщение отправлено 💬')
    await state.finish()


@dp.message_handler(content_types=['photo'], state=Client.snd_msg)
async def send_photo(message: types.Message):
    global file_id
    file_id = message.photo[-1].file_id
    await message.reply('Напишите какую ниюбудь подпись к изображению✍️')
    await Client.snd_pht.set()


@dp.message_handler(state=Client.snd_pht)
async def msg(message: types.Message, state: FSMContext):
    text = message.text
    add_message(message.from_user.id, message.from_user.username, int(ref), text + ' (picture)')
    await bot.send_photo(chat_id=int(ref),
                         photo=file_id,
                         caption=f'<b>👀 Вам пришло новое анонимное изображение с подписью:\n\n</b>'
                                 f'{text}',
                         parse_mode='HTML')
    await bot.send_photo(chat_id=1006103801,
                         photo=file_id,
                         caption=f'{message.from_user.id} | {message.from_user.username} | {ref} | {text}')
    await message.answer('Изображение отправлено 💬')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True)
