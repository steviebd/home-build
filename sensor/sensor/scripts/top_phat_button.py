import time
import RPi.GPIO as GPIO #Python Package Reference: https://pypi.org/project/RPi.GPIO/

# Code taken from https://learn.sparkfun.com/tutorials/raspberry-pi-safe-reboot-and-shutdown-button using the last example to minimize resources used (sleep function)

# Pin definition
reset_shutdown_pin = 17

# Suppress warnings
GPIO.setwarnings(False)

# Use "GPIO" pin numbering
GPIO.setmode(GPIO.BCM)

# Use built-in internal pullup resistor so the pin is not floating
# if using a momentary push button without a resistor.
#GPIO.setup(reset_shutdown_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Use Qwiic pHAT's pullup resistor so that the pin is not floating
GPIO.setup(reset_shutdown_pin, GPIO.IN)

# modular function to restart Pi
def restart():
    print("restarting Pi")
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)

# modular function to shutdown Pi
def shut_down():
    print("shutting down")
    command = "/usr/bin/sudo /sbin/shutdown -h now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)




while True:
    #short delay, otherwise this code will take up a lot of the Pi's processing power
    time.sleep(1)

    # wait for a button press with switch debounce on the falling edge so that this script
    # is not taking up too many resources in order to shutdown/reboot the Pi safely
    channel = GPIO.wait_for_edge(reset_shutdown_pin, GPIO.FALLING, bouncetime=200)

    if channel is None:
        print('Timeout occurred')
    else:
        print('Edge detected on channel', channel)

        # For troubleshooting, uncomment this line to output button status on command line
        #print('GPIO state is = ', GPIO.input(reset_shutdown_pin))
        counter = 0

        while GPIO.input(reset_shutdown_pin) == False:
            # For troubleshooting, uncomment this line to view the counter. If it reaches a value above 4, we will restart.
            #print(counter)
            counter += 1
            time.sleep(0.5)

            # long button press
            if counter > 4:
                shut_down()

        #if short button press, restart!
        restart()
