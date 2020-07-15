# import p1
from rand48 import Rand48
from process import Process
from params import Params
import print_sim
import math


def getNames(readyQueue, processesInQueue):
    msg = ""

    # combine the values into one list
    for i in readyQueue.values():
        processesInQueue = processesInQueue + i

    for i in processesInQueue:
        msg += " " + i.name

    msg += "]"

    return msg


def tiebreaker(processes):
    smallestName = processes.pop(0)
    while len(processes) > 0:
        tmpName = processes.pop(0)
        if smallestName > tmpName:
            smallestName = tmpName
    return smallestName


def addOntoQueue(readyQueue, processes, time):
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

        # add into the dictionary
        key = processes[i].tau

        if key in readyQueue:
            readyQueue[key].append(processes[i])
        else:
            readyQueue[key] = [processes[i]]

        # Print msg
        msg = (
            "time "
            + str(int(time))
            + "ms: Process "
            + processes[i].name
            + " (tau "
            + str(int(processes[i].tau))
            + "ms)"
        )
        
        if processes[i].current_burst_num == 0:
            msg += (
                " arrived; added to ready queue "
                + "[Q"
            )
        else:
            msg += (
                " completed I/O; added to ready queue "
                + "[Q"
            )

        if len(readyQueue) == 0:
            msg += " <empty>]"
            print(msg)
        else:
            msg += getNames(readyQueue, [])
            print(msg)

# FIX PROCESS NUM, HOW TO GET THE PROCESS !!!

# msg = "time " + str(time) + "ms: Process " + processes[i].name + \
# " started using the CPU for " + \
# str(processes[i].burst_time[current_burst_num]) \
# + "ms burst " + "[Q"
# time += params.t_cs / 2

def usingCPU(readyQueue, time, params, nextProcess):
    # add context switch time
    time += params.t_cs / 2

    # Print Msg
    msg = (
        "time "
        + str(int(time))
        + "ms: Process "
        + nextProcess.name
        + " (tau "
        + str(int(nextProcess.tau))
        + "ms)"
        + " started using the CPU for "
        + str(nextProcess.burst_time[nextProcess.current_burst_num])
        + "ms burst "
        + "[Q"
    )

    if len(readyQueue) == 0:
            msg += " <empty>]"
            print(msg)
    else:
        msg += getNames(readyQueue, [])
        print(msg)

    return time

def finishCPU(readyQueue, time, nextProcess):
    # Update time, current_burst_num
    time += nextProcess.burst_time[nextProcess.current_burst_num]
    nextProcess.current_burst_num += 1

    if nextProcess.num_burst - nextProcess.current_burst_num == 0:
        msg = (
            "time "
            + str(int(time))
            + "ms: Process "
            + nextProcess.name
            + " terminated [Q"
        )
    else:
        bursts = "burst" if nextProcess.num_burst - nextProcess.current_burst_num == 1 else "bursts"
        msg = (
            "time "
            + str(int(time))
            + "ms: Process "
            + nextProcess.name
            + " (tau "
            + str(int(nextProcess.tau))
            + "ms)"
            + " completed a CPU burst; "
            + str(nextProcess.num_burst - nextProcess.current_burst_num)
            + f" {bursts} to go "
            + "[Q"
        )

    if len(readyQueue) == 0:
            msg += " <empty>]"
            print(msg)
    else:
        msg += getNames(readyQueue, [])
        print(msg)

    return time

def recalculateTau(readyQueue, params, time, nextProcess):
    # Recalculate 
    tau = nextProcess.tau
    turn = nextProcess.current_burst_num - 1
    alpha = params.alpha
    nextProcess.tau = normal_round((alpha * nextProcess.burst_time[turn]) + ((1 - alpha) * tau))

    # Print
    msg = (
        "time "
        + str(int(time))
        + "ms: Recalculated tau = "
        + str(int(nextProcess.tau)) # I believe this floors it, not sure if it will always be an int
        + "ms for process "
        + nextProcess.name
        + " [Q"
    )

    if len(readyQueue) == 0:
            msg += " <empty>]"
            print(msg)
    else:
        msg += getNames(readyQueue, [])
        print(msg)

def switchOut(readyQueue, params, time, nextProcess):
    # update blocked IO
    nextProcess.blocked_IO = nextProcess.IO_burst[nextProcess.current_burst_num - 1]
    nextProcess.blocked_IO += time + params.t_cs / 2

    # Print
    msg = (
        "time "
        + str(int(time))
        + "ms: Process "
        + nextProcess.name
        + " switching out of CPU; will block on I/O until time "
        + str(int(nextProcess.blocked_IO))
        + "ms "
        + "[Q"
    )

    if len(readyQueue) == 0:
            msg += " <empty>]"
            print(msg)
    else:
        msg += getNames(readyQueue, [])
        print(msg)

    # Context switch time - out
    time += params.t_cs / 2

    return time

def allDone(processes):
    for i in range(len(processes)):
        if processes[i].current_burst_num != processes[i].num_burst:
            return False
    return True

def print_start(processes):
    for i in processes:
        print(f"Process {i.name} [NEW] (arrival time {i.arrival_time} ms) {i.num_burst} CPU bursts (tau {int(i.tau)}ms)")
    temp_queue = []
    for i in sorted(processes, key=lambda x: x.arrival_time):
        if i.arrival_time == 0:
            temp_queue.append(i)
    queue_string = '<empty>' 
    if temp_queue:
        queue_string = ' '.join([i.name for i in temp_queue])
    print(f'time 0ms: Simulator started for SJF [Q {queue_string}]')


    
# Taken from https://stackoverflow.com/questions/33019698/how-to-properly-round-up-half-float-numbers-in-python
def normal_round(n):
    if n - math.floor(n) < 0.5:
        return math.floor(n)
    return math.ceil(n)

def sjf(processes, params):
    print_start(processes)
    readyQueue = dict()
    time = 0 # change to 0 later and have loop code set it
    while (not allDone(processes)):

        # add any processes that need to be added, onto the ready queue
        addOntoQueue(readyQueue, processes, time)

        # Skip if nothing to add from readyQueue
        if len(readyQueue) == 0:
            time += 1
            continue

        # get the process with the smallest predicted CPU Burst time
        smallest = min(readyQueue)

        # if more than one, perform tie breaker
        if len(readyQueue[smallest]) > 1:
            nextProcess = tiebreaker(readyQueue[smallest])
        else:
            nextProcess = readyQueue[smallest].pop(0)
            readyQueue.pop(smallest) # Must remove the empty []

        # now take the process and let it use the CPU
        time = usingCPU(readyQueue, time, params, nextProcess)
        time = finishCPU(readyQueue, time, nextProcess)

        # End?
        if nextProcess.num_burst - nextProcess.current_burst_num == 0:
            time += params.t_cs / 2
            continue

        recalculateTau(readyQueue, params, time, nextProcess)
        switchOut(readyQueue, params, time, nextProcess)

        time += 1
    
    msg = (
        "time "
        + str(int(time))
        + "ms: Simulator ended for SJF [Q <empty>]"
    )
    print(msg)


if __name__ == "__main__":
    params = Params(
        n=1,
        seed=2,
        lam=0.01,
        upper_bound=256,
        t_cs=4,
        alpha=0.5,
        t_slice=128,
        rr_add="END",
    )
    processes = []
    ran = Rand48(params.seed)
    ran.srand(params.seed)
    for i in range(params.n):
        processes.append(Process(chr(i + 65), params, ran))

    print_sim.p_sim(0, processes, [], params, "SJF")
    sjf(processes, params)
