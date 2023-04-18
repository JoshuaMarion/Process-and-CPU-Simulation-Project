# Round robin (RR)
# The RR algorithm is essentially the FCFS algorithm with time slice tslice. Each process is given
# tslice amount of time to complete its CPU burst. If the time slice expires, the process is preempted
# and added to the end of the ready queue.
# If a process completes its CPU burst before a time slice expiration, the next process on the ready
# queue is context-switched in to use the CPU.
# For your simulation, if a preemption occurs and there are no other processes on the ready queue,
# do not perform a context switch. For example, given process G is using the CPU and the ready
# queue is empty, if process G is preempted by a time slice expiration, do not context-switch process G
# back to the empty queue; instead, keep process G running with the CPU and do not count this as
# a context switch. In other words, when the time slice expires, check the queue to determine if a
# context switch should occur.
import queue

def printQueue(readyState):
    str = "[Q "
    if len(readyState) == 0:
        return str + "empty]"
    for i in readyState:
        str += i.name
    str += "]"
    return str

def rr(process_array, processes, cpu_bound_processes, seed, lambda_, upper_bound, context_switch_time, cpu_burst_time_estimate, time_slice):
    # :)   
    # print("time 0ms: Simulator started for RR [Q <empty>]")
    interesting_events = queue.PriorityQueue()
    time = 0
    current_process_queue = []
    start_time_set = set()

    for event in process_array:
        interesting_events.put((event.get_arrival_time(), event.get_process_name()))

    print("time 0ms: Simulator started for RR with time slice " + str(time_slice) + "ms " + printQueue(current_process_queue) )

    # while not interesting_events.empty() :
        # priority, hi = interesting_events.get()
        # print(priority+" AND "+hi)
    while time < 10000:
        time+=1
        for process in process_array:
            if process.get_arrival_time() == time:
                print(f'time {process.get_arrival_time()}ms: Process {process.get_process_name()} arrived; added to ready queue [Q {process.get_process_name()}]')
                temp = process.get_arrival_time() + (context_switch_time/2)
                if (len(current_process_queue) == 0):
                    process.set_start_time(temp)
                    start_time_set.add(temp)
                else:
                    process.set_start_time(temp)
                    start_time_set.add(temp)
        

        if (time in start_time_set):
            for process in process_array:
                if(process.get_start_time() == time):
                    temp_cpu_burst = process.get_cpu_burst_array()[process.get_cpu_burst_index()]
                    print("time " + str(time) + "ms: Process " + process.name + " started using the CPU for the remaining " + str(process.cpu_bursts[0])+"ms of "+ str(process.cpu_bursts[0]+time_slice)+"ms burst" + printQueue(process_array))
    print("time "+str(time)+"ms: Simulator started for RR with time slice " + str(time_slice) + "ms " + printQueue(current_process_queue) )

    # while not priorities.empty():