# import p1
from rand48 import Rand48
from process import Process
from params import Params
import print_sim
import math


def sjf(processes, params):
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

    while (len(ordered) != 0 or currentProcess != None or len(readyQueue) != 0 or len(ioQueue) != 0 or time < switchedOutTime):
        # If there is a current process running
        if currentProcess != None and time >= switchedOutTime + params.t_cs / 2:
            name = currentProcess.name
            tau = int(currentProcess.tau)
            current_burst_num = currentProcess.current_burst_num
            arrival_time = int(currentProcess.arrival_time)
            if not started and time >= arrival_time + params.t_cs / 2 and time >= currentProcess.run_time:
                startTime = time
                started = True
                msg = f"time {time}ms: Process {name} (tau {tau}ms) started using the CPU"
                msg += f" for {currentProcess.burst_time[current_burst_num]}ms burst [Q"
                msg += strReadyQueue(readyQueue)
                print(msg)
            completionTime = currentProcess.burst_time[current_burst_num] + startTime
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
                currentProcess.tau = normal_round( (alpha * currentProcess.burst_time[current_burst_num - 1]) + ((1 - alpha) * tau) )
                tau = currentProcess.tau
                msg = f"time {time}ms: Recalculated tau = {tau}ms for process {name} [Q"
                msg += strReadyQueue(readyQueue)
                print(msg)
            if not switched and time >= completionTime and recalculated:
                switched = True
                currentProcess.blocked_IO = currentProcess.IO_burst[current_burst_num - 1] + params.t_cs / 2 + time
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
            ioQueue = sorted(ioQueue, key=lambda x: x.name) # sort by name, so tie breaker
            for i in ioQueue:

                if time >= i.blocked_IO:
                    msg = f"time {time}ms: Process {i.name} (tau {int(i.tau)}ms) completed I/O; added"
                    msg += f" to ready queue [Q"
                    ioQueue.pop(ioQueue.index(i))
                    readyQueue.append(i)
                    i.run_time = time + params.t_cs / 2
                    msg += strReadyQueue(readyQueue)
                    print(msg)
                    

        # Any arriving processes?
        if len(ordered) > 0:
            for i in ordered:
                if i.arrival_time == time:
                    readyQueue.append(i)
                    msg = f"time {time}ms: Process {i.name} (tau {int(i.tau)}ms) arrived; added to "
                    msg += f"ready queue [Q"
                    msg += strReadyQueue(readyQueue)
                    print(msg)
                    i.run_time = time + params.t_cs / 2
                    ordered.pop(ordered.index(i))

        # Is current Process none?
        if currentProcess == None:
            # if there is something, add
            if len(readyQueue) > 0:
                readyQueue = sorted(readyQueue, key=lambda x: x.tau) # sort first
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

    msg = f"time {time}ms: Simulator ended for SJF [Q <empty>]"
    print(msg)

def strReadyQueue(readyQueue):
    if len(readyQueue) == 0:
        return " <empty>]"
    readyQueue = sorted(readyQueue, key=lambda x: x.tau)
    msg = ""
    currentValue = readyQueue[0].tau
    queue = []
    for p in readyQueue:
        if p.tau == currentValue:
            queue.append(p)
        else:
            currentValue = p.tau
            queue = sorted(queue, key=lambda x: x.name)
            for i in queue:
                msg += " " + str(i.name)
            queue.clear()
            queue.append(p)
    for j in queue:
        msg += " " + str(j.name)
    msg += "]"
    return msg
        


def print_start(processes):
    for i in processes:
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
    print(f"time 0ms: Simulator started for SJF [Q <empty>]")


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
    )
    processes = []
    ran = Rand48(params.seed)
    ran.srand(params.seed)
    for i in range(params.n):
        processes.append(Process(chr(i + 65), params, ran))

    print_start(processes)
    sjf(processes, params)
