# Name: Isha Kanade
# Roll No: 43135
# Batch: Q-9

# Imitating a clock server
from timeit import default_timer as timer
from functools import reduce
from dateutil import parser
import threading
import datetime
import socket
import time

# datastructure to store client's address and clock data
client_data = {}

# Nested Thread function to receive clock time from a connectd client
def startReceivingClockTime(connector, address):

    while True:
        # receive clock time
        clock_time_string = connector.recv(1024).decode()
        clock_time = parser.parse(clock_time_string)
        clock_time_diff = datetime.datetime.now() - clock_time

        client_data[address] = {
            "clock_time" : clock_time,
            "time_difference": clock_time_diff,
            "connector": connector
        }
        print("Client data updated with: "+ str(address),end="\n\n")
        time.sleep(5)

# Master thread function used to open portal for accepting clients over given port
def startConnecting(master_server):
    
    # Fetch clock time at slaves / clients

    while True:
        # Accepting a client / slave clock client
        master_slave_connector, addr = master_server.accept()
        slave_address = str(addr[0]) + ":" + str(addr[1])

        print(slave_address+ " got connected successfully")
        
        current_thread = threading.Thread(
            target= startReceivingClockTime,
            args= (master_slave_connector,slave_address)
        )
        current_thread.start()

# Subroutine function used to fetch average clock difference
def getAverageClockDiff():

    current_client_data = client_data.copy()

    time_difference_list = list(client['time_difference'] for client_addr, client in client_data.items())

    sum_of_clock_difference = sum(time_difference_list, datetime.timedelta(0,0))

    average_clock_difference = sum_of_clock_difference / len(client_data)

    return average_clock_difference

# Master sync thread function used to generate cycles of clock synchronization in the network
def synchronizeAllClocks():

    while True:

        print("New synchronization cycle started.")
        print("Number of clients to be synchronized: " + str(len(client_data)))

        if len(client_data) > 0:
            average_clock_difference = getAverageClockDiff()

            for client_addr, client in client_data.items():
                try:
                    synchronized_time = datetime.datetime.now() + average_clock_difference

                    client['connector'].send(str(synchronized_time).encode())

                except Exception as e:
                    print("Something went wrong while sending synchronized time through "+str(client_addr))
                    print("Exception occurred: "+ str(e))

        else:
            print("No client data. Synchronization not applicable.")

        print("\n\n")
        time.sleep(5)

# Function used to initiate the Clock Server / Master Node
def initiateClockServer(port = 8080):
    
    master_server = socket.socket()
    master_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    print("Socket at master node created successfully\n")

    master_server.bind(('',port))

    # Start listening to requests
    master_server.listen(10)
    print("Clock server started...\n")

    # Start making connections
    print("Starting to make connections ... \n")
    master_thread = threading.Thread(
        target= startConnecting,
        args= (master_server,)
    )

    master_thread.start()

    # Start synchronization
    print("Starting synchronization parallely ... \n")
    sync_thread = threading.Thread(
        target= synchronizeAllClocks,
        args=()
    )

    sync_thread.start()

# Driver function
if __name__ == '__main__':
    # Trigger the Clock Server
    initiateClockServer(port = 8080)




def startSendingTime(slave_client):
    while True:
        slave_client.send(str(datetime.datetime.now()).encode())
        print("Recent time sent successfully", end="\n\n")

        time.sleep(5)

def startReceivingTime(slave_client):
    while True:
        Synchronized_time = parser.parse(slave_client.recv(1024).decode())

        print("Synchronized time at the client is : "+ \
            str(Synchronized_time), end="\n\n")

def initiateSlaveClient(port=8080):

    slave_client=socket.socket()
        
    slave_client.connect(('127.0.0.1',port))

    print("Starting to send time to server\n")
    send_time_thread = threading.Thread(
                        target=startSendingTime,
                        args=(slave_client, ))
    send_time_thread.start()

    print("Starting to receive " + \
            "synchronized time from server\n")
    receive_time_thread=threading.Thread(
        target = startReceivingTime,
        args=(slave_client, ))
    receive_time_thread.start()



if __name__ == '__main__':

    initiateSlaveClient(port=8080)