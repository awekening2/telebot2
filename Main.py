from TelegramView import TelegramView
from TelegramDataBase import TelegramDataBase
from TelegramPresenter import TelegramPresenter

def main():
    view = TelegramView()
    model = TelegramDataBase()
    presenter = TelegramPresenter(model, view)

    view.setPresenter(presenter)
    view.loop()

    model.disconnect()

if __name__ == "__main__":
    main()