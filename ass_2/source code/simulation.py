import math
from random import random,seed

class server:
    def __init__(self,flag,expire_t,detail = (0,0)):
        self.flag = flag
        self.expire_time =expire_t
        self.detail = detail

class event:
    def __init__(self, status, detail):
        self.status = status
        self.detail = detail

def find_server(l,flag):
    i = 0
    for e in l:
        if e.flag == flag:
            i+=1
    return i

def function(mode,arrival,service,nb_server,setup_t,delayoff_t,time_end=9999):
    depart_time =[]
    master_clock = [0]
    l = []
    buffer_queue = list()
    for i in range(nb_server):
        a = server('OFF',-1)
        l.append(a)
    if mode =='random':
        time = []
        a=0
        service_time_list =[]
        while True:
            a += (-math.log(1- random())/arrival)
            if a >= time_end:
                break
            time.append((a,2))
            service_time_list.append((-math.log(1 - random())/service) +(-math.log(1 - random())/service) + (-math.log(1 - random())/service))
        service_time_list.reverse()
    if mode =='trace':
        time = [(e,2) for e in arrival]
        service.reverse()
        service_time_list = service                                                                 # time 2:arrival 1:event finish
    while master_clock[0] <= time_end:
        if len(time) ==0:
            break                                                                                   #0: setup finish 3:delayoff finish
        time = sorted(time,reverse=True)
        master_clock = time.pop()
        if master_clock[1] == 2:
            busy = find_server(l,'BUSY')
            delay = find_server(l,'DELAY')
            setup = find_server(l,'SETUP')
            if busy + setup == nb_server:
                service_time = service_time_list.pop()
                buffer_queue.append(event(-1,(master_clock[0],service_time)))
            elif delay > 0:
                p = 0
                for index,e in enumerate(l):
                    if e.flag == 'DELAY':
                        if e.expire_time - master_clock[0]> p:
                            p = e.expire_time - master_clock[0]
                            index_delay = index
                service_time = service_time_list.pop()
                l[index_delay] = server('BUSY',-1,(master_clock[0],service_time))
                time.append((master_clock[0] + service_time,1))
            else:
                for index,e in enumerate(l):
                    if e.flag =='OFF':
                        service_time = service_time_list.pop()
                        buffer_queue.append(event(1,(master_clock[0],service_time)))
                        l[index] = server('SETUP',-1,(master_clock[0],setup_t))
                        time.append((master_clock[0] + setup_t, 0))
                        break
        elif master_clock[1] ==1:
            for e in l:
                if e.flag =='BUSY' and master_clock[0] == e.detail[0] + e.detail[1]:
                    if e.expire_time ==-1:
                        depart_time.append((e.detail[0],e.detail[0]+e.detail[1]))
                    else:
                        depart_time.append((e.expire_time, e.detail[0] + e.detail[1]))
                    if buffer_queue:
                        task = buffer_queue[0]
                        buffer_queue = buffer_queue[1:]
                        e.expire_time = task.detail[0]
                        e.detail = (master_clock[0],task.detail[1])
                        time.append((master_clock[0]+task.detail[1],1))
                        if task.status==1:
                            nb_unmark = 0
                            for t in buffer_queue:
                                if t.status ==-1:
                                    nb_unmark+=1
                            if nb_unmark:
                                for t in buffer_queue:
                                    if t.status==1:
                                        continue
                                    t.status = task.status
                                    break
                            else:
                                max = -1
                                for index,e_set in enumerate(l):
                                    if e_set.flag =='SETUP':
                                        if max ==-1:
                                            max = master_clock[0]-e_set.detail[0]
                                            e_index = index
                                        else:
                                            if master_clock[0]-e_set.detail[0]< max:
                                                max = master_clock[0]-e_set.detail[0]
                                                e_index = index
                                l[e_index] = server('OFF',-1,(0,0))
                    else:
                        e.flag ='DELAY'
                        e.expire_time = master_clock[0] + delayoff_t
                        e.detail = (master_clock[0],delayoff_t)
                        time.append((e.expire_time,3))
                    break
        elif master_clock[1] == 0:
            for e in l:
                if e.flag =='SETUP' and master_clock[0] == e.detail[0] + e.detail[1]:
                    for index, e_1 in enumerate(buffer_queue):
                        if e_1.status == 1:
                            task = buffer_queue[index]
                            if index == len(buffer_queue) - 1:
                                buffer_queue.pop()
                            else:
                                buffer_queue = buffer_queue[:index] + buffer_queue[index + 1:]
                            break
                    e.flag = 'BUSY'
                    e.expire_time = task.detail[0]
                    e.detail = (master_clock[0], task.detail[1])
                    time.append((master_clock[0] + task.detail[1], 1))
                    break
        else:
            for e in l:
                if e.flag =='DELAY' and master_clock[0] == e.expire_time:
                    e.flag ='OFF'
                    e.expire_time =-1
                    e.detail =(0,0)
                    break
    mrt = 0
    for e in depart_time:
        mrt +=e[1]-e[0]
    mrt /= float(len(depart_time))
    return mrt,depart_time