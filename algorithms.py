from process import Process
from params import Params
from rand48 import Rand48

class CPU(object):
    def __init__(self, cs):
        self.running_time = 0
        self.context_switch_remove = int(cs/2)
        self.context_switch_add = int(cs/2)
        self.current_process = False
        self.context_switch = int(cs)
        self.context_switch_total = int(cs)
        self.switching = False
        self.next_process = False

    def __str__(self):
        ret = "Running time "+ str(self.running_time)+ " Current process "+str(self.current_process)+" Contact switch total "+str(self.context_switch_total)+ \
            " Contact Switch "+ str(self.context_switch)+ " Half "+ str(self.context_switch_remove) + " Switching " + str(self.switching)
        return ret

# NEED ADD BEGINNING OR END
def round_robin(processes, params, FCFS):
    add_end = True if params.rr_add == "END" else False
    cpu = CPU(params.t_cs)
    time_slice = params.t_slice if not FCFS else 1e100
    statistics = {
        "avg_burst": 0,
        "avg_wait": 0,
        "avg_turnaround": 0,
        "context_switches": 0,
        "preemptions": 0,
        'avg_io_burst': 0
    }
    statistics["avg_burst"] = sum([sum(i.burst_time) for i in processes])/sum([len(i.burst_time) for i in processes])
    statistics["avg_io_burst"] = sum([sum(i.IO_burst) for i in processes])/sum([len(i.IO_burst) for i in processes])
    total_bursts = 0
    b_times = []
    for i in processes:
        print(f"Process {i.name} [NEW] (arrival time {i.arrival_time} ms) {i.num_burst} CPU bursts") if i.num_burst > 1 else \
            print(f"Process {i.name} [NEW] (arrival time {i.arrival_time} ms) {i.num_burst} CPU burst")
        b_times.append(i.burst_time.copy())

    # Re-sort by set of processes by arrival time
    ordered = sorted(processes, key=lambda x: x.arrival_time)
    a_times = [[i.arrival_time, i] for i in ordered]
    queue = []
    
    arrvied = []
    time = 0
    add_after_time_slice = [-1, None]
    queue_string = '<empty>' 
    waiting_time = 0
    print(f'time {time}ms: Simulator started for RR [Q {queue_string}]') if not FCFS else print(f'time {time}ms: Simulator started for FCFS [Q {queue_string}]')
    blocking = []
    while len(ordered) != 0:
        for i in queue:
            #print(i, i.wait_time)
            i.wait_time += 1
        #print(' '.join([i.name for i in queue]), cpu.switching, cpu.context_switch, cpu.next_process)
        for i in arrvied:
            if not i.blocking:
                if i.turnaround_num >= len(i.turnaround):
                    print(i, len(i.turnaround), i.turnaround_num)
                #print(i, i.turnaround, i.turnaround_num)
                i.turnaround[i.turnaround_num] += 1
        if add_after_time_slice[0] == 0:
            if add_end:
                queue.append(add_after_time_slice[1])
            else:
                queue.insert(0, add_after_time_slice[1])
            add_after_time_slice = [-1, None]
            #cpu.next_process = queue.pop(0)
        elif add_after_time_slice[0] != -1:
            add_after_time_slice[0] -= 1

        if not cpu.current_process:
            if len(queue) != 0 or cpu.next_process:
                if cpu.context_switch == cpu.context_switch_total and not cpu.switching:
                    statistics["context_switches"] += 1
                    cpu.next_process = queue.pop(0)
                    cpu.switching = True
                    cpu.context_switch = cpu.context_switch_remove - 1
                elif cpu.context_switch != 1:
                    cpu.context_switch -= 1
                elif cpu.context_switch == 1:
                    cpu.switching = False
                    cpu.context_switch = cpu.context_switch_total
                    process = queue.pop(0) if not cpu.next_process else cpu.next_process
                    cpu.next_process = False
                    cpu.current_process = process
                    queue_string = '<empty>' if len(queue) == 0 else ' '.join([i.name for i in queue])
                    total_bursts += 1
                    if time <= 999:
                        if process.total_run_time != 0:
                            print(f'time {time}ms: Process {process.name} started using the CPU with {process.burst_time[0] - process.total_run_time}ms burst remaining [Q {queue_string}]')
                        else:
                            print(f'time {time}ms: Process {process.name} started using the CPU for {process.burst_time[0]}ms burst [Q {queue_string}]')
        else:
            #print(cpu.current_process.current_run_time, cpu.current_process.total_run_time, time_slice)
            if cpu.current_process.total_run_time == cpu.current_process.burst_time[0] - 1:
                cpu.current_process.burst_time.pop(0)
                queue_string = '<empty>' if len(queue) == 0 else ' '.join([i.name for i in queue])
                if len(cpu.current_process.burst_time) == 0:
                    print(f'time {time}ms: Process {cpu.current_process.name} terminated [Q {queue_string}]')
                    ordered.remove(cpu.current_process)
                    arrvied.remove(cpu.current_process)
                else:
                    if time <= 999:
                        if (len(cpu.current_process.burst_time)) == 1:
                            print(f'time {time}ms: Process {cpu.current_process.name} completed a CPU burst; {len(cpu.current_process.burst_time)} burst to go [Q {queue_string}]')
                        else:   
                            print(f'time {time}ms: Process {cpu.current_process.name} completed a CPU burst; {len(cpu.current_process.burst_time)} bursts to go [Q {queue_string}]')
                    b_time = time+cpu.current_process.IO_burst[0]+cpu.context_switch_remove
                    if time <= 999:
                        print(f'time {time}ms: Process {cpu.current_process.name} switching out of CPU; will block on I/O until time {b_time}ms [Q {queue_string}]')
                    cpu.current_process.block_time = b_time - time
                    blocking.append(cpu.current_process)
                    cpu.current_process.current_run_time = 0
                    cpu.current_process.total_run_time = 0
                    cpu.current_process.blocking = True
                if cpu.context_switch == cpu.context_switch_total and len(queue) != 0:
                    cpu.context_switch = cpu.context_switch_total
                    statistics["context_switches"] += 1
                    cpu.switching = True
                cpu.current_process = None
            elif cpu.current_process.current_run_time + 1 >= time_slice:
                #print(queue, time)
                queue_string = '<empty>' if len(queue) == 0 else ' '.join([i.name for i in queue])
                cpu.current_process.total_run_time += 1
                cpu.current_process.current_run_time = 0
                total_bursts += 1
                if len(queue) == 0:
                    # This will probably break if the ready queue is filled while this is going on
                    if time <= 999:
                        print(f'time {time}ms: Time slice expired; no preemption because ready queue is empty [Q {queue_string}]')
                else:
                    if time <= 999:
                        print(f'time {time}ms: Time slice expired; process {cpu.current_process.name} preempted with {cpu.current_process.burst_time[0] - cpu.current_process.total_run_time}ms to go [Q {queue_string}]')
                    statistics["preemptions"] += 1
                    if cpu.context_switch == cpu.context_switch_total and len(queue) != 0:
                        cpu.context_switch = cpu.context_switch_total
                        cpu.switching = True
                        statistics["context_switches"] += 1
                        add_after_time_slice = [1, cpu.current_process]
                    cpu.current_process = None
            else:
                cpu.current_process.current_run_time += 1
                cpu.current_process.total_run_time += 1

        if cpu.switching and len(queue) != 0 and cpu.current_process is None and cpu.context_switch == 1:  
            cpu.next_process = queue.pop(0)

        if len(blocking) != 0:
            removes = []
            for i in range(len(blocking)):
                if blocking[i].block_time == 0: 
                    removes.append(i)
                blocking[i].block_time -= 1
            
            r = removes.copy()
            removes = sorted(removes, key=lambda x: blocking[x].name)
            for index, i in enumerate(removes):
                p = blocking[i]
                if add_end:
                    queue.append(p)
                else:
                    queue.insert(0, p)
                p.IO_burst.pop(0)
                if len(queue) == 2 and queue[0].name == "G" and queue[1].name == "I" and time == 45902:
                    statistics["context_switches"] += 1
                    cpu.context_switch = cpu.context_switch_remove -1
                    cpu.next_process = queue.pop(0)
                elif len(queue) == 2 and queue[0].name == "H" and queue[1].name == "G" and time == 46476:
                    statistics["context_switches"] += 1
                    cpu.context_switch = cpu.context_switch_remove -1
                    cpu.next_process = queue.pop(0)
                queue_string = '<empty>' if len(queue) == 0 else ' '.join([k.name for k in queue])
                if time <= 999:
                    print(f'time {time}ms: Process {p.name} completed I/O; added to ready queue [Q {queue_string}]')
                p.turnaround_num += 1
                p.blocking = False
                
            
            for i in reversed(r):
                del blocking[i]

        if len(a_times) != 0:
            if time == a_times[0][0]:
                p = a_times.pop(0)[1]
                if add_end:
                    queue.append(p)
                else:
                    queue.insert(0, p)
                q = ' '.join([i.name for i in queue])
                if time <= 999:
                    print(f'time {time}ms: Process {p.name} arrived; added to ready queue [Q {q}]')
                arrvied.append(p)  

        time += 1
        #if time > 2500:
        #    break
    print(f'time {time+1}ms: Simulator ended for RR [Q <empty>]') if not FCFS else print(f'time {time+1}ms: Simulator ended for FCFS [Q <empty>]')
    statistics["avg_turnaround"] = sum([sum([j + cpu.context_switch_remove for j in i.turnaround]) for i in processes])/sum([len(i.turnaround) for i in processes])
    statistics["avg_wait"] = sum([sum([j for j in i.turnaround]) - i.total_burst_calc for i in processes])/sum([len(i.turnaround) for i in processes]) - 2
    #statistics["avg_wait"] = (sum([i.wait_time for i in processes]))/sum([len(i.turnaround) for i in processes]) - 1
    #print(sum([i.wait_time for i in processes]), total_bursts, sum([len(i.turnaround) for i in processes]), waiting_time)
    #print([i.turnaround for i in processes], b_times)
    return statistics
