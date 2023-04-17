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

def rr():
    pass