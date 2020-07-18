from __future__ import print_function
import sys
from process import Process
from rand48 import Rand48
from print_sim import end
from params import Params
from algorithms import round_robin
from srt1 import srt
from sjf import sjf


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def check_args():
    try:
        if not isinstance(int(sys.argv[1]), int) or (int(sys.argv[1]) < 0 or int(sys.argv[1]) > 26):
            print(f'ERROR: <{sys.argv[1]} isn\'t a valid n value>', file=sys.stderr)
            sys.exit()
        if not isinstance(int(sys.argv[2]), int):
            print(f'ERROR: <{sys.argv[2]} isn\'t a valid seed>', file=sys.stderr)
            sys.exit()
        if not isinstance(float(sys.argv[3]), float) or (float(sys.argv[3]) <= 0 or float(sys.argv[3]) > 1):
            print(f'ERROR: <{sys.argv[3]} isn\'t a valid lambda value>', file=sys.stderr)
            sys.exit()
        if not isinstance(int(sys.argv[4]), int) or int(sys.argv[4]) < 0:
            print(f'ERROR: <{sys.argv[4]} isn\'t a valid upper bound>', file=sys.stderr)
            sys.exit()
        if not isinstance(int(sys.argv[5]), int) and int(sys.argv[5]) % 2 != 0:
            print(f'ERROR: <{sys.argv[5]} isn\'t a valid context switch>', file=sys.stderr)
            sys.exit()
        if not isinstance(float(sys.argv[6]), float):
            print(f'ERROR: <{sys.argv[6]} isn\'t a valid alpha>', file=sys.stderr)
            sys.exit()
        if not isinstance(int(sys.argv[7]), int):
            print(f'ERROR: <{sys.argv[7]} isn\'t a valid time slice>', file=sys.stderr)
            sys.exit()
    except ValueError as e:
        print(f'ERROR: <{e}>', file=sys.stderr)
        sys.exit()

if __name__ == '__main__':
    check_args()
    if len(sys.argv) == 9:
        params = Params(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8])
    elif len(sys.argv) == 8:
        params = Params(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], "END")
    else:
        eprint("Incorrect Arguments")
        sys.exit()
    
    # TEST 2
    # sys.stdout = open("ourtest2.txt", 'w')
    # params = Params(
    #     n=1,
    #     seed=2,
    #     lam=0.01,
    #     upper_bound=256,
    #     t_cs=4,
    #     alpha=0.5,
    #     t_slice=128,
    #     rr_add="END"
    # )

    # TEST 3
    # sys.stdout = open("ourtest3.txt", 'w')
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
    # sys.stdout = open("rrbegin4.txt", 'w')
    #params = Params(
    #    n=16,
    #    seed=2,
    #    lam=0.01,
    #    upper_bound=256,
    #    t_cs=4,
    #    alpha=0.75,
    #    t_slice=64,
    #    rr_add="BEGINNING"
    #)

    # TEST 5
    # sys.stdout = open("ourtest5.txt", 'w')
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
    print()
    '''
    Shortest Job First (SJF)
    '''
    processes = []
    ran = Rand48(params.seed)
    ran.srand(params.seed)
    for i in range(params.n):
        processes.append(Process(chr(i + 65), params, ran))

    sjf_stats = sjf(processes=processes, params=params)
    print()
    '''
    Shortest Remaining Time (SRT)
    '''
    processes = []
    ran = Rand48(params.seed)
    ran.srand(params.seed)
    for i in range(params.n):
        processes.append(Process(chr(i + 65), params, ran))

    srt_stats = srt(processes=processes, params=params)
    print()
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
