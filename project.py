from FCFS import fcfs
from SRT import srt
from SJF import sjf
from RR import rr

process_array = []


'''
rand object is from
https://stackoverflow.com/questions/7287014/is-there-any-drand48-equivalent-in-python-or-a-wrapper-to-it
'''
import sys
import math

alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
            'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',]

# Uncomment the next line if using Python 2.x...
# from __future__ import division


def part_one(processes, cpu_bound_processes, io_bound_processes, seed, lambda_, upper_bound):

    '''
    :param processes:
    :param cpu_bound_processes:
    :param io_bound_processes:
    :param seed:
    :param lambda_:
    :param upper_bound:
    :return: void

    Part one that must be ran at the beginning, but with less print statements that before
    '''
    rand = Rand48(seed)
    print(f'<<< PROJECT PART I -- process set (n={processes}) with {cpu_bound_processes} CPU-bound process', end='')
    if cpu_bound_processes == 1:
        print(" >>>")
    else:
        print("es >>>")
    for process in range(processes):
        # For a specific process (A, B, etc)
        # make it
        Process_ = Process(alphabet[process])
        process_array.append(Process_)
        arrival_time = math.floor(next_exp(lambda_, rand, upper_bound))
        Process_.set_arrival_time(arrival_time)
        num_bursts = math.ceil(rand.drand() * 100)
        process_name = Process_.get_process_name()
        if process + 1 <= io_bound_processes:
            print("I/O-", end='')
        else:
            print("CPU-", end='')

        print(f'bound process {process_name}: arrival time {arrival_time}ms; {num_bursts} CPU bursts')
        for burst in range(num_bursts - 1):
            # alternate between cpu and io bursts
            cpu_burst_tmp = math.ceil((next_exp(lambda_, rand, upper_bound)))
            if (process + 1 > io_bound_processes):
                cpu_burst_tmp *= 4
            # print(f'--> CPU burst {cpu_burst_tmp}ms', end='')
            Process_.add_cpu_burst(cpu_burst_tmp)
            io_burst_tmp = math.ceil((next_exp(lambda_, rand, upper_bound))) * 10
            if (process + 1 > io_bound_processes):
                io_burst_tmp = io_burst_tmp // 4
            # print(f' --> I/O burst {io_burst_tmp}ms')
            Process_.add_io_bursts(io_burst_tmp)
        cpu_burst_tmp = math.ceil((next_exp(lambda_, rand, upper_bound)))
        if (process + 1 > io_bound_processes):
            cpu_burst_tmp *= 4
        # print(f'--> CPU burst {cpu_burst_tmp}ms')
        Process_.add_cpu_burst(cpu_burst_tmp)


# Determines a CPU burst
def next_exp(lambda_, rand, upper_bound):
    burst = rand.drand()
    time = ((-1 * math.log(burst)) / lambda_)
    while time > upper_bound:
        burst = rand.drand()
        time = ((-1 * math.log(burst)) / lambda_)
    return time


class Rand48(object):
    def __init__(self, seed):
        # This is the srand function
        self.n = (seed << 16) + 0x330e

    def next(self):
        self.n = (25214903917 * self.n + 11) & (2**48 - 1)
        return self.n

    def drand(self):
        # This drand fuction calls next
        return self.next() / 2**48


class Process(object):
    def __init__(self, char):
        # Arrival time is once, when that process arrives
        self.name = char
        self.cpu_bursts = []
        self.io_bursts = []
        self.total_bursts = 0
        self.arrival_time = 0
        self.start_time = 0
        self.num_cpu_bursts = 0
        self.cpu_burst_index = 0
        self.io_burst_index = 0
        self.next_time = 0
        self.io_blocked_until = 0

    def add_cpu_burst(self, cpu_burst):
        self.cpu_bursts.append(cpu_burst)
        self.total_bursts += 1
        self.num_cpu_bursts += 1

    def add_io_bursts(self, io_burst):
        self.io_bursts.append(io_burst)
        self.total_bursts += 1

    def set_arrival_time(self, arrival_time):
        self.arrival_time = arrival_time

    def get_process_name(self):
        return self.name

    def get_arrival_time(self):
        return self.arrival_time

    def set_start_time(self, start_time):
        self.start_time = start_time

    def get_start_time(self):
        return self.start_time

    def get_cpu_burst_array(self):
        return self.cpu_bursts

    def get_io_burst_array(self):
        return self.io_bursts

    def get_num_cpu_bursts(self):
        return self.num_cpu_bursts

    def use_cpu_burst(self):
        self.num_cpu_bursts -= 1

    def increment_cpu_burst_index(self):
        self.cpu_burst_index += 1

    def get_cpu_burst_index(self):
        return self.cpu_burst_index

    def increment_io_burst_index(self):
        self.io_burst_index += 1

    def get_io_burst_index(self):
        return self.io_burst_index

    def set_next_time(self, next_time):
        self.next_time = next_time

    def get_next_time(self):
        return self.next_time

    def set_io_blocked_until(self, blocked_io):
        self.io_blocked_until = blocked_io

    def get_io_blocked_until(self):
        return self.io_blocked_until




'''
class Simulator(object):
    def __init__(self):
        # make priority queue for everything but FCFS
        pass
'''


if __name__ == '__main__':
    queue = []

    '''
    Part 2
    example run project.py 3 1 1024 0.001 3000 4 0.75 256
    1st: 3 is number of process. assigned alphabeticals from A-Z, most is 26.
    2nd: 1 is number of cpu-bound processes
    3rd: 1024 is seed for the pseudorandom number sequence
    4th: 0.001 is lambda. 1/lambda_ is the average random value generated
    5th: 3000 is upper bound for valid pseudo-random numbers, upper bound relates to arrival time
    6th: 4ms is time required to make a context switch 
    7th: 0.75 is estimate cpu burst time, for SJF and SRT.
    8th: 256 is time slice in ms
    
    
    '''


    # number of process. assigned alphabeticals from A-Z, most is 26.
    processes = int(sys.argv[1])

    # number of cpu-bound processes
    cpu_bound_processes = int(sys.argv[2])

    io_bound_processes = processes - cpu_bound_processes

    # seed for the pseudorandom number sequence
    seed = int(sys.argv[3])

    # 1/lambda_ is the average random value generated
    lambda_ = float(sys.argv[4])

    # bounds for valid pseudo-random numbers, upper bound relates to arrival time
    # make sure next_exp is between lower and upper
    lower_bound = 0
    upper_bound = int(sys.argv[5])

    context_switch_time = int(sys.argv[6])

    cpu_burst_time_estimate = float(sys.argv[7])

    time_slice = int(sys.argv[8])

    part_one(processes, cpu_bound_processes, io_bound_processes, seed, lambda_, upper_bound)

    print()

    # Part 2 starts, Could be it's own function

    print(f'<<< PROJECT PART II -- t_cs={context_switch_time}ms; alpha={cpu_burst_time_estimate:.2f}; t_slice={time_slice}ms >>>')

    fcfs(process_array, processes, cpu_bound_processes, seed, lambda_, upper_bound, context_switch_time, cpu_burst_time_estimate, time_slice)

    # sjf()

    # srt()

    # rr(process_array, processes, cpu_bound_processes, seed, lambda_, upper_bound, context_switch_time, cpu_burst_time_estimate, time_slice)
