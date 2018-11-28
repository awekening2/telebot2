import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

class TelegramView:

    def __init__(self):

        self.TOKEN = "668194662:AAGhMG_LkFcWwjfssoRtBMzk08AHudTVDq4"
        self.PROXY = "http://94.242.58.108:1448"
        print("Подключаемся к telegram")
        try:
            telepot.api.set_proxy(self.PROXY)
            self.bot = telepot.Bot(self.TOKEN)
            print("Подключение к telegram установлено")
        except:
            print( "Подключение к telegram не установлено" )

    def loop(self):

        print("Слушаю telegram канал")
        try:
            MessageLoop(self.bot, { 'chat': self.listner, 'callback_query': self.on_callback_query }).run_as_thread()
            while 1:
                time.sleep(120)
        except:
            print( "Прервано" )

    def listner(self, msg):
        name = msg['chat']['first_name']
        chat_id = msg['chat']['id']
        command = msg['text'].split()
        self.presenter.getCommand( chat_id, name, command )

    def sendMessage(self, chat_id, msg):
        self.bot.sendMessage(chat_id, msg)

    def sendRequestResult(self, chat_id, msg):
        buf = ""
        for i in msg:
            for j in i:
                buf +=str(j)+self.tab
            buf+="\n"
        self.sendMessage(chat_id, buf)

    def showMenu(self, chat_id,msg):
        new_keyboard = []
        for item in msg:
            new_keyboard.append( [InlineKeyboardButton(text=item[1], callback_data=item[0])] )
        keyboard = InlineKeyboardMarkup( inline_keyboard = new_keyboard)
        self.bot.sendMessage(chat_id, 'Управление', reply_markup=keyboard)

    def showcategories(self, chat_id, msg):
        new_keyboard = []
        for item in msg:
            new_keyboard.append([InlineKeyboardButton(text=item[0], callback_data= "/categories "+ item[0])])
        keyboard = InlineKeyboardMarkup(inline_keyboard=new_keyboard)
        self.bot.sendMessage(chat_id, 'Категории', reply_markup=keyboard)

    def showincategory(self, chat_id, msg, cat_name):
        new_keyboard = []
        for item in msg:
            new_keyboard.append([InlineKeyboardButton(text=item[0].replace('_',' '), callback_data= "/product "+ item[0])])
        keyboard = InlineKeyboardMarkup(inline_keyboard=new_keyboard)
        self.bot.sendMessage(chat_id, cat_name, reply_markup=keyboard)

    def showproduct(self, chat_id, msg):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Добавить в корзину', callback_data='/add '+ msg[0])]
        ])
        self.bot.sendMessage(chat_id, f"""Название: {msg[0].replace('_',' ')}\nОписание: {msg[1]}\nЦена: { msg[2] }
        """, reply_markup=keyboard)

    def showpopup(self, query_id, msg):
        self.bot.answerCallbackQuery(query_id, text=msg)

    def showbasket(self, chat_id, msg):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Оформить', callback_data='/order')],
            [InlineKeyboardButton(text='Очистить', callback_data='/delete')]
        ])
        buf = ""
        for item in msg:
            buf += f"""Название: {item[0].replace('_',' ')}\t Кол-во: {item[1]} \t Цена: {item[2]}\n"""
        self.bot.sendMessage(chat_id, f"""Корзина\n{buf}""", reply_markup=keyboard)

    def on_callback_query(self, msg):
        query_id,chat_id, command = telepot.glance(msg, flavor='callback_query')
        self.presenter.pressButton( chat_id, command.split(), query_id )

    def setPresenter(self, presenter):
        self.presenter = presenter
