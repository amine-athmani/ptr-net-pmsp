import os
import sys
import numpy as np

import reader as rd 

def write_solution(path):
    f = open(path,"r")
    content = f.read().split("\n")
    content_formatted = ""
    #content_formatted = str(content[4:len(content)-2]).replace("[","").replace("]","<ENDM>").replace(" ","").replace("','","")
    for i in range(4,len(content)-2):
        content_formatted+=content[i].replace("[","").replace("]","").replace(" ","")
        if (i != len(content)-2):
            content_formatted+="<ENDM>"
    return(content_formatted)

def write_solution_ML(path):
    f = open(path,"r")
    best_cmax = 99999
    best_i = 1
    i = 1
    sequences = f.read().split("Best sequence is:\n")
    for sequence in sequences[1:]:
        content = sequence.split("\n")
        if (i==0):
            print(content)
        cmax = int(content[-2])
        if cmax < best_cmax:
            best_cmax = cmax
            best_i = i
        i += 1
    content_formatted = ""
    content = sequences[best_i].split("\n")
    #content_formatted = str(content[4:len(content)-2]).replace("[","").replace("]","<ENDM>").replace(" ","").replace("','","")
    for i in range(0,len(content)-2):
        content_formatted+=content[i].replace("[","").replace("]","").replace(" ","")
        if (i != len(content)-2):
            content_formatted+="<ENDM>"
    return(content_formatted)

def get_files_dict(path):
    files = {}
    i = 0
    for r, d, f in os.walk(path):
        for file in f:
            if '.xls' not in file:
                file_info = file.split("_")
                files.setdefault((file_info[1],file_info[2]),[]).append(os.path.join(r, file))

    return(files)

def write_instance(path):
    reader = rd.READ_BENCHMARK()
    instance=reader.READ_INSTANCE(path)
    nb_job = instance[0]
    nb_machines = instance[1]
    all_instances = ""
    for i in range(0,nb_job):
        job_process = [ str(elem) for elem in instance[2][i] ]
        job_setup = []
        for S in instance[3]:
            job_setup.append(str(np.mean(np.array(S[i]))))
        instance_formatted = (",".join(job_process))
        instance_formatted += "<ENDP>"
        instance_formatted += (",".join(job_setup))
        instance_formatted += "<ENDT>"

        all_instances += instance_formatted
    return all_instances

def get_files_dict_ML(path):
    files = {}
    i = 0
    for r, d, f in os.walk(path):
        for file in f:
            if '.xls' not in file:
                file_info = file.split("_")
                files.setdefault((file_info[2],file_info[3]),[]).append(os.path.join(r, file))

    return (files)

def create_dataset():
    path = "Solutions/Set_1"
    output_path = "data.ptr"
    output_file = open(output_path,"w")
    solution_paths = get_files_dict(path)
    solution_keys = solution_paths.keys()
    solution_keys = sorted(solution_keys, key=lambda solution_key: solution_key[0])
    for k in solution_keys:
        for path_k in solution_paths.get(k):
            print(path_k)
            path_infos = path_k.split("/")
            instance_path = "Instances/"+path_infos[1]+"/"+path_infos[2]+"/"+path_infos[3]+"/"+path_infos[4]+"/"+path_infos[5]+"/"+path_infos[7]+".txt"
            output_file.write(write_instance(instance_path))
            output_file.write(" output ")
            output_file.write(write_solution(path_k))
            output_file.write("\n")
    output_file.close()

def main():
    path = "../metaheuristic_rm_sijk_cmax/RES_GA1_(II_IMI_EI_ES_B)/ML_alpha_beta/"
    solution_paths = get_files_dict_ML(path)
    output_path = "data/data_alpha_beta.ptr"
    output_file = open(output_path,"w")
    solution_paths = get_files_dict(path)
    solution_keys = solution_paths.keys()
    solution_keys = sorted(solution_keys, key=lambda solution_key: solution_key[1])
    for k in solution_keys:
        if (k==("100","5")):
            for path_k in solution_paths.get(k):
                path_infos = path_k.split("/")
                print(path_k)
    
    #print(write_instance("../Instances/I_100_5_S_1-149_0.1_0.4_10.txt"))
    #print(write_solution_ML("../Instances/Solution/best_I_100_5_S_1-149_0.1_0.4_10"))
if __name__ == '__main__':
    main()


