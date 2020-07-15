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
        "preemptions": 0
    }
    
    for i in processes:
        print(i)

    for i in processes:
        print(f"Process {i.name} [NEW] (arrival time {i.arrival_time} ms) {i.num_burst} CPU bursts")

    # Re-sort by set of processes by arrival time
    ordered = sorted(processes, key=lambda x: x.arrival_time)
    a_times = [[i.arrival_time, i] for i in processes]
    queue = []
    for i in ordered:
        if i.arrival_time == 0:
            # TODO: deal with ties?
            queue.append(i)
            ordered.remove(i)
    
    time = 0
    queue_string = '<empty>' 
    if queue:
        queue_string = ' '.join([i.name for i in queue])
    print(f'time {time}ms: Simulator started for RR [Q {queue_string}]') if not FCFS else print(f'time {time}ms: Simulator started for FCFS [Q {queue_string}]')
    blocking = []
    while len(ordered) != 0:
        if not cpu.current_process:
            if len(queue) != 0:
                #print(cpu)
                if cpu.context_switch == cpu.context_switch_total and not cpu.switching:
                    cpu.context_switch = cpu.context_switch_remove - 1
                elif cpu.context_switch != 1:
                    cpu.context_switch -= 1
                elif cpu.context_switch == 1:
                    cpu.switching = False
                    cpu.context_switch = cpu.context_switch_total
                    process = queue.pop(0)
                    cpu.current_process = process
                    queue_string = '<empty>' if len(queue) == 0 else ' '.join([i.name for i in queue])
                    print(f'time {time}ms: Process {process.name} started using the CPU for {process.burst_time[0]}ms burst [Q {queue_string}]')
        else:
            if cpu.current_process.run_time == cpu.current_process.burst_time[0] - 1:
                cpu.current_process.burst_time.pop(0)
                queue_string = '<empty>' if len(queue) == 0 else ' '.join([i.name for i in queue])
                if len(cpu.current_process.burst_time) == 0:
                    print(f'time {time}ms: Process {cpu.current_process.name} terminated [Q {queue_string}]')
                    ordered.remove(cpu.current_process)
                else:
                    if (len(cpu.current_process.burst_time)) == 1:
                        print(f'time {time}ms: Process {cpu.current_process.name} completed a CPU burst; {len(cpu.current_process.burst_time)} burst to go [Q {queue_string}]')
                    else:   
                        print(f'time {time}ms: Process {cpu.current_process.name} completed a CPU burst; {len(cpu.current_process.burst_time)} bursts to go [Q {queue_string}]')
                    b_time = time+cpu.current_process.IO_burst[0]+cpu.context_switch_remove
                    print(f'time {time}ms: Process {cpu.current_process.name} switching out of CPU; will block on I/O until time {b_time}ms [Q {queue_string}]')
                    cpu.current_process.block_time = b_time - time
                    blocking.append(cpu.current_process)
                    cpu.current_process.run_time = 0
                    cpu.current_process.sliced = 0
                if cpu.context_switch == cpu.context_switch_total and len(queue) != 0:
                    cpu.context_switch = cpu.context_switch_total
                    cpu.switching = True
                cpu.current_process = None
            elif cpu.current_process.run_time + 1 >= time_slice and cpu.current_process.sliced == 0:
                queue_string = '<empty>' if len(queue) == 0 else ' '.join([i.name for i in queue])
                if len(queue) == 0:
                    # This will probably break if the ready queue is filled while this is going on
                    print(f'time {time}ms: Time slice expired; no preemption because ready queue is empty [Q {queue_string}]')
                    cpu.current_process.run_time += 1
                    cpu.current_process.sliced = 1
                else:
                    # Might need something here
                    pass
            else:
                cpu.current_process.run_time += 1

        if len(blocking) != 0:
            removes = []
            for i in range(len(blocking)):
                if blocking[i].block_time == 0: 
                    removes.append(i)
                blocking[i].block_time -= 1
        
            for i in removes:
                p = blocking[i]
                if add_end:
                    queue.append(p)
                else:
                    queue.insert(0, p)
                p.IO_burst.pop(0)
                del blocking[i]
                queue_string = '<empty>' if len(queue) == 0 else ' '.join([k.name for k in queue])
                print(f'time {time}ms: Process {p.name} completed I/O; added to ready queue [Q {queue_string}]')

        if len(a_times) != 0:
            if time == a_times[0][0]:
                p = a_times.pop(0)[1]
                if add_end:
                    queue.append(p)
                else:
                    queue.insert(0, p)
                q = ' '.join([i.name for i in queue])
                print(f'time {time}ms: Process {p.name} arrived; added to ready queue [Q {q}]')
        else:
            pass

        time += 1
        #if time > 400:
        #    break
    print(f'time {time+1}ms: Simulator ended for RR [Q <empty>]') if not FCFS else print(f'time {time+1}ms: Simulator ended for FCFS [Q <empty>]')

    
