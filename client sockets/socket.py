import socketio
import pickle
import socket
import time
n=0
dict={}
dict1={}
dict2={}
HOST = '127.0.0.1'
PORT = 65432

#
#========================START=============================================#
exp_server_address = ('192.168.100.115', 3000)
exp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
exp_client_socket.connect(exp_server_address)
#========================END=============================================#

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

@ sio.event
def connect(sid, environ):
    print(f'Client {sid} connected')

@ sio.event
def disconnect(sid):
    print(f'Client {sid} disconnected')
  
@ sio.event
def setServo(sid, data):
    global n
    global dict
    global dict1
    global dict2

    sender = data.get('sender')
    pose = data.get('pose')
   # print(f'Received pose data from {sender}: {pose["leftFront"]}')
    

    list_serv=[pose["leftFront"]["alpha"],pose["leftFront"]["beta"],pose["leftFront"]["gamma"],
                pose["leftMiddle"]["alpha"],pose["leftMiddle"]["beta"],pose["leftMiddle"]["gamma"],
                pose["leftBack"]["alpha"],pose["leftBack"]["beta"],pose["leftBack"]["gamma"],
                pose["rightFront"]["alpha"],pose["rightFront"]["beta"],pose["rightFront"]["gamma"],
                pose["rightMiddle"]["alpha"],pose["rightMiddle"]["beta"],pose["rightMiddle"]["gamma"],
                pose["rightBack"]["alpha"],pose["rightBack"]["beta"],pose["rightBack"]["gamma"],
                
                ]


    list_stnd=list_serv
    dict = {
    "GPIO 21": list_serv[0],
    "GPIO 13": list_serv[1],
    "GPIO 26": list_serv[2],
    "GPIO 16": list_serv[3],
    "GPIO 6": list_serv[4],
    "GPIO 19": list_serv[5],
    "GPIO 11": list_serv[6],
    "GPIO 5": list_serv[7],
    "GPIO 0": list_serv[8],
    "GPIO 20": list_serv[9],
    "GPIO 10": list_serv[10],
    "GPIO 15": list_serv[11],
    "GPIO 22": list_serv[12],
    "GPIO 27": list_serv[13],
    "GPIO 17": list_serv[14],
    "GPIO 3": list_serv[15],
    "GPIO 2": list_serv[16],
    "GPIO 14": list_serv[17]
}
    

    if n==0:
        dict1=dict2=dict
    else :
        dict2=dict



    diff_dict = {}

    # Compare dictionaries and generate the new dictionary
    for key in set(dict1) | set(dict2):
        if dict1.get(key) != dict2.get(key):
            diff_dict[key] =  dict2.get(key)
    print(diff_dict)
   
    

    dict1=dict2








    print(n)

# Compare dictionaries and generate the new dictionary
    
    
    n+=1


    message = pickle.dumps(diff_dict)
    exp_client_socket.sendall(message)
# Define the host and port for the server

# Start the server
if __name__ == '__main__':
    print(f'Server listening on {HOST}:{PORT}')
    import eventlet
    eventlet.wsgi.server(eventlet.listen((HOST, PORT)), app)
