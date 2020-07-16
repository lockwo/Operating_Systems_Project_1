from rand48 import Rand48
from process import Process
from params import Params
import print_sim
import math


def srt(processes, params):
    readyQueue = []
    ioQueue = []
    ordered = sorted(processes, key=lambda x: x.arrival_time)
    time = 0
    currentProcess = None
    started = False
    finished = False
    recalculated = False
    switched = False
    switchedOut = False
    switchedOutTime = 0
    startTime = 0
    toBeAdded = []
    mostRecentArrived = None

    while (len(ordered) != 0 or currentProcess != None or len(readyQueue) != 0 or len(ioQueue) != 0 or time < switchedOutTime):
        
        toBeAddedTmp = sorted(toBeAdded, key=lambda x: x.run_time)
        for i in toBeAddedTmp:
            if time >= i.run_time:
                readyQueue.append(i)
                toBeAdded.remove(i)
                # print(i.name + " added back at time " + str(time))

        
        # If there is a current process running
        if currentProcess != None and time >= switchedOutTime + params.t_cs / 2:
            if currentProcess in readyQueue and currentProcess.remove and currentProcess.run_time <= time:
                readyQueue.remove(currentProcess)
                currentProcess.remove = False

            name = currentProcess.name
            tau = int(currentProcess.tau)
            current_burst_num = currentProcess.current_burst_num
            arrival_time = int(currentProcess.arrival_time)
            if not started and time >= arrival_time + params.t_cs / 2 and time >= currentProcess.run_time:
                startTime = time
                started = True
                elapsed = (currentProcess.tau - currentProcess.originalTau)
                msg = f"time {time}ms: Process {name} (tau {tau}ms) started using the CPU"
                msg += f" with {int(currentProcess.burst_time[current_burst_num] - elapsed)}ms burst remaining [Q"
                msg += strReadyQueue(readyQueue)
                print(msg)
            completionTime = int(currentProcess.burst_time[current_burst_num] + startTime - elapsed)
            if not finished and time >= completionTime and started:
                finished = True
                currentProcess.current_burst_num += 1
                current_burst_num = currentProcess.current_burst_num

                if currentProcess.num_burst - current_burst_num == 0:
                    finished = False
                    msg = f"time {time}ms: Process {name} terminated [Q"
                    msg += strReadyQueue(readyQueue)
                    print(msg)
                    # set to none and change times
                    switchedOutTime = time + params.t_cs /2
                    currentProcess = None
                else:
                    msg = f"time {time}ms: Process {name} (tau {tau}ms) completed a CPU burst;"
                    msg += f" {currentProcess.num_burst - currentProcess.current_burst_num} burst"
                    if currentProcess.num_burst - currentProcess.current_burst_num != 1:
                        msg += "s"
                    msg += f" to go [Q"
                    msg += strReadyQueue(readyQueue)
                    print(msg)
            if not recalculated and time >= completionTime and finished:
                recalculated = True
                alpha = params.alpha
                currentProcess.tau = math.ceil( (alpha * currentProcess.burst_time[current_burst_num - 1]) + ((1 - alpha) * tau))
                #print(currentProcess.tau)
                tau = currentProcess.tau
                currentProcess.originalTau = tau
                msg = f"time {time}ms: Recalculated tau = {tau}ms for process {name} [Q"
                msg += strReadyQueue(readyQueue)
                print(msg)
            if not switched and time >= completionTime and recalculated:
                switched = True
                currentProcess.blocked_IO = int(currentProcess.IO_burst[current_burst_num - 1] + params.t_cs / 2 + time)
                ioQueue.append(currentProcess)
                msg = f"time {time}ms: Process {name} switching out of CPU; will block on"
                msg += f" I/O until time {int(currentProcess.blocked_IO)}ms [Q"
                msg += strReadyQueue(readyQueue)
                switchedOutTime = time + params.t_cs
                print(msg)
                currentProcess = None
            if not switchedOut and time >= completionTime and switched:
                switchedOut = True
                switchedOutTime = completionTime + params.t_cs / 2

        # Any completed IO?

        if len(ioQueue) > 0:
            ioQueueTmp = sorted(ioQueue, key=lambda x: x.name) # sort by name, so tie breaker
            for i in ioQueueTmp:
                # print(i.name + " " + str(i.blocked_IO))
                if time >= i.blocked_IO:
                    msg = f"time {time}ms: Process {i.name} (tau {int(i.tau)}ms) completed I/O; added"
                    msg += f" to ready queue [Q"
                    ioQueue.pop(ioQueue.index(i))
                    readyQueue.append(i)
                    i.run_time = time + params.t_cs / 2
                    msg1 = strReadyQueue(readyQueue)
                    msg += msg1

                    # Now check for preemption
                    if started and not finished and currentProcess != None: # if it already started finishing, don't preempt
                        # print(i.name + str(i.tau))
                        # print(currentProcess.name + str(currentProcess.originalTau - (time - startTime)))
                        if i.originalTau < currentProcess.originalTau - (time - startTime):
                            currentProcess.originalTau = currentProcess.originalTau - (time - startTime)
                            msg = f"time {time}ms: Process {i.name} (tau {int(i.tau)}ms) completed I/O;"
                            msg += f" preempting {currentProcess.name} [Q"
                            #readyQueue.append(currentProcess)
                            toBeAdded.append(currentProcess)
                            currentProcess.run_time = time + params.t_cs / 2

                            currentProcess = i
                            # reset
                            started = False
                            finished = False
                            recalculated = False
                            switched = False
                            switchedOut = False

                            #readyQueue.remove(i)
                            i.remove = True

                            i.run_time += params.t_cs / 2 # switch out current Process, switching in is already added

                            msg += msg1
                    print(msg)

        # Any arriving processes?
        if len(ordered) > 0:
            orderedTmp = ordered
            for i in orderedTmp:
                if i.arrival_time == time:
                    readyQueue.append(i)
                    msg = f"time {time}ms: Process {i.name} (tau {int(i.tau)}ms) arrived; added to "
                    msg += f"ready queue [Q"
                    msg += strReadyQueue(readyQueue)
                    print(msg)
                    i.run_time = time + params.t_cs / 2
                    ordered.pop(ordered.index(i))

        # Is current Process none?
        if currentProcess == None and time >= switchedOutTime:
            # if there is something, add
            if len(readyQueue) > 0:
                readyQueue = sorted(readyQueue, key=lambda x: x.originalTau) # sort first
                currentProcess = readyQueue[0]
                # If a process has the same tau but comes first alphabetically, take it
                for p in processes:
                    if not (p in readyQueue):
                        continue
                    if p.tau == currentProcess.tau and p.name < currentProcess.name:
                        currentProcess = p
                index = readyQueue.index(currentProcess)
                readyQueue.pop(index)
                started = False
                finished = False
                recalculated = False
                switched = False
                switchedOut = False
                currentProcess.run_time = time + params.t_cs / 2
        time += 1

    msg = f"time {time}ms: Simulator ended for srt [Q <empty>]"
    print(msg)

