task_times=[]
timeCPU = 0
#test = 10 #ดูว่ารับjob จากอะไรแล้วค่อยเขียนใหม่
from multicoremlfq import *

# mlfq_multicore(numJobs=5)
# job = int(input("enter job : "))
# # x = mlfq_multicore()
# #print(x[0][2]['currCore']) การหา job
# # print(x[1][3]['currTimeCore'])
x=mlfq_multicore() 
print(x[1][3]['currTimeCore'])
# for i in range (0,job):
#     timeCPU = x[0][i]['runTime']
#     #timeCPU=x[1][i]['currTimeCore']
#     task_times.append(timeCPU)
# print(task_times)

# #print(x[0][2]['currCore']) #การหา job
# for j in range(0,job):
#     print(j," ", x[0][j]['currCore'],"",x[0][j]['runTime']) #การหา job
#     #print(x[0][j]['runTime'])
    




        

        
     