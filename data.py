import matplotlib.pyplot as plt
import numpy as np
from multicoremlfqs import *

#นับจำนวนงานและเก็บไว้ในarray task_times
task_times=[]
timeCPU = 0
job,iquantun,iallotment,boost,ioTime = int(input("enter : ").split())
x=mlfq_multicore(job)

for i in range (0,job):
    timeCPU = x[0][i]['runTime']
    #timeCPU=x[1][i]['currTimeCore']
    task_times.append(timeCPU)

# for j in range(0,job):
#     print(j," ", x[0][j]['currCore'],"",x[0][j]['runTime']) #การหา job
#     #print(x[0][j]['runTime'])    

# จำนวน CPU cores
num_cores = 4
cpu_names = [f'CPU {i+1}' for i in range(num_cores)]

# เวลาที่แต่ละงานใช้เสร็จ (ในหน่วยเวลา)
# เหลือทำ task_times ให้รับค่าจากเพื่อนได้
#task_times = [200, 84, 76, 58, 110, 75, 85, 56, 210, 312]
count =1
tasks =[]
text = "Task "
labels = ['CPU1','CPU2','CPU3','CPU4']

#นับจำนวนงานที่อยู่ในlist
for i in task_times:
    count+=1
    
#ชื่องานแต่ละงาน
for j in range(0,count):
     result = text + str(j)
     tasks.append(result)
    

# สร้างกราฟ
plt.figure(figsize=(10, 6))
bottom = [0] * num_cores
assignments = {}

for task, time in zip(tasks, task_times):
    # ค้นหา CPU core ที่ว่างที่สุด
    min_core = min(range(num_cores), key=lambda core: bottom[core])
    
    # กำหนดงานให้ CPU core ที่ว่างที่สุด
    assignments[task] = min_core
    
    # สร้างกราฟแท่งเด้อ
    plt.bar(min_core, time, bottom=bottom[min_core], label=task)
    bottom[min_core] += time

plt.xlabel('CPU')
plt.ylabel('Time (units)')
plt.title('Multi-thread Multi-CPU Task Execution Time')
plt.legend(loc='upper right')

# เพิ่มชื่อ CPU ในแต่ละแท่ง
plt.xticks(range(num_cores), labels)

# พิมพ์ข้อมูลการกำหนดงานในแต่ละ CPU
# print("Task assignments to CPU cores:")
# for task, core in assignments.items():
#     print(f"{task} -> CPU {core + 1}")
    
#plt.yticks(range(1, 30+1)) เว้นไปก่อนไม่รู้จะเขียนยังไงให้พอดี
plt.show()