import sys
import threading
import socket
import time 
import random
import pickle

# broadcast
SEPARATOR = "<>"

Evntlst = {}
profId = 0

def vector_compare(vec1,vec2):
    vector = [max(value) for value in zip(vec1,vec2)]
    return vector

def handler(conn,add):
    # confirm the connection
    # Determine the operation the client wants to execute by checking the flag.
    print(f"\n[+] {add} is connected.")
    receive = conn
    if receive:
        print(f"Before Receiving: Vector clock for all events:{Evntlst}\n")
        data = pickle.loads(receive)

        for key in Evntlst:
            if key != data["sEvntId"]:
                rEvntId = key

                vector = vector_compare(data["sEvntData"] , Evntlst[rEvntId])
                Evntlst[key] = vector
                print(f"New Vector Value For Event:{rEvntId} is {vector}")
                print("\n")
            
                if (rEvntId + 1) in Evntlst:
                    for i in range(rEvntId + 1, len(Evntlst) + 1):
                        Evntlst[i] = vector_compare(Evntlst[i-1],Evntlst[i])
        
        
        receive = None      

def listener(node):
    while True:
        conn,addr = node.recvfrom(1024)
        print(f"\nRecieveing Message From:{addr}")
        print("\n")
        if conn and addr:
            thread = threading.Thread(target=handler,args=(conn,addr))
            thread.start()



def sender():
    while True:
        opt = int(input(" 1. Enter 1 to Communicate\n 2. Enter 2 to Skip\n 3. Enter 0 to Quit\nChoice:"))
        print("\n")
        if opt == 1:
            print(f"Before Sending: Vector clock for all events:{Evntlst}\n")
            recvPort = int(input("Enter port number of reciever: "))
            print("\n")
            if recvPort:
                msgdata = {}
                
                sEvntId = int(input("Enter Sender Event Number:"))
                print("\n")
                Evntlst[sEvntId][profId-1] += 1
                sEvntData = Evntlst[sEvntId]
                print("\n")

                msgdata["sEvntId"] = sEvntId
                msgdata["sEvntData"] = sEvntData
                data = pickle.dumps(msgdata)
                try:
                    print(f"\nBroadcasting Message to 127.0.0.1:{recvPort}\n")
                    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,socket.IPPROTO_UDP)
                    conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    conn.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) #setting to broadcast mode
                    conn.connect(('localhost',recvPort))
                    broadcast_address = ('<broadcast>', recvPort)
                    print(f"\n[+] Connected and sending\n")

                    conn.sendto(data,broadcast_address)
                    time.sleep(2)
                    conn.close()
                    print(f"After Sending: Vector clock for all events:{Evntlst}\n")
                except Exception as e:
                    print(e)
                finally:
                    recvPort = None
        elif opt == 2:
            print("\n")
        else:
            print("Current Vector Clock For All Events On This Node\n")
            print(Evntlst)
            sys.exit()


def main(port):
    node = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    node.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    node.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) #enabling the transmission setting

    node.bind(('',port))

    lst_thread = threading.Thread(target=listener,args=(node,))
    snd_thread = threading.Thread(target=sender,args=())
    lst_thread.start()
    snd_thread.start()

    


if __name__ == '__main__':
    port = int(input("Enter port number for this node:"))
    print("\n")
    pid = int(input("Process Id for this node(1/2/3):"))
    print("\n")
    profId = pid

    n1 = int(input(f"Enter the no. of events in Process {pid} : "))
    print("\n")
    e1 = [i for i in range(1, n1 + 1)]
    if pid == 1:
        Evntlst = {key: [key, 0, 0] for key in e1}
    elif pid == 2:
        Evntlst = {key: [0, key, 0] for key in e1}
    elif pid == 3:
        Evntlst = {key: [0, 0, key] for key in e1}
    print(Evntlst)
    print("\n")

    main(port)