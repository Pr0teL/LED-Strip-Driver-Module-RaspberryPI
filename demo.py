# demo.py
from led_strip_driver import LEDStripDriver
import time

def show_menu():
    print("\n" + "="*40)
    print("RGB LED Control")
    print("="*40)
    print("1. Set color (RGB)")
    print("2. Set color (HEX)")
    print("3. Color demonstration")
    print("4. Breathing effect")
    print("5. Rainbow")
    print("6. Police lights")
    print("7. Change brightness")
    print("8. Turn off")
    print("9. Exit")
    print("="*40)

def main():
    led = LEDStripDriver()
    
    while True:
        show_menu()
        choice = input("Select action (1-9): ").strip()
        
        if choice == "1":
            try:
                r = int(input("Red (0-255): "))
                g = int(input("Green (0-255): "))
                b = int(input("Blue (0-255): "))
                led.set_color(r, g, b)
                print(f"Color set: RGB({r}, {g}, {b})")
            except ValueError:
                print("Error: enter numbers from 0 to 255")
        
        elif choice == "2":
            hex_color = input("Enter HEX color (e.g., #FF00FF): ")
            led.set_color_hex(hex_color)
            print(f"Color set: {hex_color}")
        
        elif choice == "3":
            delay = float(input("Delay between colors (sec): "))
            led.demo_sequence(delay)
        
        elif choice == "4":
            try:
                r = int(input("Red (0-255): "))
                g = int(input("Green (0-255): "))
                b = int(input("Blue (0-255): "))
                cycles = int(input("Number of cycles: "))
                led.breathing_effect(r, g, b, cycles=cycles, duration=2.0)
            except ValueError:
                print("Input error")
        
        elif choice == "5":
            cycles = int(input("Number of rainbow cycles: "))
            led.rainbow(cycles=cycles, speed=0.03)
        
        elif choice == "6":
            duration = float(input("Duration (sec): "))
            led.police_lights(duration=duration, speed=0.1)
        
        elif choice == "7":
            try:
                brightness = float(input("Brightness (0.0 - 1.0): "))
                led.set_brightness(brightness)
            except ValueError:
                print("Error: enter number from 0.0 to 1.0")
        
        elif choice == "8":
            led.clear()
            print("LED turned off")
        
        elif choice == "9":
            print("Exiting program...")
            break
        
        else:
            print("Invalid choice. Try again.")
        
        time.sleep(0.5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
