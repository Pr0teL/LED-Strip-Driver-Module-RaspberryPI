# led_strip_driver.py
import RPi.GPIO as GPIO
import time
import atexit
import math

class LEDStripDriver:
    """
    Драйвер для управления RGB лентой на чипе P9813
    
    Args:
        din_pin (int): GPIO пин для данных (DIN) (по умолчанию: 23)
        cin_pin (int): GPIO пин для тактового сигнала (CIN) (по умолчанию: 24)
        brightness (float): Яркость от 0.0 до 1.0 (по умолчанию: 1.0)
    """
    
    def __init__(self, din_pin=23, cin_pin=24, brightness=1.0):
        self.DIN_PIN = din_pin
        self.CIN_PIN = cin_pin
        self.num_leds = 1
        self.brightness = max(0.0, min(1.0, brightness))  # Ограничение 0-1
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.DIN_PIN, GPIO.OUT)
        GPIO.setup(self.CIN_PIN, GPIO.OUT)
        GPIO.output(self.DIN_PIN, False)
        GPIO.output(self.CIN_PIN, False)
        
        # Автоматическая очистка при завершении
        atexit.register(self.cleanup)
        
        # Выключить все светодиоды при старте
        self.clear()
        print(f"LEDStripDriver инициализирован: {num_leds} светодиод(ов), пины DIN={din_pin}, CIN={cin_pin}")
    
    def _send_byte(self, val):
        """Приватный метод: отправка одного байта через DIN с тактированием по CIN"""
        for i in range(8):
            GPIO.output(self.DIN_PIN, (val & 0x80) != 0)
            GPIO.output(self.CIN_PIN, True)
            time.sleep(0.000005)  # 5µs
            GPIO.output(self.CIN_PIN, False)
            time.sleep(0.000005)  # 5µs
            val <<= 1
    
    def _send_pixel(self, r, g, b):
        """Приватный метод: отправка одного пикселя в формате P9813"""
        # Применение яркости
        r = int(r * self.brightness)
        g = int(g * self.brightness)
        b = int(b * self.brightness)
        
        # Ограничение значений 0-255
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        
        # Стартовый фрейм (4×0x00)
        for _ in range(4):
            self._send_byte(0x00)
        
        # Контрольный байт
        control = 0xC0 \
            | ((0x03 - ((r >> 6) & 0x03)) << 4) \
            | ((0x03 - ((g >> 6) & 0x03)) << 2) \
            | (0x03 - ((b >> 6) & 0x03))
        self._send_byte(control)
        
        # Цвета в порядке B, G, R
        self._send_byte(b)
        self._send_byte(g)
        self._send_byte(r)
        
        # Завершающий фрейм
        for _ in range(4):
            self._send_byte(0x00)
        
        # Защелкивание данных
        time.sleep(0.001)
    
    def set_brightness(self, brightness):
        """
        Установка общей яркости ленты
        
        Args:
            brightness (float): Яркость от 0.0 до 1.0
        """
        self.brightness = max(0.0, min(1.0, brightness))
        print(f"Яркость установлена: {self.brightness * 100:.0f}%")
    
    def set_color(self, r, g, b, led_index=0):
        """
        Установка цвета для одного светодиода
        
        Args:
            r (int): Красный (0-255)
            g (int): Зеленый (0-255)
            b (int): Синий (0-255)
            led_index (int): Индекс светодиода (по умолчанию: 0)
        
        Returns:
            bool: True если цвет установлен, False если индекс вне диапазона
        """
        if 0 <= led_index < self.num_leds:
            self._send_pixel(r, g, b)
            return True
        return False
    
    def set_color_all(self, r, g, b):
        """
        Установка одинакового цвета для всех светодиодов
        
        Args:
            r (int): Красный (0-255)
            g (int): Зеленый (0-255)
            b (int): Синий (0-255)
        """
        self.set_color(r, g, b, 0)
    
    def set_color_rgb(self, rgb_tuple):
        """
        Установка цвета из кортежа RGB
        
        Args:
            rgb_tuple (tuple): Кортеж из трех значений (R, G, B)
        """
        if len(rgb_tuple) == 3:
            self.set_color(rgb_tuple[0], rgb_tuple[1], rgb_tuple[2])
    
    def set_color_hex(self, hex_color):
        """
        Установка цвета из HEX-строки
        
        Args:
            hex_color (str): HEX-цвет в формате '#RRGGBB' или 'RRGGBB'
        """
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 6:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            self.set_color(r, g, b)
    
    def clear(self):
        """Выключить все светодиоды"""
        self.set_color_all(0, 0, 0)
        print("Все светодиоды выключены")
    
    def demo_sequence(self, delay=1.0):
        """
        Демонстрационная последовательность цветов
        
        Args:
            delay (float): Задержка между цветами в секундах
        """
        colors = [
            ("Красный", (255, 0, 0)),
            ("Оранжевый", (255, 165, 0)),
            ("Желтый", (255, 255, 0)),
            ("Зеленый", (0, 255, 0)),
            ("Голубой", (0, 255, 255)),
            ("Синий", (0, 0, 255)),
            ("Фиолетовый", (128, 0, 128)),
            ("Розовый", (255, 192, 203)),
            ("Белый", (255, 255, 255)),
        ]
        
        print("Запуск демонстрационной последовательности:")
        for name, (r, g, b) in colors:
            print(f"  {name}")
            self.set_color(r, g, b)
            time.sleep(delay)
        
        self.clear()
        print("Демонстрация завершена")
    
    def breathing_effect(self, r, g, b, cycles=3, duration=3.0):
        """
        Эффект дыхания (плавное изменение яркости)
        
        Args:
            r, g, b (int): Базовый цвет
            cycles (int): Количество циклов дыхания
            duration (float): Длительность одного цикла в секундах
        """
        steps = 50
        delay = duration / (2 * steps)  # Делим на 2 для вдоха и выдоха
        
        for _ in range(cycles):
            # Вдох (увеличение яркости)
            for i in range(steps):
                brightness = i / steps
                self._send_pixel(
                    int(r * brightness),
                    int(g * brightness),
                    int(b * brightness)
                )
                time.sleep(delay)
            
            # Выдох (уменьшение яркости)
            for i in range(steps, -1, -1):
                brightness = i / steps
                self._send_pixel(
                    int(r * brightness),
                    int(g * brightness),
                    int(b * brightness)
                )
                time.sleep(delay)
    
    def rainbow(self, cycles=1, speed=0.05):
        """
        Радужный эффект
        
        Args:
            cycles (int): Количество циклов радуги
            speed (float): Скорость смены цветов
        """
        print(f"Радужный эффект ({cycles} цикл(ов))")
        for cycle in range(cycles):
            for i in range(256):
                # Генерация радужных цветов
                if i < 85:
                    r = i * 3
                    g = 255 - i * 3
                    b = 0
                elif i < 170:
                    i -= 85
                    r = 255 - i * 3
                    g = 0
                    b = i * 3
                else:
                    i -= 170
                    r = 0
                    g = i * 3
                    b = 255 - i * 3
                
                self.set_color(r, g, b)
                time.sleep(speed)
            print(f"  Цикл {cycle + 1} завершен")
    
    def police_lights(self, duration=10.0, speed=0.2):
        """
        Имитация полицейских мигалок
        
        Args:
            duration (float): Общая длительность эффекта в секундах
            speed (float): Скорость мигания
        """
        print("Полицейские мигалки")
        end_time = time.time() + duration
        
        while time.time() < end_time:
            # Красный
            self.set_color(255, 0, 0)
            time.sleep(speed)
            self.clear()
            time.sleep(0.05)
            
            # Синий
            self.set_color(0, 0, 255)
            time.sleep(speed)
            self.clear()
            time.sleep(0.05)
    
    def fade_between_colors(self, color1, color2, steps=50, duration=2.0):
        """
        Плавный переход между двумя цветами
        
        Args:
            color1 (tuple): Первый цвет (R, G, B)
            color2 (tuple): Второй цвет (R, G, B)
            steps (int): Количество шагов перехода
            duration (float): Длительность перехода в секундах
        """
        delay = duration / steps
        
        for step in range(steps + 1):
            ratio = step / steps
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            
            self.set_color(r, g, b)
            time.sleep(delay)
    
    def get_status(self):
        """
        Получение статуса драйвера
        
        Returns:
            dict: Словарь с информацией о состоянии драйвера
        """
        return {
            "din_pin": self.DIN_PIN,
            "cin_pin": self.CIN_PIN,
            "num_leds": self.num_leds,
            "brightness": self.brightness,
            "gpio_mode": "BCM"
        }
    
    def cleanup(self):
        """Очистка GPIO и выключение светодиодов"""
        print("Очистка ресурсов LEDStripDriver...")
        self.clear()
        GPIO.cleanup()
