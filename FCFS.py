import queue

def fcfs(process_array, processes, cpu_bound_processes, seed, lambda_, upper_bound, context_switch_time, cpu_burst_time_estimate, time_slice):
    '''
    :param process_array: Process Array that has name, arrival time
    :return:
    '''
    print("time 0ms: Simulator started for FCFS [Q <empty>]")
    io_bound_processes = processes - cpu_bound_processes
    time = 0
    current_process_queue = [] #queue.PriorityQueue()
    start_time_set = set()

    # make dictionary of things to print??
    hshmap = {}

    while (time < 500000):
        time += 1
        # For printing the arrival times
        # will probably need to make this faster
        # can calculate arrival times and put in a set for faster lookup
        for process in process_array:
            if process.get_arrival_time() == time:
                print(f'time {process.get_arrival_time()}ms: Process {process.get_process_name()} arrived; added to ready queue [Q {process.get_process_name()}]')
                if (len(current_process_queue) == 0): # cut context switch time in half, since not removing anything
                    tmp = process.get_arrival_time() + (context_switch_time/2)
                    process.set_start_time(tmp)
                    start_time_set.add(tmp)
                else:
                    tmp = process.get_arrival_time() + (context_switch_time)
                    process.set_start_time(tmp)
                    start_time_set.add(tmp)
                    #current_process_queue.append(process)

        # Means we are starting a CPU burst of a process. Finish, then update time to save efficiency
        if (time in start_time_set):
            for process in process_array:
               # print(f'process name is {process.get_process_name()}')
                if (process.get_start_time() == time): #We now need to finish a cpu burst
                    # print(f'process name: {process.get_process_name()}, time = {time}')
                    tmp_cpu_burst = process.get_cpu_burst_array()[process.get_cpu_burst_index()]
                    print(f'time {time}ms: Process {process.get_process_name()} started using the CPU for {tmp_cpu_burst}ms burst [Q <empty>]')
                    current_process_queue.append(process)
                    process.increment_cpu_burst_index()
                    process.use_cpu_burst()

                    # Before do new time, check again and print any needed arrivals
                    for check_process in process_array:
                        if check_process.get_arrival_time() > time and check_process.get_arrival_time() < (time+tmp_cpu_burst):
                            print(f'time {check_process.get_arrival_time()}ms: Process {check_process.get_process_name()} arrived; added to ready queue [Q {process.get_process_name()}]')
                            if (len(current_process_queue) == 0):  # cut context switch time in half, since not removing anything
                                tmp = check_process.get_arrival_time() + (context_switch_time / 2)
                                check_process.set_start_time(tmp)
                                start_time_set.add(tmp)
                            else:
                                tmp = check_process.get_arrival_time() + context_switch_time
                                check_process.set_start_time(tmp)
                                start_time_set.add(tmp)

                    # todo: I HAVE NO CLUE IF THIS WORKS OR WHY IF IT DOES

                    time += tmp_cpu_burst

                    print(f'time {time}ms: Process {process.get_process_name()} completed a CPU burst; {process.get_num_cpu_bursts()} bursts to go [Q <empty>]')
                    # todo: I HAVE NO CLUE IF THIS WORKS OR WHY IF IT DOES
                    if (len(current_process_queue) != 0):
                        tmp_io_burst = time + process.get_io_burst_array()[process.get_io_burst_index()] + (context_switch_time // 2)
                    else:
                        tmp_io_burst = time + process.get_io_burst_array()[process.get_io_burst_index()]
                    print(f'time {time}ms: Process {process.get_process_name()} switching out of CPU; blocking on I/O until time {tmp_io_burst}ms [Q <empty>]')
                    # print(current_process_queue[0].get_process_name())
                    current_process_queue.pop(0)




                # Once a process is started, finish a cpu burst, and skip time ahead to end
                # Should save a lot of time and make things easier


