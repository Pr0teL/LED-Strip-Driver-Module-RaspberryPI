# led_strip_driver.py
import RPi.GPIO as GPIO
import time
import atexit
import math

class LEDStripDriver:
    """
    Driver for controlling RGB LED strip with P9813 chip
    
    Args:
        din_pin (int): GPIO pin for data (DIN) (default: 23)
        cin_pin (int): GPIO pin for clock signal (CIN) (default: 24)
        brightness (float): Brightness from 0.0 to 1.0 (default: 1.0)
    """
    
    def __init__(self, din_pin=23, cin_pin=24, brightness=1.0):
        self.DIN_PIN = din_pin
        self.CIN_PIN = cin_pin
        self.num_leds = 1
        self.brightness = max(0.0, min(1.0, brightness))  # Clamp to 0-1
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.DIN_PIN, GPIO.OUT)
        GPIO.setup(self.CIN_PIN, GPIO.OUT)
        GPIO.output(self.DIN_PIN, False)
        GPIO.output(self.CIN_PIN, False)
        
        # Automatic cleanup on exit
        atexit.register(self.cleanup)
        
        # Turn off all LEDs on startup
        self.clear()
        print(f"LEDStripDriver initialized: pins DIN={din_pin}, CIN={cin_pin}")
    
    def _send_byte(self, val):
        """Private method: send one byte via DIN with clocking via CIN"""
        for i in range(8):
            GPIO.output(self.DIN_PIN, (val & 0x80) != 0)
            GPIO.output(self.CIN_PIN, True)
            time.sleep(0.000005)  # 5µs
            GPIO.output(self.CIN_PIN, False)
            time.sleep(0.000005)  # 5µs
            val <<= 1
    
    def _send_pixel(self, r, g, b):
        """Private method: send one pixel in P9813 format"""
        # Apply brightness
        r = int(r * self.brightness)
        g = int(g * self.brightness)
        b = int(b * self.brightness)
        
        # Clamp values to 0-255
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        
        # Start frame (4×0x00)
        for _ in range(4):
            self._send_byte(0x00)
        
        # Control byte
        control = 0xC0 \
            | ((0x03 - ((r >> 6) & 0x03)) << 4) \
            | ((0x03 - ((g >> 6) & 0x03)) << 2) \
            | (0x03 - ((b >> 6) & 0x03))
        self._send_byte(control)
        
        # Colors in B, G, R order
        self._send_byte(b)
        self._send_byte(g)
        self._send_byte(r)
        
        # End frame
        for _ in range(4):
            self._send_byte(0x00)
        
        # Latch data
        time.sleep(0.001)
    
    def set_brightness(self, brightness):
        """
        Set overall strip brightness
        
        Args:
            brightness (float): Brightness from 0.0 to 1.0
        """
        self.brightness = max(0.0, min(1.0, brightness))
        print(f"Brightness set: {self.brightness * 100:.0f}%")
    
    def set_color(self, r, g, b, led_index=0):
        """
        Set color for a single LED
        
        Args:
            r (int): Red (0-255)
            g (int): Green (0-255)
            b (int): Blue (0-255)
            led_index (int): LED index (default: 0)
        
        Returns:
            bool: True if color set, False if index out of range
        """
        if 0 <= led_index < self.num_leds:
            self._send_pixel(r, g, b)
            return True
        return False
    
    def set_color_all(self, r, g, b):
        """
        Set same color for all LEDs
        
        Args:
            r (int): Red (0-255)
            g (int): Green (0-255)
            b (int): Blue (0-255)
        """
        self.set_color(r, g, b, 0)
    
    def set_color_rgb(self, rgb_tuple):
        """
        Set color from RGB tuple
        
        Args:
            rgb_tuple (tuple): Tuple of three values (R, G, B)
        """
        if len(rgb_tuple) == 3:
            self.set_color(rgb_tuple[0], rgb_tuple[1], rgb_tuple[2])
    
    def set_color_hex(self, hex_color):
        """
        Set color from HEX string
        
        Args:
            hex_color (str): HEX color in format '#RRGGBB' or 'RRGGBB'
        """
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 6:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            self.set_color(r, g, b)
    
    def clear(self):
        """Turn off all LEDs"""
        self.set_color_all(0, 0, 0)
        print("All LEDs turned off")
    
    def demo_sequence(self, delay=1.0):
        """
        Demonstration color sequence
        
        Args:
            delay (float): Delay between colors in seconds
        """
        colors = [
            ("Red", (255, 0, 0)),
            ("Orange", (255, 165, 0)),
            ("Yellow", (255, 255, 0)),
            ("Green", (0, 255, 0)),
            ("Cyan", (0, 255, 255)),
            ("Blue", (0, 0, 255)),
            ("Purple", (128, 0, 128)),
            ("Pink", (255, 192, 203)),
            ("White", (255, 255, 255)),
        ]
        
        print("Starting demonstration sequence:")
        for name, (r, g, b) in colors:
            print(f"  {name}")
            self.set_color(r, g, b)
            time.sleep(delay)
        
        self.clear()
        print("Demonstration completed")
    
    def breathing_effect(self, r, g, b, cycles=3, duration=3.0):
        """
        Breathing effect (smooth brightness change)
        
        Args:
            r, g, b (int): Base color
            cycles (int): Number of breathing cycles
            duration (float): Duration of one cycle in seconds
        """
        steps = 50
        delay = duration / (2 * steps)  # Divide by 2 for inhale and exhale
        
        for _ in range(cycles):
            # Inhale (increase brightness)
            for i in range(steps):
                brightness = i / steps
                self._send_pixel(
                    int(r * brightness),
                    int(g * brightness),
                    int(b * brightness)
                )
                time.sleep(delay)
            
            # Exhale (decrease brightness)
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
        Rainbow effect
        
        Args:
            cycles (int): Number of rainbow cycles
            speed (float): Color change speed
        """
        print(f"Rainbow effect ({cycles} cycle(s))")
        for cycle in range(cycles):
            for i in range(256):
                # Generate rainbow colors
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
            print(f"  Cycle {cycle + 1} completed")
    
    def police_lights(self, duration=10.0, speed=0.2):
        """
        Police lights simulation
        
        Args:
            duration (float): Total effect duration in seconds
            speed (float): Blinking speed
        """
        print("Police lights")
        end_time = time.time() + duration
        
        while time.time() < end_time:
            # Red
            self.set_color(255, 0, 0)
            time.sleep(speed)
            self.clear()
            time.sleep(0.05)
            
            # Blue
            self.set_color(0, 0, 255)
            time.sleep(speed)
            self.clear()
            time.sleep(0.05)
    
    def fade_between_colors(self, color1, color2, steps=50, duration=2.0):
        """
        Smooth transition between two colors
        
        Args:
            color1 (tuple): First color (R, G, B)
            color2 (tuple): Second color (R, G, B)
            steps (int): Number of transition steps
            duration (float): Transition duration in seconds
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
        Get driver status
        
        Returns:
            dict: Dictionary with driver state information
        """
        return {
            "din_pin": self.DIN_PIN,
            "cin_pin": self.CIN_PIN,
            "num_leds": self.num_leds,
            "brightness": self.brightness,
            "gpio_mode": "BCM"
        }
    
    def cleanup(self):
        """Cleanup GPIO and turn off LEDs"""
        print("Cleaning up LEDStripDriver resources...")
        self.clear()
        GPIO.cleanup()
