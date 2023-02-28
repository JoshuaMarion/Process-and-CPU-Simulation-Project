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

    def add_cpu_burst(self, cpu_burst):
        self.cpu_bursts.append(cpu_burst)
        self.total_bursts += 1

    def add_io_bursts(self, io_burst):
        self.cpu_bursts.append(io_burst)
        self.total_bursts += 1

    def set_arrival_time(self, arrival_time):
        self.arrival_time = arrival_time

    def get_process_name(self):
        return self.name
if __name__ == '__main__':
    queue = []


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




    # todo: Add to class later
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
        arrival_time = math.floor(next_exp(lambda_, rand, upper_bound))
        Process_.set_arrival_time(arrival_time)
        num_bursts = math.ceil(rand.drand() * 100)
        process_name = Process_.get_process_name()
        if process+1 <= io_bound_processes:
            print("I/O-", end='')
        else:
            print("CPU-", end='')

        print(f'bound process {process_name}: arrival time {arrival_time}ms; {num_bursts} CPU bursts:')
        for burst in range(num_bursts-1):
            # alternate between cpu and io bursts
            cpu_burst_tmp = math.ceil((next_exp(lambda_, rand, upper_bound)))
            if (process+1 > io_bound_processes):
                cpu_burst_tmp *= 4
            print(f'--> CPU burst {cpu_burst_tmp}ms', end='')
            Process_.add_cpu_burst(cpu_burst_tmp)
            io_burst_tmp = math.ceil((next_exp(lambda_, rand, upper_bound))) * 10
            if (process+1 > io_bound_processes):
                io_burst_tmp = io_burst_tmp // 4
            print(f' --> I/O burst {io_burst_tmp}ms')
            Process_.add_io_bursts(io_burst_tmp)
        cpu_burst_tmp = math.ceil((next_exp(lambda_, rand, upper_bound)))
        if (process + 1 > io_bound_processes):
            cpu_burst_tmp *= 4
        print(f'--> CPU burst {cpu_burst_tmp}ms')
        Process_.add_cpu_burst(cpu_burst_tmp)
