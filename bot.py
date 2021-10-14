import telebot
from telebot import types
from config import token

bot = telebot.TeleBot(token)
# данные пользователя лучше хранить в бд
user_data = []  # данные пользователя в формате [name, surname, age]


@bot.message_handler(content_types=['text'])
def start(message):
    """обработчик текстовых сообщений"""
    if message.text == "/reg":
        user_data.clear()  # на случай, если пользователь уже регистрировался
        bot.send_message(message.from_user.id, "Как тебя зовут?")
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.from_user.id, "Напиши /reg")


def get_name(message):
    """получение имени пользователя"""
    user_data.append(message.text)
    bot.send_message(message.from_user.id, "Какая у тебя фамилия?")
    bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    """получение фамилии пользователя"""
    user_data.append(message.text)
    bot.send_message(message.from_user.id, "Сколько тебе лет?")
    bot.register_next_step_handler(message, get_age)


def get_age(message):
    """получение возраста пользователя"""
    if not message.text.isdigit():
        bot.send_message(message.from_user.id, "Цифрами, пожалуйста")
        bot.register_next_step_handler(message, get_age)
        return
    user_data.append(int(message.text))
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text="Да", callback_data="yes")
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text="Нет", callback_data="no")
    keyboard.add(key_no)
    question = f"Тебе {str(user_data[2])} лет, тебя зовут {user_data[0]} {user_data[1]}?"
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    """обработчик клавиатуры"""
    if call.data == "yes":
        bot.send_message(call.message.chat.id, "Запомню : )")
    elif call.data == "no":
        bot.send_message(call.message.chat.id, "Напиши /reg")


bot.polling(none_stop=True, interval=0)  # запрос апдейтов у сервера
