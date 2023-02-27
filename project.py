'''
rand object is from
https://stackoverflow.com/questions/7287014/is-there-any-drand48-equivalent-in-python-or-a-wrapper-to-it
'''

# Uncomment the next line if using Python 2.x...
# from __future__ import division


class Rand48(object):
    def __init__(self, seed):
        # This is the srand function
        self.n = (seed << 16) + 0x330e

    def next(self):
        self.n = (25214903917 * self.n + 11) & (2**48 - 1)
        return self.n

    def drand(self):
        return self.next() / 2**48


if __name__ == '__main__':
    queue = []

    # number of process
    n = input()

    #
    processes = input()

    # seed for the pseudorandom number sequence
    seed = input()

    # 1/lambda_ is the average random value generated
    lambda_ = input()

    # upper bound for valid pseudo-random numbers
    upper_bound = input()




    print(f'<<< PROJECT PART I -- process set (n={n}) with {processes} CPU-bound process >>>')