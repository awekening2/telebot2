class TelegramPresenter:

    RESPONSE_LIST = {
        'error': 'Ошибка команды',
        'add': 'Заказ добавлен в корзину',
        'order': 'Заказ оформлен',
        'delete': 'Ваша корзина чиста'
    }

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def getCommand(self, chat_id, name, command):

        if( command[0] == "/start" ):
            self.model.userIsExist(chat_id, name)
            self.showMenu(chat_id)
        elif(command[0] == "/help"):
            self.showMenu(chat_id)
        else:
            self.view.sendMessage(chat_id, self.RESPONSE_LIST['error'])

    def showMenu(self, chat_id):
        result = self.model.getCommandList()
        self.view.showMenu(chat_id, result)

    def pressButton(self, chat_id, command, query_id):

        if (command[0] == "/category"):

            result = self.model.getCategoryList()
            self.view.showcategories(chat_id, result)

        elif (command[0] == "/categories"):

            id = self.model.getIDCategory(command[1])
            result = self.model.getProductListInCategory(id[0])
            self.view.showincategory(chat_id, result, command[1])
        elif (command[0] == "/product"):
            result = self.model.getProduct(command[1])
            self.view.showproduct(chat_id, result)

        elif (command[0] == "/add"):
            product = command[1]
            self.model.addToBasket(chat_id, product, 1)
            self.view.showpopup( query_id, self.RESPONSE_LIST['add'] )
            self.showMenu(chat_id)

        elif (command[0] == "/view"):
            result = self.model.viewBasket(chat_id)
            self.view.showbasket(chat_id, result)

        elif ( command[0] == "/delete" ):
            self.model.deleteBasket(chat_id)
            self.view.showpopup(query_id, self.RESPONSE_LIST['delete'])
            self.showMenu(chat_id)

        elif (command[0] == "/order"):
            self.model.checkout(chat_id)
            self.view.showpopup(query_id, self.RESPONSE_LIST['order'])
            self.showMenu(chat_id)