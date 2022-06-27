import telebot
from extensions import CryptoConverter, APIException
from config import keys, TOKEN


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Привет!\nЧтобы начать работу введите названия валюты (через пробел): \
\n<валюта которую будем переводить> \
\n<в какую валюту перевести> \
\n<количество валюты> \
\nЧтобы увидеть список доступных валют, нужно ввести "/values"'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) > 3:
            raise APIException('Слишком много параметров')
        if len(values) < 3:
            raise APIException('Недостаточно параметров')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    else:
        text = f'Цена {amount} {quote} в {base} = {float(total_base)*float(amount)}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)