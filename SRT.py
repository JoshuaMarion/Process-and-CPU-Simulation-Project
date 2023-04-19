'''
The SRT algorithm is a preemptive version of the SJF algorithm. In SRT, when a process arrives,
if it has a predicted CPU burst time that is less than the remaining predicted time of the currently
running process, a preemption occurs. When such a preemption occurs, the currently running
process is simply added to the ready queue.
'''

from queue import *

def find_priority(process_array, processes, process_queue):
    
    processes_in = []
    found = False
    priority_q = 0
    while process_queue.qsize() != len(process_array):
        found = False
        shortest_cpu_time = 10000000000000000000000000000
        for process in process_array:
            cpu_array = process.get_cpu_burst_array()
            index = process.get_cpu_burst_index()
            found = False
            if cpu_array[index] < shortest_cpu_time:
                for proc in processes_in:
                    if proc.get_process_name() == process.get_process_name():
                        found = True
                        break
                if not found:
                    shortest_cpu_time = cpu_array[index]
                    curr_process = process
        processes_in.append(curr_process)
        process_queue.put((priority_q, curr_process))
        priority_q += 1
    #for i in processes_in:
     #   print(i.get_process_name() + " " + str(i.get_cpu_burst_array()[i.get_cpu_burst_index()]))
            
        

def srt(process_array, processes, cpu_bound_processes, seed, lambda_, upper_bound, context_switch_time, cpu_burst_time_estimate):
    
    io_bound = processes - cpu_bound_processes
    sim_time = 0
    completed_processes = False
    process_queue = PriorityQueue()
    arrived_processes = []
    
    find_priority(arrived_processes, processes, process_queue)
    
    already_arrived = False
    
    print("time " + str(sim_time) + "ms: Simulator started for SRT [Q <empty>]")
    #while not process_queue.empty():
    #    t_item = process_queue.get()
    #    print(t_item[1].get_process_name())
    while not completed_processes:
        #go through each process
        shortest_arrival_time = 10000000000000000000000000000
        for process in process_array:
            already_arrived = False
            if process.get_arrival_time() < shortest_arrival_time:
                for proc in arrived_processes:
                    if proc.get_process_name() == process.get_process_name():
                        already_arrived = True
                        break
                if not already_arrived:
                    shortest_arrival_time = process.get_arrival_time()
                    new_arrived_process = process
        sim_time += shortest_arrival_time
        arrived_processes.append(new_arrived_process)
        print(str(sim_time) + " " + new_arrived_process.get_process_name())
        completed_processes = True
        #print("time " + time + "ms: Process " + new_arrived_process.get_process_name() + " (tau 1000ms) arrived; added to ready queue [Q " )
                        
    