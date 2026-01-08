# demo.py
from led_strip_driver import LEDStripDriver
import time

def show_menu():
    print("\n" + "="*40)
    print("Управление RGB светодиодом")
    print("="*40)
    print("1. Установить цвет (RGB)")
    print("2. Установить цвет (HEX)")
    print("3. Демонстрация цветов")
    print("4. Эффект дыхания")
    print("5. Радуга")
    print("6. Полицейские мигалки")
    print("7. Изменить яркость")
    print("8. Выключить")
    print("9. Выход")
    print("="*40)

def main():
    led = LEDStripDriver()
    
    while True:
        show_menu()
        choice = input("Выберите действие (1-9): ").strip()
        
        if choice == "1":
            try:
                r = int(input("Красный (0-255): "))
                g = int(input("Зеленый (0-255): "))
                b = int(input("Синий (0-255): "))
                led.set_color(r, g, b)
                print(f"Цвет установлен: RGB({r}, {g}, {b})")
            except ValueError:
                print("Ошибка: введите числа от 0 до 255")
        
        elif choice == "2":
            hex_color = input("Введите HEX цвет (например, #FF00FF): ")
            led.set_color_hex(hex_color)
            print(f"Цвет установлен: {hex_color}")
        
        elif choice == "3":
            delay = float(input("Задержка между цветами (сек): "))
            led.demo_sequence(delay)
        
        elif choice == "4":
            try:
                r = int(input("Красный (0-255): "))
                g = int(input("Зеленый (0-255): "))
                b = int(input("Синий (0-255): "))
                cycles = int(input("Количество циклов: "))
                led.breathing_effect(r, g, b, cycles=cycles, duration=2.0)
            except ValueError:
                print("Ошибка ввода")
        
        elif choice == "5":
            cycles = int(input("Количество циклов радуги: "))
            led.rainbow(cycles=cycles, speed=0.03)
        
        elif choice == "6":
            duration = float(input("Длительность (сек): "))
            led.police_lights(duration=duration, speed=0.1)
        
        elif choice == "7":
            try:
                brightness = float(input("Яркость (0.0 - 1.0): "))
                led.set_brightness(brightness)
            except ValueError:
                print("Ошибка: введите число от 0.0 до 1.0")
        
        elif choice == "8":
            led.clear()
            print("Светодиод выключен")
        
        elif choice == "9":
            print("Выход из программы...")
            break
        
        else:
            print("Неверный выбор. Попробуйте еще раз.")
        
        time.sleep(0.5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрограмма завершена пользователем")
