from js import document
import matplotlib.pyplot as plt
import numpy as np
from multicoremlfqs import *

def translate_english(event):
    job = document.querySelector("#input1").value
    output1_div = document.querySelector("#output1")
    output1_div.innerText = job
    iquantum = document.querySelector("#input2").value
    output2_div = document.querySelector("#output2")
    output2_div.innerText = iquantum
    iallotment = document.querySelector("#input3").value
    output3_div = document.querySelector("#output3")
    output3_div.innerText = iallotment
    boost = document.querySelector("#input4").value
    output4_div = document.querySelector("#output4")
    output4_div.innerText = boost
    ioTime = document.querySelector("#input5").value
    output5_div = document.querySelector("#output5")
    output5_div.innerText = ioTime
# #     นับจำนวนงานและเก็บไว้ในarray task_times
# task_times=[]
# timeCPU = 0
# job = input("enter : ")
# iquantum = input("enter : ")
# iallotment = input("enter : ")
# boost = input("enter : ")
# ioTime = input("enter : ")
# if (job == '') or (iquantum == '') or (iallotment == '') or (boost == '') or (ioTime == '') :
#     x=mlfq_multicore()
#     jobs = 3
# else :
#     x=mlfq_multicore(int(job),int(iquantum),int(iallotment),int(boost),int(ioTime))
#     jobs = int(job)

# # x=mlfq_multicore(job)

# for i in range (0,jobs):
#     timeCPU = x[0][i]['runTime']
#     #timeCPU=x[1][i]['currTimeCore']
#     task_times.append(timeCPU)

# # for j in range(0,job):
# #     print(j," ", x[0][j]['currCore'],"",x[0][j]['runTime']) #การหา job
# #     #print(x[0][j]['runTime'])    

# # จำนวน CPU cores
# num_cores = 4
# cpu_names = [f'CPU {i+1}' for i in range(num_cores)]

# # เวลาที่แต่ละงานใช้เสร็จ (ในหน่วยเวลา)
# # เหลือทำ task_times ให้รับค่าจากเพื่อนได้
# #task_times = [200, 84, 76, 58, 110, 75, 85, 56, 210, 312]
# count =1
# tasks =[]
# text = "Task "
# labels = ['CPU1','CPU2','CPU3','CPU4']

# #นับจำนวนงานที่อยู่ในlist
# for i in task_times:
#     count+=1
    
# #ชื่องานแต่ละงาน
# for j in range(0,count):
#     result = text + str(j)
#     tasks.append(result)
    

# # สร้างกราฟ
# plt.figure(figsize=(10, 6))
# bottom = [0] * num_cores
# assignments = {}

# for task, time in zip(tasks, task_times):
#     # ค้นหา CPU core ที่ว่างที่สุด
#     min_core = min(range(num_cores), key=lambda core: bottom[core])
    
#     # กำหนดงานให้ CPU core ที่ว่างที่สุด
#     assignments[task] = min_core
    
#     # สร้างกราฟแท่งเด้อ
#     plt.bar(min_core, time, bottom=bottom[min_core], label=task)
#     bottom[min_core] += time

# plt.xlabel('CPU')
# plt.ylabel('Time (units)')
# plt.title('Multi-thread Multi-CPU Task Execution Time')
# plt.legend(loc='upper right')

# # เพิ่มชื่อ CPU ในแต่ละแท่ง
# plt.xticks(range(num_cores), labels)

# # พิมพ์ข้อมูลการกำหนดงานในแต่ละ CPU
# # print("Task assignments to CPU cores:")
# # for task, core in assignments.items():
# #     print(f"{task} -> CPU {core + 1}")
    
# #plt.yticks(range(1, 30+1)) เว้นไปก่อนไม่รู้จะเขียนยังไงให้พอดี
# plt.show()

