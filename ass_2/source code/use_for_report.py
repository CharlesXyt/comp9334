from simulation import *
import matplotlib.pyplot as plt
from math import sqrt
import numpy as np


def steady_state(w,time):
    depart_l = []
    result = [0]
    for i in range(time):
        seed(i)
        mrt,depart = function('random',0.35,1,5,5,0.1,20000)
        depart.sort()
        s =[]
        for i in depart:
            s.append(i[1] - i[0])
        depart_l.append(s)
    min = 10000
    for e in depart_l:
        if(len(e)) < min:
            min = len(e)
    for i in range(min):
        a = 0
        for j in range(len(depart_l)):
            a+=depart_l[j][i]
        result.append(a/time)
    x = [i for i in range(min-w)]
    y_1 = [sum(result[1:2*i])/(2*i-1) for i in range(1,w+1)]
    y_2 = [sum(result[i-w:i+w+1])/(2*w +1) for i in range(w+1,min+1-w)]
    y = y_1+y_2
    plt.plot(x, y)
    plt.title('w = {}'.format(w))
    plt.show()
steady_state(2000,5)
steady_state(1000,5)
steady_state(500,5)
steady_state(100,5)
def calculation(w,tc):
    w = 2*w
    result = []
    for i in range(30):
        seed(i)
        mrt, depart = function('random', 0.35, 1, 5, 5, tc, 20000)
        depart.sort()
        l = []
        for e in depart:
            l.append(e[1]-e[0])
        m = sum(l[w:])/len(l[w:])
        result.append(m)
    t_p = sum(result)/len(result)
    s = 0
    for e in result:
        s+=(e-t_p)*(e-t_p)
    s_r = sqrt(s/(len(result) - 1))
    mid =2.045*s_r/sqrt(len(result))
    print((t_p-mid,t_p+mid))

def draw():
    dict ={}
    y=[]
    seed(0)
    x=[]
    max = 0
    for i in range(8000):
        t = -math.log(1-random())/0.35
        if t>max:
            max = t
        y.append(t)
    print(max)
    x =np.linspace(0,max,50)
    x=x[1:]
    for i in x:
        dict[i] = 0
    for e in y:
        for j in dict:
            if e<j and abs(e-j) < max/50:
                dict[j]+=1
    y = [dict[i] for i in dict]
    plt.bar(x, y, max/50, color="green")
    plt.title("Arrival")
    plt.show()

def draw_1():
    dict ={}
    y=[]
    seed(0)
    x=[]
    max = 0
    for i in range(8000):
        t = -math.log(1-random())/1 - math.log(1-random())/1 -math.log(1-random())/1
        if t>max:
            max = t
        y.append(t)
    print(max)
    x =np.linspace(0,max,50)
    x=x[1:]
    for i in x:
        dict[i] = 0
    for e in y:
        for j in dict:
            if e<j and abs(e-j) < max/50:
                dict[j]+=1
    y = [dict[i] for i in dict]
    plt.bar(x, y, max/50, color="green")
    plt.title("Service")
    plt.show()



#mrt,depart = function('trace',[10,20,32,33],[1,2,3,4],3,50,100)
#print('mrt =',mrt)
#for i in depart:
# print(f'job arrive at {i[0]}, job departure at {i[1]}')
#
#mrt,depart = function('random',0.35,1,5,5,0.1,20000)
#for i in range(1,4):
# seed(i)
# mrt,depart =function('random',0.35,1,5,5,0.1,20000)
# with open(f'mrt_{i}.txt','w') as file:
#     file.write(f'{mrt:0.3f}')
# with open(f'departure_{i}.txt','w') as file:
#     for e in depart:
#         file.write(f'{e[0]:0.3f}\t {e[1]:0.3f}\n')

