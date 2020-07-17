import sys
from process import Process
from rand48 import Rand48
from print_sim import end
from params import Params
from algorithms import round_robin
from srt1 import srt
from sjf import sjf

if __name__ == '__main__':
    '''
    if len(sys.argv) == 9:
        params = Params(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8])
    else:
        params = Params(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], "END")
    '''
    # TEST 2
    params = Params(
        n=1,
        seed=2,
        lam=0.01,
        upper_bound=256,
        t_cs=4,
        alpha=0.5,
        t_slice=128,
        rr_add="END"
    )
    # TEST 3
    # params = Params(
    #     n=2,
    #     seed=2,
    #     lam=0.01,
    #     upper_bound=256,
    #     t_cs=4,
    #     alpha=0.5,
    #     t_slice=128,
    #     rr_add="END"
    # )

    # TEST 4
    # params = Params(
    #     n=16,
    #     seed=2,
    #     lam=0.01,
    #     upper_bound=256,
    #     t_cs=4,
    #     alpha=0.75,
    #     t_slice=64,
    #     rr_add="END"
    # )

    # TEST 5
    # params = Params(
    #     n=8,
    #     seed=64,
    #     lam=0.001,
    #     upper_bound=4096,
    #     t_cs=4,
    #     alpha=0.5,
    #     t_slice=2048,
    #     rr_add="END",
    # )

    '''
    First Come First Served (FCFS)
    '''
    processes = []
    ran = Rand48(params.seed)
    ran.srand(params.seed)
    for i in range(params.n):
        processes.append(Process(chr(i + 65), params, ran))

    fcfs_stats = round_robin(processes=processes, params=params, FCFS=True)

    '''
    Shortest Job First (SJF)
    '''
    processes = []
    ran = Rand48(params.seed)
    ran.srand(params.seed)
    for i in range(params.n):
        processes.append(Process(chr(i + 65), params, ran))

    sjf_stats = sjf(processes=processes, params=params)

    '''
    Shortest Remaining Time (SRT)
    '''
    processes = []
    ran = Rand48(params.seed)
    ran.srand(params.seed)
    for i in range(params.n):
        processes.append(Process(chr(i + 65), params, ran))

    srt_stats = srt(processes=processes, params=params)

    '''
    Round Robin (RR)
    '''
    processes = []
    ran = Rand48(params.seed)
    ran.srand(params.seed)
    for i in range(params.n):
        processes.append(Process(chr(i + 65), params, ran))

    rr_stats = round_robin(processes=processes, params=params, FCFS=False)

    end(fcfs=fcfs_stats, sjf=sjf_stats, srt=srt_stats, rr=rr_stats)
