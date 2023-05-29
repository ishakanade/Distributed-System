import time
import random

def average_time(node_curr_time, server_time):

    time_diff = 0
    for i in node_curr_time:
        time_diff += i - server_time

    avg_time = time_diff/(len(node_curr_time))
    server_time = avg_time+server_time
    print("\nUpdated Server time ",server_time)

    return server_time

def berkeleyAlgorithm(node_curr_time, server_time):

    avg_time = average_time(node_curr_time, server_time)

    updated_time = []

    for i in range(len(node_curr_time)):
        updated_time.append(avg_time)

    return updated_time


if __name__ == "__main__":

    node_count = int(input("Enter number of process : "))
    
    node_curr_time = []

    for i in range(node_count):
        print("Enter time for node ",i," in hr format : ")
        time_input = int(input())
        node_curr_time.append(time_input)

    
    print("\nEnter Server time : ")
    server_time  = int(input())

    print("\nInitial time of nodes")
    for i in range(node_count): 
        print("Time at node ",i," is ", node_curr_time[i])

    updated_time = berkeleyAlgorithm(node_curr_time, server_time)
    print("\nUpdated time of nodes")
    for i in range(node_count): 
        print("Time at node ",i," is ", updated_time[i])