# main_script.py


import RPi.GPIO as GPIO
import time
import tkinter as tk
import tkinter.font as tkFont  # Add this import at the beginning of your script

# Global variable to track if any red sensor has been triggered
L_red_sensor_triggered = False
R_red_sensor_triggered = False

class GpioTkinterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GPIO Tkinter App")
        self.root.geometry("1600x950")
        
        self.start_time = None
        self.L_reaction_time = None
        self.R_reaction_time = None

        self.L_reaction_recorded = False
        self.R_reaction_recorded = False
        
        self.button_press_times = {'L_Start': None, 'R_Start': None}

        self.init_gpio()
        self.create_widgets()

    def init_gpio(self):
        GPIO.setmode(GPIO.BCM)

        # Define button and LED pins
        self.pin_config = {
            'sensor_pins': {
                'L_Start': 26,
                'R_Start': 13,
                'L_Stage': 6,
                'R_Stage': 5,
            },
            'ligth_pins': {
                'L_Blue1': 7,
                'R_Blue1': 20,
                'L_Blue2': 8,
                'R_Blue2': 21,
                'Yellow1': 24,
                'Yellow2': 25,
                'Yellow3': 17,
                'L_Green': 27,
                'R_Green': 23,
                'L_Red': 4,
                'R_Red': 18,
            }
        }

        for pin in self.pin_config['sensor_pins'].values():
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(pin, GPIO.BOTH, callback=self.button_changed, bouncetime=1)

        for pin in self.pin_config['ligth_pins'].values():
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
    def create_widgets(self):
        # Create and configure label for "Next" button state
        self.next_label = tk.Label(root, text="Next Button State: 1")
        self.next_label.pack(pady=10)

        # Create "Next" button
        self.next_button_state = 1
        self.next_button = tk.Button(root, text="Next", command=self.next_button_pressed)
        self.next_button.pack(pady=10)

        # Create a font object for extra large text
        extra_large_font = tkFont.Font(family="Helvetica", size=150, weight="bold") 

        # Reaction time labels with extra large font and positioned at the edges
        self.L_reaction_label = tk.Label(root, text="--", font=extra_large_font)
        self.L_reaction_label.pack(side='left', padx=10)  # Position on the left edge

        self.R_reaction_label = tk.Label(root, text="--", font=extra_large_font)
        self.R_reaction_label.pack(side='right', padx=10)  # Position on the right edge


    def l_red_sensor_interrupt(self, pin):
        global L_red_sensor_triggered
        L_red_sensor_triggered = True
    def r_red_sensor_interrupt(self, pin):
        global R_red_sensor_triggered
        R_red_sensor_triggered = True

    def button_changed(self, channel):
        button_name = [name for name, pin in self.pin_config['sensor_pins'].items() if pin == channel][0]
        corresponding_led = self.get_corresponding_led(button_name)

        if GPIO.input(channel) == GPIO.LOW:
            print(f"{button_name} Pressed!")
            # Turn on the corresponding LED
            GPIO.output(corresponding_led, GPIO.HIGH)

            current_time = time.time()

            if button_name == 'L_Start' and self.next_button_state == 3 and not self.L_reaction_recorded:
                self.button_press_times['L_Start'] = current_time
                if self.start_time is not None:
                    self.L_reaction_time = (time.time() - self.start_time)
                    print(f"L reaction time: {self.L_reaction_time} ms")
                    self.update_reaction_times()
                    self.L_reaction_recorded = True

            elif button_name == 'R_Start' and self.next_button_state == 3 and not self.R_reaction_recorded:
                self.button_press_times['R_Start'] = current_time
                if self.start_time is not None:
                    self.R_reaction_time = (time.time() - self.start_time)
                    print(f"R reaction time: {self.R_reaction_time} ms")
                    self.update_reaction_times()
                    self.R_reaction_recorded = True
        else:
            print(f"{button_name} Released!")
            # Turn off the corresponding LED
            GPIO.output(corresponding_led, GPIO.LOW)

    def update_reaction_times(self):
        # Assuming you have labels for displaying reaction times
        if self.L_reaction_time is not None:
            self.L_reaction_label.config(text=f"{self.L_reaction_time:.3f}")
        if self.R_reaction_time is not None:
            self.R_reaction_label.config(text=f"{self.R_reaction_time:.3f}")  

    def get_corresponding_led(self, button_name):
        # Determine the corresponding LED based on the pressed button
        if button_name == 'L_Start':
            return self.pin_config['ligth_pins']['L_Red']
        elif button_name == 'R_Start':
            return self.pin_config['ligth_pins']['R_Red']
        elif button_name == 'L_Stage':
            return self.pin_config['ligth_pins']['L_Blue2']
        elif button_name == 'R_Stage':
            return self.pin_config['ligth_pins']['R_Blue2']
        
    def next_button_pressed(self):

        # Update the next button state and label
        self.next_button_state = (self.next_button_state % 4) + 1
        print(f"Next Button State: {self.next_button_state}")
        self.next_label.config(text=f"Next Button State: {self.next_button_state}")

        # Reset the red sensor triggered flag for the new state
        global L_red_sensor_triggered
        global R_red_sensor_triggered
        L_red_sensor_triggered = False
        R_red_sensor_triggered = False
        self.button_press_times = {'L_Start': None, 'R_Start': None}

        # Perform additional actions based on the current next_button_state

        if self.next_button_state == 2:
            GPIO.output(self.pin_config['ligth_pins']['L_Blue1'], GPIO.HIGH)
            GPIO.output(self.pin_config['ligth_pins']['R_Blue1'], GPIO.HIGH)
            self.L_reaction_label.config(text=f"--")
            self.R_reaction_label.config(text=f"--")  

        elif self.next_button_state == 3:
            
            self.start_time = None
            self.L_reaction_recorded = False
            self.R_reaction_recorded = False
            self.L_reaction_time = None
            self.R_reaction_time = None
            time.sleep(3)
            for pin_name in ['Yellow1', 'Yellow2', 'Yellow3']:
                GPIO.output(self.pin_config['ligth_pins'][pin_name], GPIO.HIGH)
                time.sleep(0.5)  # Turn on for half a second
                GPIO.output(self.pin_config['ligth_pins'][pin_name], GPIO.LOW)
            # Additional action for state 3: Check for red sensor activation
            if not L_red_sensor_triggered:
                GPIO.output(self.pin_config['ligth_pins']['L_Green'], GPIO.HIGH)
            else:
                print("L_Red sensor triggered during Yellow countdown. Skipping green LEDs.")
                GPIO.output(self.pin_config['ligth_pins']['L_Red'], GPIO.LOW)
                
            if not R_red_sensor_triggered:
                GPIO.output(self.pin_config['ligth_pins']['R_Green'], GPIO.HIGH)                
            else:
                print("R_Red sensor triggered during Yellow countdown. Skipping green LEDs.")
                GPIO.output(self.pin_config['ligth_pins']['R_Red'], GPIO.LOW)
            self.start_time = time.time()
            # Calculate negative reaction times if there were false starts
            for button in ['L_Start', 'R_Start']:
                press_time = self.button_press_times.get(button)
                if press_time and press_time < self.start_time:
                    reaction_time = -(self.start_time - press_time)
                    if button == 'L_Start':
                        self.L_reaction_time = reaction_time
                        self.L_reaction_recorded = True
                    elif button == 'R_Start':
                        self.R_reaction_time = reaction_time
                        self.R_reaction_recorded = True

            self.update_reaction_times()

        elif self.next_button_state == 4:
            GPIO.output(self.pin_config['ligth_pins']['L_Blue1'], GPIO.LOW)
            GPIO.output(self.pin_config['ligth_pins']['R_Blue1'], GPIO.LOW)
           

        else:
            # Turn off specific LEDs if not in state 3
            GPIO.output(self.pin_config['ligth_pins']['Yellow1'], GPIO.LOW)
            GPIO.output(self.pin_config['ligth_pins']['Yellow2'], GPIO.LOW)
            GPIO.output(self.pin_config['ligth_pins']['Yellow3'], GPIO.LOW)
            
            # Turn off specific LEDs when state is 1 or 2
            if self.next_button_state in [1, 2]:
                GPIO.output(self.pin_config['ligth_pins']['L_Green'], GPIO.LOW)
                GPIO.output(self.pin_config['ligth_pins']['R_Green'], GPIO.LOW)

if __name__ == "__main__":
    root = tk.Tk()
    app = GpioTkinterApp(root)
    root.mainloop()
