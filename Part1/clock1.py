import sys
import threading
import socket
import time 
import random
import pickle

SEPARATOR = "<>"

EvntLst = {}

def vec_compare(vec1,vec2):
    vec = [max(val) for val in zip(vec1,vec2)] 
    return vec

def handler(conn,add):
    # confirm the connection
    # Determine the operation the client wants to execute by checking the flag.
    print(f"\n[+] {add} is connected.")
    receive = conn.recv(1024)
    if receive:
        print(f"Before Receiving: Vector clock for all events:{EvntLst}\n")
        data = pickle.loads(receive)
        rEvntId = data["rEvntId"]

        vec = vec_compare(data["sEvntData"] , EvntLst[rEvntId])
        EvntLst[data["rEvntId"]] = vec
        print(f"New Vector Value For Event:{rEvntId} is {vec}")
        print("\n")
        
        
        
        receive = None      
    conn.close()

def listener(node):
    while True:
        conn,addr = node.accept()
        print(f"\nRecieveing Message From:{addr}")
        print("\n")
        if conn and addr:
            thread = threading.Thread(target=handler,args=(conn,addr))
            thread.start()



def sender():
    while True:
        opt = int(input(" 1. Enter 1 to Communicate\n 2. Enter 2 to Skip\n 3. Enter 0 to QUIT\nChoice:"))
        print("\n")
        if opt == 1:
            print(f"Before Sending: Vector clock for all events:{EvntLst}\n")
            recvPort = int(input("Enter port number of reciever: "))
            print("\n")
            if recvPort:
                msgdata = {}
                
                sEvntId = int(input("Enter Sender Event Number:"))
                print("\n")
                sEvntData = EvntLst[sEvntId]
                rEvntId = int(input("Enter Reciever Event Number:"))
                print("\n")

                msgdata["sEvntId"] = sEvntId
                msgdata["sEvntData"] = sEvntData
                msgdata["rEvntId"] = rEvntId
                data = pickle.dumps(msgdata)
                try:
                    print(f"\nSending Message to 127.0.0.1:{recvPort}\n")
                    conn = socket.socket()
                    conn.connect(('localhost',recvPort))
                    print(f"\n[+] Connected and sending\n")

                    conn.sendall(data)
                    time.sleep(2)
                    conn.close()
                    print(f"After Sending: Vector clock for all events:{EvntLst}\n")
                except Exception as e:
                    print(e)
                finally:
                    recvPort = None
        elif opt == 2:
            print("\n")
        else:
            print("Current Vector Clock For All Events On This Node\n")
            print(EvntLst)
            sys.exit()


def main(port):
    node = socket.socket()
    node.bind(('',port))

    # Start listening
    node.listen(10)

    lst_thread = threading.Thread(target=listener,args=(node,))
    snd_thread = threading.Thread(target=sender,args=())
    lst_thread.start()
    snd_thread.start()

    


if __name__ == '__main__':
    port = int(input("Enter port number for this node:"))
    print("\n")
    pId = int(input("Process Id for this node(1/2/3):"))
    print("\n")

    n = int(input(f"Enter the no. of events in Process {pId} : "))
    print("\n")
    e1 = [i for i in range(1, n + 1)]
    if pId == 1:
        EvntLst = {key: [key, 0, 0] for key in e1}
    elif pId == 2:
        EvntLst = {key: [0, key, 0] for key in e1}
    elif pId == 3:
        EvntLst = {key: [0, 0, key] for key in e1}
    print(EvntLst)
    print("\n")

    main(port)