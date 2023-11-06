<?php
$servername = "localhost";
$username = "root";
$password = "12345678";
$dbname = "manga";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
    <link rel="stylesheet" href="styles.css">
    <link rel="stylesheet" href="https://pyscript.net/latest/pyscript.css" />
    <script defer src="https://pyscript.net/latest/pyscript.js"></script>
    <py-config>
        packages = ["numpy", "matplotlib"]
        [[fetch]]
        files = ["multicoremlfqs.py"]
    </py-config>
    <title>Document</title>
</head>
<body>
    <header>
        <p>Multi Level Feedback Queue<p>
    </header>
            <div class="container primary">
                <form method="post" action="insert.php">
                    <div class="mb-3">
                        <label for="id" class="form-label">Job</label>
                        <input type="number" class="form-control" id="id" placeholder="Job" name="id" required>
                    </div>
                    <div class="mb-3">
                        <label for="Name" class="form-label">Time</label>
                        <input type="text" class="form-control" id="Name" placeholder="Time" name="Name" required>
                    </div>
                    <div class="mb-3">
                        <label for="cover" class="form-label">Example label</label>
                        <input type="text" class="form-control" id="cover" placeholder="Example input placeholder" name="cover" required>
                    </div>
                    
                    <input type="submit" class="btn btn-primary" > <input type="reset" class="btn btn-secondary" >
                </form>
                <div class="mb-3">
                        <?php 
                            $query = "SELECT * FROM `anime`";
                            $result = mysqli_query($conn, $query);
                            if(mysqli_num_rows($result)>0){
                                while($row=mysqli_fetch_assoc($result)){
                        ?>
                            <h5><?php echo $row["id"]?></h5>
                            <input type="text" class="form-control" id="Name" value="<?php echo $row["Name"]?>" readonly >
                            <img src="<?php echo $row["cover"] ?>" class="img-thumbnail" alt="">
                        <?php
                                }
                            }
                            mysqli_close($conn);
                        ?>
                </div>
            </div>
            <div id="plot" class="alert alert-primary" role="alert"></div>
            <py-script output="plot">
            import matplotlib.pyplot as plt
import numpy as np
from multicoremlfqs import *

#นับจำนวนงานและเก็บไว้ในarray task_times
task_times=[]
timeCPU = 0
job = input("enter : ")
iquantum = input("enter : ")
iallotment = input("enter : ")
boost = input("enter : ")
ioTime = input("enter : ")
if (job == '') or (iquantum == '') or (iallotment == '') or (boost == '') or (ioTime == '') :
    x=mlfq_multicore()
    job = 3
else :
    x=mlfq_multicore(job,iquantum,iallotment,boost,ioTime)

# x=mlfq_multicore(job)

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
display(plt)

            </py-script>
            <!-- <py-script output="plot">
import numpy as np
import matplotlib.pyplot as plt
rng = np.random.default_rng()
xy = rng.random((100,2))*4.0-2.0
z = xy[:, 0]*np.exp(-xy[:, 0]**2-xy[:, 1]**2)
plt.plot(xy, z, "ob")
display(plt)
            </py-script> -->


    

    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js" integrity="sha384-I7E8VVD/ismYTF4hNIPjVp/Zjvgyol6VFvRkX/vR+Vc4jQkC+hVqc2pM8ODewa9r" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.min.js" integrity="sha384-BBtl+eGJRgqQAUMxJ7pMwbEyER4l1g+O15P+16Ep7Q9Q+zqX6gSbd85u4mG4QzX+" crossorigin="anonymous"></script>
</body>
</html>