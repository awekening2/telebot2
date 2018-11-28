import psycopg2

class TelegramDataBase:

    def __init__(self):
        self.host = "ec2-54-247-119-167.eu-west-1.compute.amazonaws.com"
        self.dbname = "d7to7lm591k63g"
        self.dbuser = "jxkqaclpjpmzez"
        self.dbpass = "8dbde4ebb9ce7e6720455d0ad19fb6c949d5ba8c2de36b44b50558c834301085"
        self.connect()

    def connect(self):
        print( "Подключаюсь к БД" )
        try:
            self.connection = psycopg2.connect( host = self.host,  dbname=self.dbname, user=self.dbuser, password=self.dbpass)
            self.cursor = self.connection.cursor()
            print("Подключение к БД установлено")
        except:
            print("Ошибка подключения к БД")


    def disconnect(self):
        print("Отключаюсь от БД")
        self.cursor.close()
        self.connection.close()

    def getUserID(self, chat_id):
        self.cursor.execute(f"SELECT id FROM public.user WHERE chat_id = {chat_id};")
        return self.cursor.fetchone()

    def userIsExist(self, chat_id, name):
        # если пользователя нет, то добавить его в БД и пусть там живет
        res = self.getUserID( chat_id )
        if not res:
            print("create")
            salary = 50000
            self.cursor.execute(f"INSERT INTO public.user (chat_id, first_name, salary) VALUES ({chat_id}, '{name}', {salary});")
            self.connection.commit()
            return 1
        return 0

    def getCommandList(self):
        #получить список команд
        self.cursor.execute(f"SELECT name, description FROM commands;")
        return self.cursor.fetchall()

    def getCategoryList(self):
        # получить список категорий
        self.cursor.execute(f"SELECT name FROM sections;")
        return self.cursor.fetchall()

    def getIDCategory(self, category_name):
        self.cursor.execute(f"SELECT id FROM sections WHERE sections.name = '{category_name}'")
        result = self.cursor.fetchone()
        if result is None:
            return 0
        return result

    def getProduct(self, product_name):
        self.cursor.execute( f"SELECT product.name, product.desription, product.price from product where name = '{product_name}';")
        return self.cursor.fetchone()

    def getProductListInCategory(self, category_id):
        # получить список продуктов в категории
        self.cursor.execute(f"SELECT product.name, product.price from product, sections where sections.id = {category_id} and product.sections_id = sections.id")
        return self.cursor.fetchall()

    def addToBasket(self, chat_id, product, count):
        self.cursor.execute(f"SELECT addtobasket({chat_id}, '{product}', {count});")
        self.connection.commit()

    def viewBasket(self, chat_id):
        self.cursor.execute(f"select * from viewbasket({chat_id});")
        return self.cursor.fetchall()

    def deleteBasket(self, chat_id):
        id = self.getUserID(chat_id)
        self.cursor.execute(f"delete from basket where user_id = {id[0]};")

    def checkout(self, chat_id):
        self.cursor.execute(f"select * from checkout({chat_id});")
        self.connection.commit()
        return self.cursor.fetchone()[0]


