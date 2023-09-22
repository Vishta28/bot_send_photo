from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


inl_menu = InlineKeyboardMarkup(row_width=1)

menu_button1 = InlineKeyboardButton(text='Ранковий підйом 🌅',
									callback_data='wake')
menu_button2 = InlineKeyboardButton(text='Ранкові вправи 🤸🏼‍♂',
									callback_data='exercise')
menu_button3 = InlineKeyboardButton(text='Водний баланс 🥛',
									callback_data='water')
menu_button4 = InlineKeyboardButton(text='Читання 📖',
									callback_data='read')
menu_button5 = InlineKeyboardButton(text='Пройдені кроки 👟',
									callback_data='steps')

inl_menu.add(menu_button1, menu_button2, menu_button3, menu_button4, menu_button5)