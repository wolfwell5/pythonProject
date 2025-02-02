import random
import time

sleep_range = [1, 2]


def sleep_random():
    random_time = random.randint(sleep_range[0], sleep_range[1])
    print(rf'random stop: {random_time} s')
    time.sleep(random_time)
