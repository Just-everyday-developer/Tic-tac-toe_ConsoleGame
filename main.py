import keyboard
import numpy as np
from threading import Thread
import queue

field = np.array([
    [' 1 ', ' 2 ', ' 3 '],
    [' 4 ', ' 5 ', ' 6 '],
    [' 7 ', ' 8 ', ' 9 ']
])

exit_flag = False
input_queue = queue.Queue()

class Player:
    def __init__(self, symbol, order):
        self.symbol: str = symbol
        self.order = order

    def is_valid_place(self):
        global exit_flag
        while not exit_flag:
            try:
                number = input_queue.get(timeout=0.1)
                if number == 'q':
                    exit_flag = True
                    break
                elif number.strip().isdigit():
                    number = int(number)
                    if 1 <= number <= 9 and field[(number-1) // 3][number % 3 - 1] not in [' x ', ' o ']:
                        field[(number - 1) // 3][number % 3 - 1] = self.symbol
                        show_field()
                        break
                    elif number not in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                        print("Неправильная ячейка ")
                    elif field[(number-1) // 3][number % 3 - 1] in [' x ', ' o ']:
                        print("Ошибка! Уже установлен символ ")
                else:
                    print("Неправильный ввод! Введите еще раз число: ")
            except queue.Empty:
                continue

    def __print_message(self):
        global exit_flag
        print(f"Победитель: Игрок {self.order}!")
        exit_flag = True
        return True

    def check_victory(self):
        for row in field:
            if np.all(row == self.symbol):
                return self.__print_message()

        for column in field.transpose():
            if np.all(column == self.symbol):
                return self.__print_message()

        if np.all(np.diag(field) == self.symbol):
            return self.__print_message()

        if np.all(np.diag(np.fliplr(field)) == self.symbol):
            return self.__print_message()


def show_field(field=field):
    for i in field:
        print(i)


def check_draw():
    for array in field:
        for element in array:
            if element.strip().isdigit():
                return False
    print("Ничья!")
    global exit_flag
    exit_flag = True
    return True


def show_start_message():
    print()
    show_field()
    print("Игрок 1 - x, Игрок 2 - o")
    print("'q' - выход из игры")
    print()


def monitor_exit():
    global exit_flag

    while not exit_flag:
        if keyboard.is_pressed('q'):
            input_queue.put('q')
            print("\nВыход из программы...")
            exit_flag = True
            break


def get_user_input():
    while not exit_flag:
        user_input = input()
        input_queue.put(user_input)


def main():
    global exit_flag
    player1 = Player(' x ', 1)
    player2 = Player(' o ', 2)

    try:
        while not exit_flag:
            if check_draw():
                break
            print("Выберите поле: ")
            player1.is_valid_place()
            if exit_flag or player1.check_victory():
                break
            if check_draw():
                break
            print("Выберите поле: ")
            player2.is_valid_place()
            if exit_flag or player2.check_victory():
                break
    except KeyboardInterrupt:
        pass
    except IndexError:
        print("Неверно введенное число!")


if __name__ == "__main__":
    exit_flag = False
    show_start_message()

    thread1 = Thread(target=monitor_exit)
    thread2 = Thread(target=get_user_input)
    thread1.start()
    thread2.start()

    main()

    thread1.join()
    thread2.join()
