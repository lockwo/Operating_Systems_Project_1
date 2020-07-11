

def p_sim(time, processes, Q, params, algo):
    if time == 0:
        for i in processes:
            if algo == "FCFS" or algo == "RR":
                print("Process", i.name, "[NEW] (arrival time", i.arrival_time, "ms)", i.num_burst, "CPU Bursts")
            if algo == "SJF" or algo == "SRT":
                print("Process", i.name, "[NEW] (arrival time", i.arrival_time, "ms)", i.num_burst, "CPU Bursts (tau ", str(i.tau) + "ms)")
        if len(Q) == 0:
            print("time 0ms: Simulator started for", algo, "[Q <empty>]")
        else:
             print("time 0ms: Simulator started for", algo, "[Q", ' '.join([i.name for i in Q]) + "]")
    
