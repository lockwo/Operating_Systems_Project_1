# import p1
from rand48 import Rand48
from process import Process
from params import Params

# SJF

def sjf(time, processes, params):
    # Make the ready queue
    readyQueue = dict()
    
    # Add all current processes
    for i in range(len(processes)):
        current_burst_num = processes[i].current_burst_num
        key = processes[i].burst_time[current_burst_num]

        if key in readyQueue: # adds onto the list
            readyQueue[key].append(processes[i])
        else: # makes the list
            readyQueue[key] = [ processes[i] ]

        # we don't need to update the current_burst_num yet

    print(readyQueue)

if __name__ == '__main__':

    params = Params("10", "123123", ".001", "3000", "10", "1", "1", "END")
    processes = []
    ran = Rand48(params.seed)
    ran.srand(params.seed)
    for i in range(params.n):
        processes.append(Process(chr(i + 65), params, ran))

    # did not add params yet
    sjf(0, processes, params)