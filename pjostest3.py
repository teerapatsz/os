import matplotlib.pyplot as plt
import numpy as np
from testmlfq1 import task_times

# จำนวน CPU cores
num_cores = 4
cpu_names = [f'CPU {i+1}' for i in range(num_cores)]

# ชื่องาน หยาบๆคิดเงื่อนไขไม่ออกของแมนเองจ้าา ไว้มาแก้เมื่อเขียนเสร็จด้วยเด้ออ
#tasks = ['Task 1', 'Task 2', 'Task 3', 'Task 4', 'Task 5', 'Task 6', 'Task 7', 'Task 8', 'Task 9','Task10 ']

# เวลาที่แต่ละงานใช้เสร็จ (ในหน่วยเวลา)
# เหลือทำ task_times ให้รับค่าจากเพื่อนได้
# task_times = [200, 84, 76, 58, 110, 75, 85, 56, 210, 312]
count =1
tasks =[]
text = "Task "
labels = ['CPU1','CPU2','CPU3','CPU4']

for i in task_times: #นับจำนวนงานที่อยู่ในlist 
    count+=1

for j in range(1,count): #ชื่องานแต่ละงาน
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

# พิมพ์ข้อมูลการกำหนดงานในแต่ละ CPU
print("Task assignments to CPU cores:")
for task, core in assignments.items():
    print(f"{task} -> CPU {core + 1}")
    
#plt.yticks(range(1, 30+1)) เว้นไปก่อน
plt.show()