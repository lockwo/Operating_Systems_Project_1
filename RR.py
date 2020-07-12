from process import Process
from p1 import Params
from rand48 import Rand48



def round_robin(processes, time_slice, cs_time):
    statistics = {
        avg_burst: 0,
        avg_wait: 0,
        avg_turnaround: 0,
        context_switches: 0,
        preemptions: 0
    }
    
    for i in processes:
        print(f"Process {i.name} [NEW] (arrival time {i.arrival_time} ms) {i.num_burst} CPU Bursts")

    # Re-sort by set of processes by arrival time
    ordered = sorted(processes, key=lambda x: x.arrival_time)
    queue = []
    for i in ordered:
        if i.arrival_time == 0:
            queue.append(i)
            ordered.remove(i)
    
    time = 0
    queue_string = '<empty>'
    if queue:
        queue_string = ' '.join([i.name for i in queue])
    print(f'time {time}ms: Simulator started for FCFS [Q {queue_string}]')
    while ordered:
        if queue:
            process = queue.pop(0)
            time += process.arrival_time

            print(f'time {time}ms: Process {process.name} started using the CPU for {process.burst_time}')

if __name__ == '__main__':
    params = Params(n=1, seed=2, lam=0.01, upper_bound=256, t_cs=4, alpha=0.5, t_slice=128, rr_add='test')
    processes = []
    ran = Rand48(params.seed)
    ran.srand(params.seed)
    for i in range(params.n):
        processes.append(Process(chr(i + 65), params, ran))