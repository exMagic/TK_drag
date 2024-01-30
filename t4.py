import tkinter as tk
import RPi.GPIO as GPIO
import time

class GpioTkinterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GPIO Interrupts with Tkinter")
        self.root.geometry("700x500")  # Set window size

        # GPIO pin configuration
        self.pin_config = {
            'button_pins': {'Button 1': 26, 'Button 2': 13, 'Button 3': 6, 'Button 4': 5},
            'led_pins': {'Button 1': 7, 'Button 2': 8, 'Button 3': 18, 'Button 4': 23},
            'additional_pins': {'Pin 24': 24, 'Pin 25': 25, 'Pin 17': 17, 'Pin 27': 27, 'Pin 23': 23}
        }

        # Set up GPIO
        GPIO.setmode(GPIO.BCM)

        # Set up buttons with reduced bouncetime
        for pin in self.pin_config['button_pins'].values():
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(pin, GPIO.BOTH, callback=self.button_changed, bouncetime=1)

        # Set up LEDs
        for pin in self.pin_config['led_pins'].values():
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)  # Initially turn off all LEDs

        # Set up additional pins as OUTPUT
        for pin in self.pin_config['additional_pins'].values():
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)  # Initially set all OUTPUT pins to LOW

        # Create and configure labels for buttons
        self.button_labels = []
        for name, pin in self.pin_config['button_pins'].items():
            label = tk.Label(root, text=f"{name}: Waiting for press...")
            label.pack(pady=10)
            self.button_labels.append(label)

        # Create and configure label for "Next" button state
        self.next_label = tk.Label(root, text="Next Button State: 1")
        self.next_label.pack(pady=10)

        # Create "Next" button
        self.next_button_state = 1
        self.next_button = tk.Button(root, text="Next", command=self.next_button_pressed)
        self.next_button.pack(pady=10)

    def button_changed(self, channel):
        button_name = next(name for name, pin in self.pin_config['button_pins'].items() if pin == channel)
        if GPIO.input(channel) == GPIO.LOW:
            print(f"{button_name} Pressed!")
            self.button_labels[self.pin_config['button_pins'][button_name] - 26].config(text=f"{button_name}: Pressed!")

            # Turn on the corresponding LED
            GPIO.output(self.pin_config['led_pins'][button_name], GPIO.HIGH)
        else:
            print(f"{button_name} Released!")
            self.button_labels[self.pin_config['button_pins'][button_name] - 26].config(text=f"{button_name}: Released!")

            # Turn off the corresponding LED
            GPIO.output(self.pin_config['led_pins'][button_name], GPIO.LOW)

    def next_button_pressed(self):
        # Update the next button state and label
        self.next_button_state = (self.next_button_state % 4) + 1
        print(f"Next Button State: {self.next_button_state}")
        self.next_label.config(text=f"Next Button State: {self.next_button_state}")

        # Perform additional actions based on the current next_button_state
        if self.next_button_state == 3:
            time.sleep(1)
            for pin_name in ['Pin 24', 'Pin 25', 'Pin 17']:
                GPIO.output(self.pin_config['additional_pins'][pin_name], GPIO.HIGH)
                time.sleep(0.5)
            time.sleep(0.5)  # Additional half-second delay
            for pin_name in ['Pin 27', 'Pin 23']:
                GPIO.output(self.pin_config['additional_pins'][pin_name], GPIO.HIGH)
        else:
            # Turn off pins 27 and 23 if not in state 3
            GPIO.output(self.pin_config['additional_pins']['Pin 27'], GPIO.LOW)
            GPIO.output(self.pin_config['additional_pins']['Pin 23'], GPIO.LOW)

    def run(self):
        self.root.mainloop()

    def cleanup(self):
        # Turn off all LEDs and clean up GPIO
        for pin in self.pin_config['led_pins'].values():
            GPIO.output(pin, GPIO.LOW)
        for pin in self.pin_config['additional_pins'].values():
            GPIO.output(pin, GPIO.LOW)
        GPIO.cleanup()

if __name__ == "__main__":
    root = tk.Tk()
    app = GpioTkinterApp(root)

    try:
        app.run()
    except KeyboardInterrupt:
        pass
    finally:
        app.cleanup()
