from math import log, floor, ceil


class Process(object):
    def __init__(self, name, params, r):
        self.name = name
        self.arrival_time = int(self.activation(r, params.lam, params.upper_bound))
        self.num_burst = floor(r.drand() * 100 + 1)
        self.current_burst_num = 0
        self.blocked_IO = 0  # represents blocked untils...
        self.burst_time = []
        self.startTime = []
        self.endTime = []
        self.IO_burst = []
        for i in range(self.num_burst):
            self.burst_time.append(
                ceil(self.activation(r, params.lam, params.upper_bound))
            )
            if i != self.num_burst-1:
                self.IO_burst.append(
                    ceil(self.activation(r, params.lam, params.upper_bound))
            )
            self.startTime.append(0)
            self.endTime.append(0)

        self.status = 2  # 0 = running, 1 = ready, 2 = waiting
        self.run_time = 0
        self.total_run_time = 0
        self.current_run_time = 0
        self.block_time = -1
        self.tau = 1 / params.lam
        self.done = False
        self.turnaround = [0 for i in self.burst_time]
        self.turnaround_num = 0
        self.blocking = False
        self.wait_time = 0
        self.start_wait = 0
        self.originalTime = 0
        self.originalTau = 1 / params.lam	
        self.avg_burst_calc = sum(self.burst_time)/len(self.burst_time)
        self.total_burst_calc = sum(self.burst_time)

    def activation(self, r, lam, ub):
        while 1:
            test = -log(r.drand()) / lam
            if test < ub:
                return test

    def __repr__(self):
        return f'Process {self.name}, Arrival time={self.arrival_time}, Num_bursts={self.num_burst}, Current_burst_num={self.current_burst_num}, \
            Blocked_IO={self.blocked_IO}, tau={self.tau}'

    def __str__(self):
        ret = (
            self.name
            + ", arrival time, "
            + str(self.arrival_time)
            + ", number of bursts, "
            + str(self.num_burst)
            + ", CPU bursts, "
            + str(self.burst_time)
            + ", I/O bursts, "
            + str(self.IO_burst)
            + ", status, "
            + str(self.status)
        )
        return ret
