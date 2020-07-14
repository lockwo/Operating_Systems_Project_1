# import p1
from rand48 import Rand48
from process import Process
from params import Params
import print_sim


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
            + str(time)
            + "ms: Process "
            + processes[i].name
            + " arrived; added to the ready queue "
            + "[Q"
        )

        if len(readyQueue) == 0:
            msg += " <empty>]"
            print(msg)
        else:
            msg += getNames(readyQueue, [])
            print(msg)


# msg = "time " + str(time) + "ms: Process " + processes[i].name + \
# " started using the CPU for " + \
# str(processes[i].burst_time[current_burst_num]) \
# + "ms burst " + "[Q"
# time += params.t_cs / 2


def sjf(time, processes, params):
    readyQueue = dict()
    # add any processes that need to be added, onto the ready queue
    addOntoQueue(readyQueue, processes, time)

    # get the next process to be in the running state
    # perform tie breakers

    # get the smallest CPU Burst time or predicted CPU Burst time
    smallest = min(readyQueue)

    # if more than one, perform tie breaker
    if len(readyQueue[smallest]) > 1:
        nextProcess = tiebreaker(readyQueue[smallest])
    else:
        nextProcess = readyQueue[smallest].pop(0)

    print(nextProcess)


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

    time = 9
    print_sim.p_sim(0, processes, [], params, "SJF")
    sjf(time, processes, params)
