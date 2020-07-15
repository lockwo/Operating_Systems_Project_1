# import p1
from rand48 import Rand48
from process import Process
from params import Params
import print_sim
import math

def sjf(processes, params):
    readyQueue = dict()
    time = 0 # change to 0 later and have loop code set it
    nextTime = -1

    while (not allDone(processes)):
        
        # if time > 200:
        #     break
        
        # See if any processes need to be added
        addOntoQueue(readyQueue, processes, time)

        # if the process running is still not done
        if time < nextTime:
            time += 1
            continue

        # Now finish up the process and switch it out
        if time == nextTime:
            finishCPU(readyQueue, time, nextProcess)
            if nextProcess.done:
                time += params.t_cs / 2
                continue
            recalculateTau(readyQueue, params, time, nextProcess)
            time = switchOut(readyQueue, params, time, nextProcess)
            continue

        # Skip if nothing to add from readyQueue
        if len(readyQueue) == 0:
            time += 1
            continue

        # get the next process with the smallest predicted CPU Burst time
        smallest = min(readyQueue)

        # if more than one, perform tie breaker
        if len(readyQueue[smallest]) > 1:
            nextProcess = tiebreaker(readyQueue[smallest])
        else:
            nextProcess = readyQueue[smallest].pop(0)
            readyQueue.pop(smallest) # Must remove the empty []

        nextTime = usingCPU(readyQueue, time, params, nextProcess)

        time += 1

    msg = (
        "time "
        + str(int(time))
        + "ms: Simulator ended for SJF [Q <empty>]"
    )
    print(msg)


def addOntoQueue(readyQueue, processes, time):
    # Add all current processes
    for i in range(len(processes)):
        # Skip if the process arrival didn't occur yet
        if time < processes[i].arrival_time:
            continue
        # Skip if done bursting
        if processes[i].current_burst_num >= processes[i].num_burst:
            continue

        if processes[i].done:
            continue

        # Skip if blocked for I/O
        if processes[i].blocked_IO > time:
            continue

        for l in readyQueue.values():
            for j in l:
                if j.name == processes[i].name:
                    return

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

        # Update blocked IO
        index = processes[i].current_burst_num
        if not (index >= processes[i].num_burst): # there's one less io burst
            if (index == processes[i].num_burst - 1):
                processes[i].done = True
                return
            processes[i].blocked_IO = processes[i].IO_burst[index]
            processes[i].blocked_IO += processes[i].burst_time[index]
            processes[i].blocked_IO += time + params.t_cs


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

    # return the time the job is finished
    return nextProcess.burst_time[nextProcess.current_burst_num] + time

def finishCPU(readyQueue, time, nextProcess):
    # Update time, current_burst_num
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
        )
        if nextProcess.num_burst - nextProcess.current_burst_num == 1:
            msg += (
                " burst to go [Q"
            )
        else:
            msg += (
                " bursts to go "
                + "[Q"
            )

    if len(readyQueue) == 0:
            msg += " <empty>]"
            print(msg)
    else:
        msg += getNames(readyQueue, [])
        print(msg)

    return time


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
    smallestProcess = processes[0]
    smallestName = smallestProcess.name
    for i in range(len(processes)):
        tmpProcess = processes[i]
        tmpName = tmpProcess.name
        if smallestName > tmpName:
            smallestName = tmpName
            smallestProcess = tmpProcess
    return smallestProcess


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
    # # update blocked IO
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

    for l in readyQueue.values():
        for p in l:
            print(p.name)

    # Context switch time - out
    time += params.t_cs / 2

    return time

def allDone(processes):
    for i in range(len(processes)):
        if processes[i].current_burst_num != processes[i].num_burst:
            return False
    return True

# Taken from https://stackoverflow.com/questions/33019698/how-to-properly-round-up-half-float-numbers-in-python
def normal_round(n):
    if n - math.floor(n) < 0.5:
        return math.floor(n)
    return math.ceil(n)


if __name__ == "__main__":
    params = Params(
        # n=1,
        # seed=2,
        # lam=0.01,
        # upper_bound=256,
        # t_cs=4,
        # alpha=0.5,
        # t_slice=128,
        # rr_add="END",
        n=2,
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
