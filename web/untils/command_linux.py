COMMAND_GET_DATE = 'date +%s'
COMMAND_GET_CPU = """
#!/bin/sh
#
#脚本功能描述：依据/proc/stat文件获取并计算CPU使用率
#
#CPU时间计算公式：CPU_TIME=user+system+nice+idle+iowait+irq+softirq
#CPU使用率计算公式：cpu_usage=(idle2-idle1)/(cpu2-cpu1)*100
#默认时间间隔
TIME_INTERVAL=0.1
LAST_CPU_INFO=$(cat /proc/stat | grep -w cpu | awk '{print $2,$3,$4,$5,$6,$7,$8}')
LAST_SYS_IDLE=$(echo $LAST_CPU_INFO | awk '{print $4}')
LAST_TOTAL_CPU_T=$(echo $LAST_CPU_INFO | awk '{print $1+$2+$3+$4+$5+$6+$7}')
sleep ${TIME_INTERVAL}
NEXT_CPU_INFO=$(cat /proc/stat | grep -w cpu | awk '{print $2,$3,$4,$5,$6,$7,$8}')
NEXT_SYS_IDLE=$(echo $NEXT_CPU_INFO | awk '{print $4}')
NEXT_TOTAL_CPU_T=$(echo $NEXT_CPU_INFO | awk '{print $1+$2+$3+$4+$5+$6+$7}')
#系统空闲时间
SYSTEM_IDLE=`echo ${NEXT_SYS_IDLE} ${LAST_SYS_IDLE} | awk '{print $1-$2}'`
#CPU总时间
TOTAL_TIME=`echo ${NEXT_TOTAL_CPU_T} ${LAST_TOTAL_CPU_T} | awk '{print $1-$2}'`
CPU_USAGE=`echo ${SYSTEM_IDLE} ${TOTAL_TIME} | awk '{printf "%.2f", 100-$1/$2*100}'`
echo "${CPU_USAGE}"
"""
COMMAND_GET_MEM = "cat /proc/meminfo|sed -n '1,4p'|awk '{print $2}'"
COMMAND_GET_DISK = "df -h|sed '1d'|awk '{print $5,$6}'"

# 获取日期
def get_date(ssh):
    if(ssh == None):
        return None
    stdin, stdout, stderr = ssh.exec_command(COMMAND_GET_DATE)
    curr_time = stdout.readlines()
    curr_time = curr_time[0].strip()
    return int(curr_time)

# 获取CPU
def get_cpu(ssh):
    if (ssh == None):
        return None
    # 查看cpu使用率(取三次平均值)
    # 第一个参数是频次(s)，第二个是输出数量(条)
    stdin, stdout, stderr = ssh.exec_command(COMMAND_GET_CPU)
    cpu = stdout.readlines()[0].strip()
    return cpu

# 获取内存
def get_mem(ssh):
    if (ssh == None):
        return None
    # 查看内存使用率
    mem = "cat /proc/meminfo|sed -n '1,4p'|awk '{print $2}'"
    stdin, stdout, stderr = ssh.exec_command(mem)
    mem = stdout.readlines()
    mem_total = round(int(mem[0]) / 1024)
    mem_total_free = round(int(mem[1]) / 1024) + round(int(mem[2]) / 1024) + round(int(mem[3]) / 1024)
    mem_usage = str(round(((mem_total - mem_total_free) / mem_total) * 100, 2))
    return mem_usage

# 获取磁盘
def get_disk(ssh):
    if (ssh == None):
        return [],[]
    # 查看硬盘使用率
    disk = "df -h|sed '1d'|awk '{print $5,$6}'"
    stdin, stdout, stderr = ssh.exec_command(disk)
    disk = stdout.readlines()
    disk_x, disk_y = [], []
    for i in disk:
        disk_x.append(i.split(" ")[1].strip())
        disk_y.append(int(i.split(" ")[0][:-1]))
    return disk_x,disk_y
