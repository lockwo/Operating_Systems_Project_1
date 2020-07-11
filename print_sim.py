
def p_sim(time, processes, Q, params, algo):
    if time == 0:
        for i in processes:
            if algo == "FCFS":
                print("Process", i.name, "[NEW] (arrival time", i.arrival_time, "ms)", i.num_burst, "CPU Bursts")
        if len(Q) == 0:
            print("time 0ms: Simulator started for", algo, "[Q <empty>]")
        else:
             print("time 0ms: Simulator started for", algo, "[Q", ' '.join([i.name for i in Q]) + "]")
    
