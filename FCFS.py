
def fcfs(process_array, processes, cpu_bound_processes, seed, lambda_, upper_bound, context_switch_time, cpu_burst_time_estimate, time_slice):
    '''

    :param process_array: Process Array that has name, arrival time
    :return:
    '''
    print("time 0ms: Simulator started for FCFS [Q <empty>]")
    io_bound_processes = processes - cpu_bound_processes
    time = 0
    current_process_queue = []
    start_time_set = set()

    while (time < 500000):
        time += 1
        # For printing the arrival times
        for process in process_array:
            if process.get_arrival_time() == time:
                print(f'time {process.get_arrival_time()}ms: Process {process.get_process_name()} arrived; added to ready queue [Q {process.get_process_name()}]')
                if (len(current_process_queue) == 0): # cut context switch time in half, since not removing anything
                    tmp = process.get_arrival_time() + (context_switch_time/2)
                    process.set_start_time(tmp)
                    start_time_set.add(tmp)
                current_process_queue.append(process)

        # Means we are starting a CPU burst of a process. Finish, then update time to save efficiency
        if (time in start_time_set):
            for process in process_array:
                if (process.get_start_time() == time): #We now need to finish a cpu burst
                    tmp_cpu_burst = process.get_cpu_burst_array()[process.get_cpu_burst_index()]
                    print(f'time {time}ms: Process {process.get_process_name()} started using the CPU for {tmp_cpu_burst}ms burst [Q <empty>]')
                    # increment cpu_burst_array?
                    time += tmp_cpu_burst



                # Once a process is started, finish a cpu burst, and skip time ahead to end
                # Should save a lot of time and make things easier


