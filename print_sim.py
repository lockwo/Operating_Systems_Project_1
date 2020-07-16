def end(fcfs: dict = None, sjf: dict = None, srt: dict = None, rr: dict = None):
    with open('simout.txt', 'w') as stats:
        stats.write("Algorithm FCFS\n")
        stats.write(f"-- average CPU burst time: {fcfs['avg_burst']:.3f} ms\n")
        stats.write(f"-- average wait time: {fcfs['avg_wait']:.3f} ms\n")
        stats.write(f"-- average turnaround time: {fcfs['avg_turnaround']:.3f} ms\n")
        stats.write(f"-- total number of context switches: {fcfs['context_switches']}\n")
        stats.write(f"-- total number of preemptions: {fcfs['preemptions']}\n")
        stats.write("Algorithm SJF\n")
        stats.write(f"-- average CPU burst time: {sjf['avg_burst']:.3f} ms\n")
        stats.write(f"-- average wait time: {sjf['avg_wait']:.3f} ms\n")
        stats.write(f"-- average turnaround time: {sjf['avg_turnaround']:.3f} ms\n")
        stats.write(f"-- total number of context switches: {sjf['context_switches']}\n")
        stats.write(f"-- total number of preemptions: {sjf['preemptions']}\n")
        stats.write("Algorithm SRT\n")
        stats.write(f"-- average CPU burst time: {srt['avg_burst']:.3f} ms\n")
        stats.write(f"-- average wait time: {srt['avg_wait']:.3f} ms\n")
        stats.write(f"-- average turnaround time: {srt['avg_turnaround']:.3f} ms\n")
        stats.write(f"-- total number of context switches: {srt['context_switches']}\n")
        stats.write(f"-- total number of preemptions: {srt['preemptions']}\n")
        stats.write("Algorithm RR\n")
        stats.write(f"-- average CPU burst time: {rr['avg_burst']:.3f} ms\n")
        stats.write(f"-- average wait time: {rr['avg_wait']:.3f} ms\n")
        stats.write(f"-- average turnaround time: {rr['avg_turnaround']:.3f} ms\n")
        stats.write(f"-- total number of context switches: {rr['context_switches']}\n")
        stats.write(f"-- total number of preemptions: {rr['preemptions']}\n")
