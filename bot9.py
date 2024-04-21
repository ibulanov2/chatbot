import telebot
from googletrans import Translator
import gtts
import os

bot = telebot.TeleBot('5813560057:AAE_TsKhMYotGYiE4tK6NKhOe2JVPXe9YUU')

translator=Translator() #создаём переводчик
dest_lang='en' #устанавливаем язык

languages = { #словарь с языками
    'руский':'ru',
    'английский':'en',
    'французский':'fr',
    'итальянский': 'it',
    'испанский': 'es',
    'казахский': 'kk',
    'китайский': 'zh-CN',
    'корейский': 'ko',
    'латинский': 'la',
    'немецкий': 'de',
}

#функция перевода
def translateText(text):
    global dest_lang
    transed = translator.translate(text, dest=dest_lang) #переводим
    transed=transed.text #получаем переводввиде текста
    return transed

#функция озвучки
def voice(text):
    global dest_lang
    audiofile = text + '.mp3'
    voice = gtts.gTTS(text, lang=dest_lang,slow=True)  # делаем гс
    voice.save(audiofile)  # сохраняем гс
    return audiofile

#команда старт
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,'Привет, я бот-переводчик. '
                         'Напиши мне любое слово, и я переведу и расскажу как его правильно прочитать.\n'
                         'Для перевода используй команду /translate\n'
                         'А для смены языка /changelang')

#команда перевод
@bot.message_handler(commands=['translate'])
def translate(message):
    text=message.text
    text = text.replace('/translate', '').strip() #получаем текст из сообщения
    transed = translateText(text) #переводим
    bot.reply_to(message, transed) #отправляем перевод

    audiofile=voice(transed) #озвучиваем перевод
    f = open(audiofile, 'rb')  # открываем аудио с речью
    bot.send_voice(message.chat.id, f)  # отправляем сообщение
    f.close()  # закрываем файл
    os.remove(audiofile)  # удаляем файл гс (озвучки)

#команда смены языка
@bot.message_handler(commands=['changelang'])
def changelang(message):
    global dest_lang,languages
    language = message.text
    language = language.replace('/changelang', '').strip() #разделяем текст на команду и язык
    language=language.lower() #приводим текств нижний регистр
    dest_lang=languages[language]#получаем значение из словаря
    bot.send_message(message.chat.id,'Вы установили '+language+' язык')

#команда помощь
@bot.message_handler(commands=['help'])
def help(message):
    global languages,dest_lang
    msg="Я могу перевести любой текст на разные языки: \n"
    for key in languages.keys(): #перебираем все ключи из словаря и добавляем в сообщение
        msg+=key
        msg+='\n'
    msg+='Для смены языка введите команду /changelang Язык'
    bot.send_message(message.chat.id,msg)

    msg = "Сейчас установлен "
    for key, value in languages.items(): #перебираем все значения и находим ключ
        if dest_lang == value:
            msg+=key
    bot.send_message(message.chat.id, msg)


bot.polling(none_stop=True) #запускаем бота





