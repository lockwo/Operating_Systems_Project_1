from process import Process
from p1 import Params
from rand48 import Rand48

def queue_str(queue):
    if not queue:
        return '<empty>'
    queue_string = ''
    for i in range(len(queue)):
        if i == len(queue)-1:
            queue_string += queue[i].name
        else:
            queue_string += f'{queue[i].name} '
    return queue_string

def round_robin(processes, time_slice, cs_time):
    statistics = {
        'avg_burst': 0,
        'avg_wait': 0,
        'avg_turnaround': 0,
        'context_switches': 0,
        'preemptions': 0
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
    current = None
    start_time = 0
    finish_time = 0
    while True:
        # Check for arriving processes
        if len(ordered) > 0 and time == ordered[0].arrival_time:
            if not current:
                current = ordered.pop(0)
                # TODO: need to deal with different context switch time... half for bringing process out, half for bringing process in
                if start_time == 0:
                    start_time = time + cs_time/2
                else:
                    start_time = time + cs_time
                print('start time:', start_time, '  time:', time)
                process = current
                print(time, current)
            else:
                process = ordered.pop(0)
            queue.append(process)
            print(f'time {time}ms: Process {process.name} arrived; added to ready queue [Q {queue_str(queue)}]')
        if current and start_time == time:
            queue.pop(0)
            print(f'time {time}ms: Process {current.name} started using the CPU for {current.burst_time[current.current_burst_num]}ms [Q {queue_str(queue)}]')
            finish_time = time + current.burst_time[current.current_burst_num]
            break


        time += 1
        




if __name__ == '__main__':
    params = Params(n=1, seed=2, lam=0.01, upper_bound=256, t_cs=4, alpha=0.5, t_slice=128, rr_add='test')
    processes = []
    ran = Rand48(params.seed)
    ran.srand(params.seed)
    for i in range(params.n):
        processes.append(Process(chr(i + 65), params, ran))
    round_robin(processes, params.t_slice, params.t_cs)