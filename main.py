import telebot
from config import keys, TOKEN
from extensions import APIException, Convertor
import traceback

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help (message: telebot.types.Message):
    text = 'Приветствую! \nЧтобы увидеть список доступных валют, введите команду боту: /values.'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Для начала работы введите команду в следующем формате: \n <имя валюты>\
 <в какую валюту перевести> \
 <количество переводимой валюты>.\n\nДоступные валюты:'
    for i in keys.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Неверное количество параметров.')

        quote, base, amount = values
        total_base = Convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f'Не удалось обработать команду:\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} : {total_base}'
        bot.reply_to(message, text)


bot.polling()
