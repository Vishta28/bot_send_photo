from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # оперативна пам'ять
from aiogram import executor
from aiogram.dispatcher.filters.state import StatesGroup, State  # стан
from data_managment import create_table
from buttons import inl_menu
import requests
import os
import shutil
from aiogram.dispatcher import FSMContext
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import io
from photo_transfer import photo_transfer

# gauth = GoogleAuth()
# gauth.LocalWebserverAuth()
# gauth.LoadClientConfigFile('/app/.heroku/python/lib/python3.11/site-packages/pydrive/client_secrets.json')
#
# drive = GoogleDrive(gauth)

# Створити об'єкт GoogleAuth
gauth = GoogleAuth()

# Задати конфігурацію вручну
gauth.settings['client_id'] = '875334599397-cp256v0rqkprmob216ql0evonioip4or.apps.googleusercontent.com'
gauth.settings['client_secret'] = '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'
gauth.settings['redirect_uri'] = 'urn:ietf:wg:oauth:2.0:oob'

# Аутентифікація
gauth.CommandLineAuth()

# Створити об'єкт GoogleDrive з аутентифікацією
drive = GoogleDrive(gauth)







print('login saccc')

BOT_TOKEN = '5675794527:AAHSjUvT1UQOxRFJYRiok4eBa4m6h3v-Fqo'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

callback_data = {}

class States(StatesGroup):
	photo_send = State()


@dp.message_handler(commands=['start'], state='*')
async def process_start_command(message: types.Message):
	await bot.send_message(message.chat.id, 'Прогрес вашого проходження марафону:', reply_markup=inl_menu)
	await bot.send_message(message.chat.id, 'Вітаю! Оберіть пункт котрий ви виконали ⬆')

@dp.message_handler(content_types=['photo'], state=States.photo_send)
async def get_photo(message: types.Message, state: FSMContext):

	create_table(message.from_user.id)

	user_id = message.from_user.id
	data = callback_data.get(user_id, {})  # порожній словник {} за замовчуванням.
	topic = data.get('topic', 'невідомо')  # "невідомо" стоїть напевно на випадок помилки

	local_file_path = f'https://drive.google.com//drive//folders//maraphon//{str(user_id)}//{topic}//'

	photo_folder = photo_transfer(user_id, topic, drive)

	photo = message.photo[-1]  # Отримайте останню фотографію з повідомлення
	file_info = await bot.get_file(photo.file_id)

	# Отримайте URL-адресу файлу фотографії на сервері Telegram
	file_url = file_info.file_path
	response = requests.get(f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_url}')
	print(photo_folder)

	file1 = drive.CreateFile({'title': f'{message.photo[0].file_id}' + '.png',
							  'parents': [{'id': photo_folder}]})  # Create GoogleDriveFile instance with title 'Hello.txt'.
	file1.content = io.BytesIO(response.content)  # Set content of the file from given string.
	file1.Upload()

	await bot.send_message(message.chat.id, 'фото отримав')
	await state.finish()

@dp.callback_query_handler(text=['wake', 'exercise', 'water', 'read', 'steps'])
async def callback_retarget(call: types.CallbackQuery):
	if call.data == 'wake':
		callback_data[call.from_user.id] = {'topic': 'підйом'}
		await call.message.answer('Відправте фото виконаного завдання')
		await States.photo_send.set()
	if call.data == 'exercise':
		callback_data[call.from_user.id] = {'topic': 'ранкові вправи'}
		await call.message.answer('Відправте фото виконаного завдання')
		await States.photo_send.set()
	if call.data == 'water':
		await call.message.answer('Відправте фото виконаного завдання')
	if call.data == 'read':
		await call.message.answer('Відправте фото виконаного завдання')
	if call.data == 'steps':
		await call.message.answer('Відправте фото виконаного завдання')


if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True)