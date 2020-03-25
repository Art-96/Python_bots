import telebot
from TelegramBot import const
from telebot import types
from geopy.distance import vincenty


bot = telebot.TeleBot(const.TOKEN)

markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn_adress = types.KeyboardButton('Adress button', request_location=True)
btn_payment = types.KeyboardButton('Payment Methods')
btn_delivery = types.KeyboardButton('Delivery Methods')
markup_menu.add(btn_adress, btn_payment, btn_delivery)

markup_inline_payment = types.InlineKeyboardMarkup()
btn_in_cash = types.InlineKeyboardButton('Cash payment', callback_data='cash')
btn_in_card = types.InlineKeyboardButton('Card payment', callback_data='card')
btn_in_invoice = types.InlineKeyboardButton('Bank transfer', callback_data='invoice')

markup_inline_payment.add(btn_in_card, btn_in_cash, btn_in_invoice)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello, I'm a shop bot", reply_markup=markup_menu)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print(message)
    if message.text=='Delivery Methods':
        bot.reply_to(message, 'Courier delivery', reply_markup=markup_menu)
    elif message.text=='Payment Methods':
        bot.reply_to(message, 'The following payment methods are available', reply_markup=markup_inline_payment)
    else:
        bot.reply_to(message, message.text,  reply_markup=markup_menu)

@bot.message_handler(func=lambda message:True, content_types = ['location'])
def location(message):
    print(message)
    lon = message.location.longitude
    lat = message.location.latitude

    distance = []
    for i in const.Magazins:
        result = vincenty((i['latitude'], i['longitude']), (lat, lon)).kilometers
        distance.append((min(distance)))
    index = distance.index(min(distance))

    bot.send_message(message.chat.id, 'Store nearest you')
    bot.send_venue(message.chat.id, const.Magazins[index]['latitude'], const.Magazins[index]['longitude'],
                   const.Magazins[index]['title'], const.Magazins[index]['address'])

@bot.callback_query_handler(func=lambda call:True)
def call_back_payment(call):
    print(call)
    if call.data == 'cash':
        bot.send_message(call.message.chat.id, text='Pay at the checkout.', reply_markup=markup_inline_payment)

bot.polling()