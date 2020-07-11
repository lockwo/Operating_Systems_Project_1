import p1
import rand48
import process

# SJF

def sjf(time, processes, params):
    # Make the ready queu
    readyQueue = dict()
    
    # Add all current processes
    for i in range(len(processes)):
        current_burst_num = processes[i].current_burst_num
        readyQueue[processes[i].burst_time[current_burst_num]] = processes[i] # add into readyQueue by burst_time
        # we don't need to update the current_burst_num yet

    print(readyQueue)


