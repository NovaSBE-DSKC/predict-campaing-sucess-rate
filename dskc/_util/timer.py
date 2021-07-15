import time


class Timer():
    def __init__(self):
        self.start = time.time()

    def end(self,prefix="Elapsed time: "):
        self.end = time.time()
        elapsed_time = self.end - self.start
        minutes = int(elapsed_time // 60)
        seconds = elapsed_time % 60
        
        if minutes > 0:
            prefix+="{}m ".format(minutes)
            
        print("{}{}s".format(prefix, round(seconds)))
