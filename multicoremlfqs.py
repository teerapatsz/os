
import random
import sys
import os

def random_seed(seed) :
    try:
        random.seed(seed,version=1)
    except:
        random.seed(seed)
    return

def FindQueue(hiQueue,queue) :
    q = hiQueue
    while q > 0:
        if len(queue[q]) > 0:
            return q
        q -= 1
    if len(queue[0]) > 0:
        return 0  
    return -1

def Abort(str) :
    sys.stderr.write(str+'\n')
    exit(1)

def mlfq_multicore1(numJobs=3,iquantum=10,iallotment=1,boost=0,ioTime=5):
    seed = 0
    maxlen = 100
    maxio = 10
    iobump = False
    stay = False
    random.seed(seed)
    # MLFQ: How Many Queues
    numQueues = 3
    numCores = 4

    quantum = {}

    for i in range(numQueues):
        quantum[i] = int(iquantum)

    allotment = {}
    for i in range(numQueues):
            allotment[i] = int(iallotment)
    # print("allotment : ",allotment)
    hiQueue = numQueues - 1

    # MLFQ: I/O Model
    # the time for each IO: not great to have a single fixed time but...
    ioTime = int(ioTime)

    # This tracks when IOs and other interrupts are complete
    ioDone = {}

    # This stores all info about the jobs
    job = {}
    # seed the random generator
    random_seed(seed)

    jobCnt = 0 
    qcores = 0

    # do something random
    for jobCnt in range(numJobs):
        startTime = 0
        runTime   = int(random.random() * (maxlen - 1) + 1)
        ioFreq    = int(random.random() * (maxio - 1) + 1)
        
        job[jobCnt] = {'currCore':qcores,'currPri':hiQueue, 'ticksLeft':quantum[hiQueue],
                        'allotLeft':allotment[hiQueue], 'startTime':startTime,
                        'runTime':runTime, 'timeLeft':runTime, 'ioFreq':ioFreq, 'doingIO':False,
                        'firstRun':-1}
        if startTime not in ioDone:
            ioDone[startTime] = []
        ioDone[startTime].append((jobCnt, 'JOB BEGINS'))
        # jobCnt += 1
    # print(job)
    numJobs = len(job)
    jobs = []
    for k in job.keys():
        jobs.append(k)

    # initialize the MLFQ queues
    queue = {}
    for q in range(numQueues):
        queue[q] = []

    #Time
    currTime = 0
    TimeC = 0
    time1 = 0
    time2 = 0
    time3 = 0
    time4 = 0
    currTimeCore = {1 : 0,
                    2 : 0,
                    3 : 0,
                    4 : 0}
    
    # #initialize for Core
    cores = {}
    for c in range(1,numCores+1) :
        cores.update({c:{'currTimeCore':TimeC}})
    # use these to know when we're finished
    totalJobs    = len(job)  #default 3
    finishedJobs = 0 
    oldJob = 0
    indcore = 0
    count = 0
    countcore = 1
    # print('Job List:')
    # for i in range(numJobs):
        # print('  Job %2d: startTime %3d - runTime %3d - ioFreq %3d' % (i, job[i]['startTime'], job[i]['runTime'], job[i]['ioFreq']))
    # print('')
    # print('\nExecution Trace:\n')
    #Execution Trace
    for j in range(1,len(job)+1) :
        if j <= numCores :
            if jobs[j-1] == oldJob:
                qcores = j
            else :
                qcores = j
                oldJob += 1
        else :
            for t in range(1,numCores+1):
                if(t == 1):
                    count = t
                    indcore = cores[t]['currTimeCore']
                else :
                    if(cores[t]['currTimeCore'] <= indcore):
                        count = t
                        indcore = cores[t]['currTimeCore']
            qcores = count
        
        job[j-1]['currCore'] = qcores
        cores[qcores]['currTimeCore'] += job[j-1]['runTime']
    
    while finishedJobs < totalJobs :
    # print(cores)
        for j in range(1,len(job)+1) :
            if len(job) >= 4:
                if countcore == 4:
                    countcore = 1
            else :
                if countcore > 3:
                    countcore = 1
            if boost > 0 and currTime != 0 :
                if currTime % boost == 0 :
                    # print('[ core %d  ] BOOST ( every %d )' % (currCore, boost))
                    # remove all jobs from queues (except high queue) and put them in high queue
                    for q in range(numQueues-1):
                        for j in queue[q]:
                            if job[j]['doingIO'] == False:
                                queue[hiQueue].append(j)

                    #change priority to high priority
                    # reset number of ticks left for all jobs (just for lower jobs?)
                    # add to highest run queue (if not doing I/O)
                    for j in range(numJobs):
                        # print('-> Boost %d (timeLeft %d)' % (j, job[j]['timeLeft']))
                        if job[j]['timeLeft'] > 0:
                            # print('-> FinalBoost %d (timeLeft %d)' % (j, job[j]['timeLeft']))
                            job[j]['currCore'] = qcores
                            job[j]['currPri']   = hiQueue
                            job[j]['ticksLeft'] = quantum[hiQueue]
                            job[j]['allotLeft'] = allotment[hiQueue]
                            # print('  BOOST', j, ' ticks:', job[j]['ticksLeft'], ' allot:', job[j]['allotLeft'])
                    # print('BOOST END: QUEUES look like:', queue)
            # check for any I/Os done
            if currTime in ioDone:
                for (j, type) in ioDone[currTime]:
                    q = job[j]['currPri']
                    job[j]['doingIO'] = False
                    # print('[ time %d ] %s by JOB %d' % (currTime, type, j))
                    if iobump == False or type == 'JOB BEGINS':
                        queue[q].append(j)
                    else:
                        queue[q].insert(0, j)
            # now find the highest priority job
            currQueue = FindQueue(hiQueue,queue)
            if currQueue == -1:
                # print(' IDLE' )
                currTime += 1
                continue

            # there was at least one runnable job, and hence ...
            currJob = queue[currQueue][0]
            if job[currJob]['currPri'] != currQueue:
                Abort('currPri[%d] does not match currQueue[%d]' % (job[currJob]['currPri'], currQueue))
            job[currJob]['timeLeft']  -= 1
            job[currJob]['ticksLeft'] -= 1

            if job[currJob]['firstRun'] == -1:
                job[currJob]['firstRun'] = currTime
            currCore = job[currJob]['currCore']
            runTime   = job[currJob]['runTime']
            ioFreq    = job[currJob]['ioFreq']
            ticksLeft = job[currJob]['ticksLeft']
            allotLeft = job[currJob]['allotLeft']
            timeLeft  = job[currJob]['timeLeft']
            # print('[ core %d | time %d ] Run JOB %d at PRIORITY %d [ TICKS %d ALLOT %d TIME %d (of %d) ]' % \
            # (currCore,currTimeCore[currCore], currJob, currQueue, ticksLeft, allotLeft, timeLeft, runTime))

            if timeLeft < 0:
                Abort('Error: should never have less than 0 time left to run')
            
            # UPDATE TIME
            currTime += 1
            # print("currcore : ",currCore)
            if currCore == 1 :
                time1 += 1
                currTimeCore.update({currCore:time1})
            if currCore == 2 :
                time2 += 1
                currTimeCore.update({currCore:time2})
            if currCore == 3 :
                time3 += 1
                currTimeCore.update({currCore:time3})
            if currCore == 4 :
                time4 += 1
                currTimeCore.update({currCore:time4})

            # CHECK FOR JOB ENDING
            if timeLeft == 0:
                # print('[ core %d  ] FINISHED JOB %d' % (currCore, currJob))
                finishedJobs += 1
                job[currJob]['endTime'] = currTime
                # print('BEFORE POP', queue)
                done = queue[currQueue].pop(0)
                # print('AFTER POP', queue)
                assert(done == currJob)
                continue
        
            # CHECK FOR IO
            issuedIO = False
            if ioFreq > 0 and (((runTime - timeLeft) % ioFreq) == 0):
                # time for an IO!
                # print(' IO_START by JOB %d' % ( currJob))
                issuedIO = True
                desched = queue[currQueue].pop(0)
                assert(desched == currJob)
                job[currJob]['doingIO'] = True
                # this does the bad rule -- reset your time at this level if you do I/O
                if stay == True:
                    job[currJob]['ticksLeft'] = quantum[currQueue]
                    job[currJob]['allotLeft'] = allotment[currQueue]
                # add to IO Queue: but which queue?
                futureTime = currTime + ioTime
                if futureTime not in ioDone:
                    ioDone[futureTime] = []
                # print('IO DONE')
                ioDone[futureTime].append((currJob, 'IO_DONE'))

            # CHECK FOR QUANTUM ENDING AT THIS LEVEL (BUT REMEMBER, THERE STILL MAY BE ALLOTMENT LEFT)
            if ticksLeft == 0:
                if issuedIO == False:
                    # IO HAS NOT BEEN ISSUED (therefor pop from queue)'
                    desched = queue[currQueue].pop(0)
                assert(desched == currJob)

                job[currJob]['allotLeft'] = job[currJob]['allotLeft'] - 1

                if job[currJob]['allotLeft'] == 0:
                    # this job is DONE at this level, so move on
                    if currQueue > 0:
                        # in this case, have to change the priority of the job
                        job[currJob]['currPri']   = currQueue - 1
                        job[currJob]['ticksLeft'] = quantum[currQueue-1]
                        job[currJob]['allotLeft'] = allotment[currQueue-1]
                        if issuedIO == False:
                            queue[currQueue-1].append(currJob)
                    else:
                        job[currJob]['ticksLeft'] = quantum[currQueue]
                        job[currJob]['allotLeft'] = allotment[currQueue]
                        if issuedIO == False:
                            queue[currQueue].append(currJob)
                else:
                    # this job has more time at this level, so just push it to end
                    job[currJob]['ticksLeft'] = quantum[currQueue]
                    if issuedIO == False:
                        queue[currQueue].append(currJob)
        countcore+=1
    # print out statistics
    # print('')
    # print('Final statistics:')
    # responseSum   = 0
    # turnaroundSum = 0
    # for i in range(numJobs):
    #     response   = (job[i]['firstRun']) - (job[i]['startTime'])
    #     turnaround = (job[i]['endTime'] )- (job[i]['startTime'])
    #     print('  Job %2d: startTime %3d - response %3d - turnaround %3d' % (i, job[i]['startTime'], response, turnaround))
    #     responseSum   += response
    #     turnaroundSum += turnaround

    # print('\n')
    return (job,cores)
