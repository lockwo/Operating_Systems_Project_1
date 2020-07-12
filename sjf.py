# import p1
from rand48 import Rand48
from process import Process
from params import Params
import print_sim

# SJF

def sjf(time, processes, params):
    # Make the ready queue
    readyQueue = dict()
    
    # Add all current processes
    for i in range(len(processes)):
        # Skip if the process arrival didn't occur yet
        if time < processes[i].arrival_time:
            continue
        # Skip if the process is in the ready queue already
        if processes[i] in readyQueue.values():
            continue

        # Skip if done bursting
        if processes[i].current_burst_num >= processes[i].num_burst:
            continue

        # Skip if blocked for I/O
        if processes[i].blocked_IO > time:
            continue

        current_burst_num = processes[i].current_burst_num
        key = processes[i].burst_time[current_burst_num]

        if key in readyQueue: # adds onto the list
            readyQueue[key].append(processes[i])
        else: # makes the list
            readyQueue[key] = [ processes[i] ]

        # we don't need to update the current_burst_num yet

    #print(readyQueue)

if __name__ == '__main__':
    params = Params(n=1, seed=2, lam=0.01, upper_bound=256, t_cs=4, alpha=0.5, t_slice=128, rr_add='END')
    processes = []
    ran = Rand48(params.seed)
    ran.srand(params.seed)
    for i in range(params.n):
        processes.append(Process(chr(i + 65), params, ran))

    print_sim.p_sim(0, processes, [] , params, "SJF")
    sjf(0, processes, params)