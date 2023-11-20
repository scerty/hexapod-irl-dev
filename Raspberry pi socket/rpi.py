
import socket
import pickle





import RPi.GPIO as GPIO
import time
import threading

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Define servo pins
#servo_pins = [11,5,0,16,6,19,21,13,26,3,2,14,22,27,17,20,15,10]
servo_pins = [21,13,26,16,6,19,11,5,0,20,10,15,22,27,17,3,2,14]
t="90 90 110 100 90 100 120 90 110 140 90 110 90 90 100 45 90 80"

# Set up GPIO for all servo pins
for servo_pin in servo_pins:
    GPIO.setup(servo_pin, GPIO.OUT)

# Define PWM frequency and duty cycle range for all servos
servos = [GPIO.PWM(pin, 50) for pin in servo_pins]
for servo in servos:
    servo.start(0)

# Define function to set the angle of a specific servo
def set_angle(servo, angle):
    duty = angle / 18 + 2  # Map angle (0 to 180) to duty cycle (2 to 12)
    GPIO.output(servo, True)
    servos[servo_pins.index(servo)].ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(servo, False)
    servos[servo_pins.index(servo)].ChangeDutyCycle(0)







# Define the server address and port
server_address = ('192.168.100.115', 3000)

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen()

print(f"Server is listening on {server_address[0]}:{server_address[1]}")

# Accept incoming connection
client_socket, client_address = server_socket.accept()

while True :
    received_data = client_socket.recv(4096)
    if not received_data:
        break

    received_list = pickle.loads(received_data)
    #print(received_list)
   # angles=received_list
    normal_list = list(received_list)
    servo_pins = [int(gpio.split()[1]) for gpio in received_list.keys()]
    angles = list(received_list.values())
    print(servo_pins)
    print(angles)

    print("----------------------------")





    def move_all_servos(angles):
        threads = []
        for servo, angle in zip(servo_pins, angles):
            thread = threading.Thread(target=set_angle, args=(servo, angle))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()

    move_all_servos(map(int, angles))
    #move_all_servos(angles)

