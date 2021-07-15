import time


class Timer():
    def __init__(self):
        self.start = time.time()

    def end(self):
        self.end = time.time()
        elapsed_time = self.end - self.start
        minutes = int(elapsed_time // 60)
        seconds = elapsed_time % 60

        print("Elapsed time: {}m {}s".format(minutes, round(seconds)))