# Order by tau then by name
def order(queue):
    queue = sorted(queue, key=lambda x: x.originalTau)
    orderKeys = dict()
    for i in queue:
        orderKeys[i.originalTau] = i
    orderKeys = sorted(orderKeys)
    queue = sorted(queue, key=lambda x: x.name)
    current = []
    final = []
    for i in orderKeys:
        for j in queue:
            if j.originalTau == i:
                current.append(j)
        final = final + current
        current.clear()
    return final
        

def strReadyQueue(readyQueue):
    msg = ""
    if len(readyQueue) == 0:
        return " <empty>]"
    else:
        for i in order(readyQueue):
            msg += " " + i.name
        msg += "]"
    return msg

def print_start(processes):
    for i in processes:
        if i.num_burst == 1:
            print(
            f"Process {i.name} [NEW] (arrival time {i.arrival_time} ms) {i.num_burst} CPU burst (tau {int(i.tau)}ms)"
        )
        else:
            print(
                f"Process {i.name} [NEW] (arrival time {i.arrival_time} ms) {i.num_burst} CPU bursts (tau {int(i.tau)}ms)"
            )
    temp_queue = []
    for i in sorted(processes, key=lambda x: x.arrival_time):
        if i.arrival_time == 0:
            temp_queue.append(i)
    queue_string = "<empty>"
    if temp_queue:
        queue_string = " ".join([i.name for i in temp_queue])
    print(f"time 0ms: Simulator started for SRT [Q <empty>]")


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

        # n=2,
        # seed=2,
        # lam=0.01,
        # upper_bound=256,
        # t_cs=4,
        # alpha=0.5,
        # t_slice=128,
        # rr_add="END",

        n=16,
        seed=2,
        lam=0.01,
        upper_bound=256,
        t_cs=4,
        alpha=0.75,
        t_slice=64,
        rr_add="END",

        # n=8,
        # seed=64,
        # lam=0.001,
        # upper_bound=4096,
        # t_cs=4,
        # alpha=0.5,
        # t_slice=2048,
        # rr_add="END",
    )
    processes = []
    ran = Rand48(params.seed)
    ran.srand(params.seed)
    for i in range(params.n):
        processes.append(Process(chr(i + 65), params, ran))

    print_start(processes)
    srt(processes, params)
