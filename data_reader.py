import numpy as np

def get_data(path):
    data = open(path,"r")

    content = data.readlines()
    X = np.zeros((1038,200,60))
    Y = np.full((1038,200),201)

    i = 0
    for line in content:
        #Seperate Input and Output
        instance = line.split("output")

        #Input
        tasks = instance[0].split("<ENDT>")
        j = 0
        for task in tasks[:-1]:
            task_feat = task.split("<ENDP>")
            process_array = np.fromstring(task_feat[0],sep=",")
            setup_array = np.fromstring(task_feat[1],sep=",")
            task_array = np.zeros((60,))
            task_array[:process_array.shape[0]] = process_array
            task_array[30:30+setup_array.shape[0]] = setup_array
            X[i,j] = task_array
            j += 1
        #Output
        machines = instance[1].split("<ENDM>")
        j = 0
        for s in machines:
            solution_array = np.fromstring(s,sep=",")
            if (j == 0):
                solution_i = solution_array[:-1]
                j = 1
            else:
                solution_i = np.concatenate((solution_i,solution_array[:-1]))
        Y[i,:solution_i.shape[0]] = solution_i
        i += 1
    return X[0:1200], Y[0:1200]