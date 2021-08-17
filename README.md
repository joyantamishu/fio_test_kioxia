# fio_test_kioxia

The main goal of this code is to use fio scripts against different type of drives and get the performance (IOPS, BW) and cpu (utilization) based metrices. Now if you want to test against a bare SSD drive, just start from **Run and generate the Test Result** section. Make sure your drive is preconditioned properly. But if you want to generate results for RAID array, you need to create the array first and run the experiements. We used **mdadm** utility to create the md array. There are tons of resources in internet regarding how to create RAID array using **mdadm**, but still I am putting those in the next section for convenience.

# Create RAID Array

I am assuming we have 4 drives named as /dev/nvme0n1, /dev/nvme2n1, /dev/nvme3n1, /dev/nvme4n1, and we want to create a RAID5 array using those 4 drives. You can partition your drives if you want. 

step 1: Clone the repo

step 2: format 4 drives 

- **sudo nvme format -f /dev/nvme0n1**
- **sudo nvme format -f /dev/nvme2n1**
- **sudo nvme format -f /dev/nvme3n1**
- **sudo nvme format -f /dev/nvme4n1**

step 3: create the raid array using **--asume-clean** command. If you don't use this flag, keep in mind the sync opteration will run in background and causes noise in you data.

- **sudo  mdadm --create /dev/md5 --level=5 --raid-devices=4 /dev/nvme0n1 /dev/nvme2n1 /dev/nvme3n1 /dev/nvme4n1 --chunk=128 --assume-clean**

please feel free to change the parameters (i.e. level, raid-devices, chunk etc.). The above command will create a raid 5 array usding 4 drives and the chunk size of that array is 128 KB. check the status using **cat /proc/mdstat** command. If you want to create a RAID 6 array, use **--level=6** in the above command.

step 4: Now you need to precondition your RAID array. For that 
- **cd precond**
- run **sudo python3 precond_pass_1.py --drive=/dev/md5**, and wait until the precond is done. This is basuically the python script provided by ezfio tool. You can also use ezfio to precondtion the drive. 

step 5: When done
- **cd..**, and start the next step "Run and generate the Test Result"

# Run and generate the Test Result
step 1: Clone the repo, if you have not done already.

step 2: ***cd fio_test_kioxia***

step 3: unzip the zip file using command ***unzip fio_tests.zip -d stat_generator/*** Now you have all the fio files to run the experiments

step 4: ***cd stat_generator***

inside the **stat_generator** folder you have two files, named **main_performance.py** and **main_performance_and_cpu_core_all_info.py** which are used to generate the results. Lets generate the input data (run fio scripts) to generate the final result. Please note that these two python file is written in python3.

step 5: run ***sudo ./run_test.sh***, to gnerate the input data. This might take approximately 1.30 hours to generate all the inputs. Each of the .fio file has a corresponding .txt file in the current directory and in the **cpu/** directory

step 6: When all the txt file has been generated, 

- run  **python3 main_performance.py** to generate the performance output file in the current directory. (**main_performance_file.csv**).
- run  **python3 main_performance_and_cpu_core_all_info.py** to generate the performance and cpu related info file in the current directory (**main_performance_and_cpu_core_all_info_file.csv**).

Whola! We are done!

# Reusability
You can find it in the readme inside the stat_generator folder. 
