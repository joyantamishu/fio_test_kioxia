# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import re
number_of_cpus = 64
import statistics
def process_cpu_calculation(cpu_usage_list):
    print(cpu_usage_list)
    sample_list = list()
    for single_list in cpu_usage_list:
        sample_list.append(100.0-float(single_list[len(single_list)-1]))

    print(sample_list)

    if len(sample_list) == 1:
        return sample_list[0], 0
    return round(statistics.mean(sample_list),1), round(statistics.stdev(sample_list),1)

def return_cpu_list(cpu_usage_list):
    sample_list = list()
    for single_list in cpu_usage_list:
        sample_list.append(100.0-float(single_list[len(single_list)-1]))

    return sample_list


def dump_result(performance_dict, cpu_dict):
    workload_string = ['seqwriteq{}t{}', 'seqreadq{}t{}', 'randomreadq{}t{}', 'randomwriteq{}t{}']
    workload_string_identifier = ['Sequential 128 KB Write', 'Sequential 128KB Read', 'Random 4KB Read', 'Random 4KB Write']
    f = open("data.csv", "w")
    f.write('Operation, Opt_ID, Threads, Queue Depth, Device Queue Depth, KIOPS , Bandwidth(MiBs), '
            'cpu_core_index, usr, nice, sys, iowait, irq, soft, steal, guest, gnice, cpu_usages\n')

    queue_depth_array = ['1', '2', '4', '8', '16', '32', '64', '128']

    thread_array = ['1', '2', '4', '8', '16', '32', '64']
    count = 0
    for workload in workload_string:
        for queue_depth in queue_depth_array:
            for thread in thread_array:
                workload_identifier = workload.format(queue_depth, thread)

                if workload_identifier not in performance_dict.keys() or workload_identifier not in cpu_dict.keys():
                    print("No performance or cpu data for " + workload_identifier)
                    continue
                #print(workload_identifier)
                #mean, variance = process_cpu_calculation(cpu_dict[workload_identifier])
                #cpu_usages_list = return_cpu_list(cpu_dict[workload_identifier])
                cpu_count = 0

                for single_cpu in cpu_dict[workload_identifier]:
                    sum_total = 0
                    f.write(workload_string_identifier[count] + ',' + workload_identifier +
                            ',' + thread + ',' + queue_depth + ',' + str(int(queue_depth) * int(thread)) + ',' +
                            str(performance_dict[workload_identifier][0]) + ',' +
                            str(performance_dict[workload_identifier][1]) + ','+str(cpu_count)+",")
                    for x in range(0, len(single_cpu)-1):
                        #print(single_cpu[x])
                        f.write(str(single_cpu[x])+',')
                        sum_total += float(single_cpu[x])
                    f.write(str(sum_total)+'\n')
                    cpu_count +=1

                #f.write("\n")
        count += 1
        #f.write("\n")


    f.close()


def parse_performance_file(name, result_dict):

    #print(name)

    key = name.split('.')[0]

    #print(key)

    nums = re.findall('[0-9]+', name)

    queue_depth = nums[0]
    thread = nums[1]
    #print(queue_depth, thread)

    file1 = open(name, 'r')
    Lines = file1.readlines()

    count = 0
    iops = 0
    bw = 0
    # Strips the newline character
    for line in Lines:
        count += 1
        if (line.strip().startswith('iops')):
            #print(line.strip())
            keywords = line.strip().split(', ')
            if keywords:
                for keyword in keywords:
                    if keyword.startswith('avg='):
                        iops = float(keyword.split('=')[1])/pow(10,3)
                        #print("iops "+iops)
                        break
        if (line.strip().startswith('bw')):
            inMB = True
            #print(line.strip())
            keywords = line.strip().split(', ')
            #print(keywords[0])
            if 'KiB/s' in keywords[0]:
                inMB = False
            if keywords:
                for keyword in keywords:
                    if keyword.startswith('avg='):
                        bw = round(float(keyword.split('=')[1])/pow(10,3) if not inMB else float(keyword.split('=')[1]),1)
                        break

    if key in result_dict.keys():
        return False
    result_dict[key] = (iops,bw)

    #print("Line{}: {}".format(count, line.strip()))


# Press the green button in the gutter to run the script.



def parse_cpu_file(fname, N, result_dict):
    #print(fname)
    prefix = fname.split('.')[0]
    #print(prefix)
    #print (queue_depth + thread)
    count = 0
    with open('cpu/'+fname) as file:
        for line in (file.readlines()[-N:]):

            # if count >= thread:
            #     break
            info = line.strip().split()
            #print(info)
            result_single_cpu = list()
            for x in range (2,len(info)):
                result_single_cpu.append(float(info[x]))
                #print(info[x])
            count += 1
            result_dict[prefix].append(result_single_cpu)


if __name__ == '__main__':

    import os
    from collections import defaultdict

    result_dict = dict()

    result_cpu_dict = defaultdict(list)

    file_arr = os.listdir()

    for file in file_arr:
        if file.endswith('.txt'):
            parse_performance_file(file, result_dict)

    #print(result_dict)

    file_arr = os.listdir('cpu/')
    #print(file_arr)

    for file in file_arr:
        if file.endswith('.txt'):
            parse_cpu_file(file, number_of_cpus, result_cpu_dict)

    #result_cpu_dict = sorted(result_cpu_dict)
    #print(result_cpu_dict)
    dump_result(result_dict, result_cpu_dict)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
