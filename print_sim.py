

def p_sim(time, processes, Q, params, algo):
    if time == 0:
        for i in processes:
            if algo == "FCFS" or algo == "RR":
                print("Process", i.name, "[NEW] (arrival time", i.arrival_time, "ms)", i.num_burst, "CPU Bursts")
            if algo == "SJF" or algo == "SRT":
                print("Process", i.name, "[NEW] (arrival time", i.arrival_time, "ms)", i.num_burst, "CPU Bursts (tau", str(i.tau) + "ms)")
        if len(Q) == 0:
            print("time 0ms: Simulator started for", algo, "[Q <empty>]")
        else:
             print("time 0ms: Simulator started for", algo, "[Q", ' '.join([i.name for i in Q]) + "]")

def end(fcfs, sjf, srt, rr):
    print("Algorithm FCFS")
    print("-- average CPU burst time:", fcfs[0], "ms")
    print("-- average wait time:", fcfs[1], "ms")
    print("-- average turnaround time:", fcfs[2], "ms")
    print("-- total number of context switches:", fcfs[3])
    print("-- total number of preemptions:", fcfs[4])
    print("Algorithm SJF")
    print("-- average CPU burst time:", sjf[0], "ms")
    print("-- average wait time:", sjf[1], "ms")
    print("-- average turnaround time:", sjf[2], "ms")
    print("-- total number of context switches:", sjf[3])
    print("-- total number of preemptions:", sjf[4])
    print("Algorithm SRT")
    print("-- average CPU burst time:", srt[0], "ms")
    print("-- average wait time:", srt[1], "ms")
    print("-- average turnaround time:", srt[2], "ms")
    print("-- total number of context switches:", srt[3])
    print("-- total number of preemptions:", srt[4])
    print("Algorithm RR")
    print("-- average CPU burst time:", rr[0], "ms")
    print("-- average wait time:", rr[1], "ms")
    print("-- average turnaround time:", rr[2], "ms")
    print("-- total number of context switches:", rr[3])
    print("-- total number of preemptions:", rr[4])
    
