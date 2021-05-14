import threading
import datetime, time

class SimpleTasking(threading.Thread):
    '''execute some functions based on time //hour is write like: Hour:Minute:Second'''
    def __init__(self):
        threading.Thread.__init__(self, daemon=True)
        self.schedules = {}

    def on(self, executetime = None, func = None):
        if executetime == None or func == None:
            return

        if not executetime in self.schedules:
            self.schedules[executetime] = []

        self.schedules[executetime].append(func)

    def GetNow(self):
        now = time.time()
        timestamp = datetime.datetime.fromtimestamp(now)
        return (str(timestamp.hour) if(timestamp.hour > 9) else '0' + str(timestamp.hour)) + ':' + (str(timestamp.minute) if(timestamp.minute > 9) else '0' + str(timestamp.minute))+ ':' + (str(timestamp.second) if(timestamp.second > 9) else '0' + str(timestamp.second))


    def run(self):
        while True:
            NowTime = self.GetNow()
            if NowTime in self.schedules:
                for Func in self.schedules[NowTime]:
                    Func()
            time.sleep(1)
            

if __name__ == '__main__':
    sched = SimpleTasking()

    sched.on('11:55:30', lambda: print("b"))
    sched.on('11:56:00', lambda: print("c1"))
    sched.on('11:56:00', lambda: print("c2"))

    sched.start()
    while True:
        pass