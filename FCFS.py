import queue


# Needs to return string
def print_ready_queue(q):
    tmp = ""
    if len(q) == 0:
        return " <empty>"
    else:
        for p in q:
            tmp += ' '
            tmp += p.get_process_name()
    return tmp


def fcfs(process_array, processes, cpu_bound_processes, seed, lambda_, upper_bound, context_switch_time, cpu_burst_time_estimate, time_slice):
    # This is correct for the first test case, not the others

    '''
    :param process_array: Process Array that has name, arrival time
    :return:

    Might need to convert arrays to queues later if too slow, but should
    be able to work for FCFS
    '''
    print("time 0ms: Simulator started for FCFS [Q <empty>]")
    io_bound_processes = processes - cpu_bound_processes
    time = 0
    current_process_queue = [] #queue.PriorityQueue()

    '''
    Add a process to the ready queue when it arrives or when it completes an IO burst
    Remove it once that process starts, and set it to be the current process
    '''
    ready_queue = []
    current_process = None
    finish_time = 0
    # start_time_set = set()
    '''
    In FCFS, only two things can interrupt once a process has started
    - Termination of an I/O Burst
    - Arrival of a new Process
    
    Notes
    - Maybe add thing_to_do in complete io burst instead of switch
    - Need to implement a check or flag so code knows if a process is currently being run. if arrival or completion of
      io burst happens and not doing anything, start that immediately. Otherwise, must calculate and wait til end.
    
    0 - arrival: print as soon as they come in, add process to ready queue, add thing_to_do as with key=start
    1 - start: remove from ready queue, add thing_to_do with key=complete(cpu_burst), set current_process
    2 - complete (CPU Burst): ready queue doesn't change, add to thing_to_do with key=switching
    3 - complete (I/O Burst): print as soon as they come in, add process to ready queue, also add to thing_to_do with key=start
    4 - switch: add to thing_to_do with key=complete(io_burst if cpu bursts left, change current_process to be None
    5 - terminate: print once as cpu bursts for said process are done
    # [ [3210ms, process A, key?, name] ] name useful for print
    
    Solution for I/O Burst/ Arrival times is set them to the next time something
    Happens if they arrive when they cant start immediately
    '''
    # IO completes and arrivals interrupt a cpu burst start, complete, and switch
    thing_to_do = []

    for process in process_array:
        # print(f'time {process.get_arrival_time()}ms: Process {process.get_process_name()} arrived; added to ready queue [Q {process.get_process_name()}]')
        if (len(ready_queue) == 0):  # cut context switch time in half, since not removing anything
            tmp = process.get_arrival_time() + (context_switch_time // 2)
            process.set_start_time(tmp)
            thing_to_do.append([process.get_arrival_time(), process, 0, process.get_process_name()])
        else:
            tmp = process.get_arrival_time() + (context_switch_time)
            process.set_start_time(tmp)
            thing_to_do.append([process.get_arrival_time(), process, 0, process.get_process_name()])


    # can make this run forever, just make sure no infinite loop first
    while (time < 1_300_000):
        time += 1
        # if (time > 519_000):
            # print(f'time is {time}')
        # For printing the arrival times
        # will probably need to make this faster
        # can calculate arrival times and put in a set for faster lookup

        # get next time is only looking forward once

        # Means we are starting a CPU burst of a process. Finish, then update time to save efficiency
        # [ [3210ms, process A, key?, name] ]

        for x in thing_to_do:
            # if (time > 519_980):
                # print(f'time is {time}, x is {x}')
            if x[0] == time:  # Hit something to do
                process = x[1]
                if x[2] == 0:  # Arrival
                    # Upon arrival, don't start if in the middle of a process
                    ready_queue.append(process)
                    if (time < 10_000):
                        print(f'time {process.get_arrival_time()}ms: Process {process.get_process_name()} arrived; added to ready queue [Q {print_ready_queue(ready_queue)}]')
                    # print(print_ready_queue(ready_queue))
                    if current_process is None:  # Nothing going, can start immediately, half context_switch time
                        thing_to_do.append([process.get_arrival_time() + (context_switch_time // 2), process, 1, process.get_process_name()])
                    else:  # Process is going on. Must wait
                        thing_to_do.append([current_process.get_next_time() + context_switch_time, process, 1, current_process.get_process_name()])
                        # print(ready_queue[0].get_process_name())

                    '''
                    if (len(ready_queue) == 0):
                        thing_to_do.append([process.get_arrival_time() + (context_switch_time//2), process, 1])
                    else:  # know something else is running, must add time with wait
                        tmp_process = ready_queue[0]
                        thing_to_do.append([tmp_process.get_next_time() + context_switch_time, process, 1])
                        #print(ready_queue[0].get_process_name())
                    ready_queue.append(process)
                    '''

                elif x[2] == 1:  # Start
                    # Before start, need to make sure nothing else is going
                    # if (len(ready_queue) == 0):
                    '''
                    if (process.get_num_cpu_bursts == 0):
                        current_process = ready_queue.pop(0)
                        print("\n\n\n here", ready_queue)
                        tmp_cpu_burst = process.get_cpu_burst_array()[process.get_cpu_burst_index()]
                        thing_to_do.append([time + tmp_cpu_burst, process, 5, process.get_process_name()])
                    '''

                    # current_process = ready_queue.pop(0)
                    # if current_process is process, then we can start. basically like nothing is there
                    # if it is not, we must wait, and append to start again with later time
                    if current_process is None: # (current_process.get_process_name() == process.get_process_name()):
                        current_process = ready_queue.pop(0)
                        tmp_cpu_burst = process.get_cpu_burst_array()[process.get_cpu_burst_index()]
                        if (time < 10_000):
                            print(f'time {time}ms: Process {process.get_process_name()} started using the CPU for {tmp_cpu_burst}ms burst [Q{print_ready_queue(ready_queue)}]')
                        process.increment_cpu_burst_index()
                        process.use_cpu_burst()
                        if (process.get_num_cpu_bursts() == 0):
                            thing_to_do.append([time + tmp_cpu_burst, process, 5, process.get_process_name()])
                        else:
                            thing_to_do.append([time + tmp_cpu_burst, process, 2, process.get_process_name()])
                    else: #re append with next_set_tim, don't print anything
                        # todo: might have errors with cpu_burst_array / index
                        if (current_process.get_process_name() == process.get_process_name()):
                            print("HEREE\n\n\n\n\nIMIMCIWEC")
                        else:
                            # tmp_cpu_burst = process.get_cpu_burst_array()[process.get_cpu_burst_index()]
                            # process.increment_cpu_burst_index()
                            # process.use_cpu_burst()
                            thing_to_do.append([current_process.get_next_time() + context_switch_time, process, 1, process.get_process_name()])


                    # print("current process is ", current_process.get_process_name())

                    # tmp_cpu_burst = process.get_cpu_burst_array()[process.get_cpu_burst_index()]
                    # print(f'time {time}ms: Process {process.get_process_name()} started using the CPU for {tmp_cpu_burst}ms burst [Q{print_ready_queue(ready_queue)}]')
                    # process.increment_cpu_burst_index()
                    # process.use_cpu_burst()
                    # thing_to_do.append([time+tmp_cpu_burst, process, 2, process.get_process_name()])

                    # Now that we started, we need to update next time of current_process
                    process.set_next_time(time+tmp_cpu_burst)
                elif x[2] == 2:  # Complete (CPU-burst)
                    if (time < 10_000):
                        print(f'time {time}ms: Process {process.get_process_name()} completed a CPU burst; {process.get_num_cpu_bursts()} bursts to go [Q{print_ready_queue(ready_queue)}]')
                    thing_to_do.append([time, process, 4, process.get_process_name()])
                    # Upon Completion, we must remove process from the queue
                    # current_process_queue.pop()
                elif x[2] == 3:  # Complete (I/O burst)
                    ready_queue.append(process)
                    if (time < 10_000):
                        print(f'time {time}ms: Process {process.get_process_name()} completed I/O; added to ready queue [Q{print_ready_queue(ready_queue)}]')
                    if process.get_num_cpu_bursts() > 0:
                        if current_process is None:
                            thing_to_do.append([process.get_io_blocked_until() + (context_switch_time // 2), process, 1, process.get_process_name()])
                        else: # must wait to be done
                            thing_to_do.append([current_process.get_next_time() + context_switch_time, process, 1, current_process.get_process_name()])


                        # append with half of context switch time added to time
                        # but will likely need an update if doesn't go directly after io burst completed
                        # thing_to_do.append([process.get_io_blocked_until() + (context_switch_time//2), process, 1])
                elif x[2] == 4:  # Switch
                    tmp_io_burst = time + process.get_io_burst_array()[process.get_io_burst_index()] + (context_switch_time // 2)
                    if (time < 10_000):
                        print(f'time {time}ms: Process {process.get_process_name()} switching out of CPU; blocking on I/O until time {tmp_io_burst}ms [Q{print_ready_queue(ready_queue)}]')
                    # Must save to process when it is blocked until
                    process.set_io_blocked_until(tmp_io_burst)
                    process.increment_io_burst_index()

                    # keep going for all cpu bursts in said process
                    if process.get_num_cpu_bursts() > 0:
                        # Wait until not io blocked to complete another CPU Burst
                        thing_to_do.append([process.get_io_blocked_until(), process, 3, process.get_process_name()])
                    # elif process.get_num_cpu_bursts == 0:
                    #    thing_to_do.append([process.get_io process, 5, process.get_process_name()])
                    current_process = None
                elif x[2] == 5:  # Terminate
                    print(f'time {time}ms: Process {process.get_process_name()} terminated [Q{print_ready_queue(ready_queue)}]')
                    current_process = None
                    total_cpu_bursts = 0
                    for tmp_p in process_array:
                        # print(f'{total_cpu_bursts}, {tmp_p.get_num_cpu_bursts()}')
                        total_cpu_bursts += tmp_p.get_num_cpu_bursts()
                    if (total_cpu_bursts == 0):
                        finish_time = time + (context_switch_time//2)
                        break

                else:
                    print("THIS SHOULD NOT HAPPEN!")


        '''
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
                            print(f'time {check_process.get_arrival_time()}ms: Process {check_process.get_process_name()} arrived; added to ready queue [Q {check_process.get_process_name()}]')
                            if (len(current_process_queue) == 0):  # cut context switch time in half, since not removing anything
                                tmp = check_process.get_arrival_time() + (context_switch_time / 2)
                                check_process.set_start_time(tmp)
                                start_time_set.add(tmp)
                                thing_to_do.append([check_process.get_arrival_time(), check_process, 0])
                            else:
                                tmp = check_process.get_arrival_time() + context_switch_time
                                check_process.set_start_time(tmp)
                                start_time_set.add(tmp)
                                thing_to_do.append([check_process.get_arrival_time(), check_process, 0])

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
            
            '''
    # print(time)
    print(f'time {finish_time}ms: Simulator ended for FCFS [Q <empty>]')
