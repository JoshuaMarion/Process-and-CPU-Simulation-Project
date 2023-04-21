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
    str = "[Q"
    if len(readyState) == 0:
        return str + " <empty>]"
    for i in readyState:
        str += " "+i.name
    str += "]"
    return str

def rr(process_array, processes, cpu_bound_processes, seed, lambda_, upper_bound, context_switch_time, cpu_burst_time_estimate, time_slice):
    # :)   
    print("time 0ms: Simulator started for RR [Q <empty>]")

    interesting_events = queue.PriorityQueue()
    time = 0
    current_process_queue = []
    next_cpu = 0

    for process in process_array:
        interesting_events.put((process.get_arrival_time(),process))

    # print("time 0ms: Simulator started for RR with time slice " + str(time_slice) + "ms " + printQueue(current_process_queue) )

    while not interesting_events.empty() :
        priority, process = interesting_events.get()
        event = process.get_interesting()
        time = process.get_arrival_time()

        # Interesting Event Numbers:
        # 0 - process arrives
        # 1 - starts using CPU
        # 2 - finishes using CPU
        # 3 - pre emption
        # 4 - io finishes
        # 5 - add to current_process_queue

        if event == 0:
            time = process.get_arrival_time()
            if len(current_process_queue)== 0 and next_cpu == 0:
                process.set_interesting(5)
                interesting_events.put((time, process))
            current_process_queue.append(process)
            print("time " + str(time) + "ms: Process " + str(process.get_process_name() + " arrived; added to ready queue " + printQueue(current_process_queue)))
        elif event == 1:
            if(process.get_cpu_burst_array()[0] < 0):
                process.add_cpu_burst(process.get_cpu_burst_array()[0]*(-1))
                time+= int(context_switch_time/2)

                print("time " + str(time) + "ms: Process " + process.get_process_name() + " started using the CPU for remaining "+str(process.get_cpu_burst_array()[0])+ "ms of " + str(process.get_cpu_burst_array()[0] + time_slice) + "ms burst " + printQueue(current_process_queue))
                process.set_interesting(2)
                interesting_events.put(((time+process.get_cpu_burst_array()[0]), process))
            else:
                time+=int(context_switch_time/2)
                print("time " + str(time) + "ms: Process "+ process.get_process_name()+" started using the CPU for " + str(process.get_cpu_burst_array()[0])+" ms burst " + printQueue(current_process_queue))
                if process.get_cpu_burst_array()[0] > time_slice:
                    process.set_interesting(3)
                    interesting_events.put(((time+process.get_cpu_burst_array()[0]), process))
                else:
                    process.set_interesting(2)
                    interesting_events.put(((time+process.get_cpu_burst_array()[0]), process))
        elif event == 2: 
            next_cpu = 0
            del process.get_cpu_burst_array()[0]
            if len(process.get_cpu_burst_array()) == 0:
                print("time " + str(time) + "ms: Process " + process.get_process_name() + " terminated " + printQueue(current_process_queue))
            else:
                if len(process.get_cpu_burst_array()) == 1:
                    print("time " + str(time) + "ms: Process " + process.get_process_name() + " completed a CPU burst; " + str(len(process.get_cpu_burst_array())) + " burst to go " + printQueue(current_process_queue))
                else:
                    print("time " + str(time) + "ms: Process " + process.get_process_name() + " completed a CPU burst; " + str(len(process.get_cpu_burst_array())) + " bursts to go " + printQueue(current_process_queue))
                
                print("time " + str(time) + "ms: Process " + process.get_process_name() + " switching out of CPU; will block on I/O until time " +  str(process.get_io_burst_array()[0]+ time + int(context_switch_time/2)) + "ms " + printQueue(current_process_queue))
                
                process.set_interesting(4)
                interesting_events.put((time+process.get_io_burst_array()[0]+int(context_switch_time/2), process))

            if len(current_process_queue) > 0:
                current_process_queue[0].set_interesting(5)
                interesting_events.put((time + int(context_switch_time/2), current_process_queue[0])) #potentially fix this +++
        elif event == 3:
            process.get_cpu_burst_array()[0] -= time_slice
            if len(current_process_queue) == 0:
                print("time " + str(time) + "ms: Time slice expired; no preemption because ready queue is empty [Q empty]")
                process.set_interesting(2)
                interesting_events.put((time+process.get_cpu_burst_array()[0],process))
            else:
                next_cpu = 0
                print("time " + str(time) + "ms: Time slice expired; process " + process.get_process_name() + " preempted with " + str(process.get_cpu_burst_array()[0]) + "ms to go " + printQueue(current_process_queue))
                process.get_cpu_burst_array()[0] *= -1
                current_process_queue[0].set_interesting(5)
                interesting_events.put((time+context_switch_time/2, current_process_queue[0])) #potentially fix this +++
        elif event == 4:
            del process.get_io_burst_array()[0]
            current_process_queue.append(process)
            current_process_queue[0].set_interesting(5)
            interesting_events.put((time, current_process_queue[0])) #maybe fix this +++
            print("time " + str(time) + "ms: Process " + process.get_process_name() + " completed I/O; added to ready queue " + printQueue(current_process_queue))
        elif event == 5:
            if next_cpu != 0:
                continue
            else:
                process.set_interesting(1)
                interesting_events.put((time, process))

                if process.get_cpu_burst_array()[0] < 0:
                    next_cpu = time+(process.get_cpu_burst_array()[0] * (-1))
                else:
                    next_cpu = time + (process.get_cpu_burst_array()[0])
                
                del current_process_queue[0]


    print("time " + str(time+int(context_switch_time/2)) + "ms: Simulator ended for RR " + printQueue(current_process_queue))
            