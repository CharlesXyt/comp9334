from simulation import *


with open('num_tests.txt','r') as file:
    for line in file:
        nb_test = int(line)
        break
for i in range(1,nb_test+1):
    with open('mode_{}.txt'.format(i),'r') as file:
        for line in file:
            mode = line
            break
    with open('para_{}.txt'.format(i),'r') as file:
        for index,line in enumerate(file):
            if index ==0:
                nb_server = int(line)
            if index ==1:
                setup_t = float(line)
            if index ==2:
                delayoff_t =float(line)
            if index ==3:
                time_end = float(line)
    with open('arrival_{}.txt'.format(i), 'r') as file:
        arrival = []
        for line in file:
            arrival.append(float(line))
    with open('service_{}.txt'.format(i), 'r') as file:
        service = []
        for line in file:
            service.append(float(line))
    if mode =='random':
        mrt,depart_time =function(mode,arrival[0],service[0],nb_server,setup_t,delayoff_t,time_end)
    if mode =='trace':
        mrt, depart_time = function(mode, arrival, service, nb_server, setup_t, delayoff_t)
    with open('mrt_{}.txt'.format(i),'w') as file:
        file.write('{:0.3f}'.format(mrt))
    with open('departure_{}.txt'.format(i),'w') as file:
        for e in depart_time:
            str = '{:0.3f}\t {:0.3f}\n'.format(e[0],e[1])
            file.write(str)


