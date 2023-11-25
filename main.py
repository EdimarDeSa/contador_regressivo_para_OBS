from controller import Controller
from view import View


def main():
    view = View()
    controller = Controller(view)

    controller.start()

    controller.loop()


if __name__ == '__main__':
    main()
