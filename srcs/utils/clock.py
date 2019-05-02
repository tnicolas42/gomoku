import time


class Clock(object):

    def __init__(self, rate):
        self.last_loop = time.time() * 1000
        self.rate = 0
        self.time_loop = 0
        self.time_process = 0  # time spend to process all calcules

        self.set_rate(rate)

    def set_rate(self, rate):
        """
        set the rate
        :param rate: the rate
        """
        self.rate = rate
        self.time_loop = 1000 / rate

    def tick(self):
        """
        wait X ms to keep a constant rate
        :return: time for process since last loop
        :rtype: float
        """
        time_act = time.time() * 1000
        self.time_process = time_act - self.last_loop
        if time_act - self.last_loop < self.time_loop:
            time.sleep((self.time_loop - self.time_process) / 1000)
        self.last_loop = time.time() * 1000
        return self.time_process