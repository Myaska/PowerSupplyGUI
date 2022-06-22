import serial
import time
import pandas as pd
import boto3
import matplotlib.pyplot as plt
    
def port_connection(comNum):
    ser = serial.Serial(comNum, 57600)
    ser.flush()
    ser.write("*idn?\n".encode())
    print(ser.readline())
    
    return ser

def set_curr_and_volt(curr, volt, ser):
    ser.write("SYS:BEEP OFF\n".encode())
    ser.write("SOUR:CURR {curr}\n".format(curr = curr).encode())
    ser.write("SOUR:VOLT {volt}\n".format(volt = volt).encode())

def set_timer(hour, minute, sec, ser):
    ser.write("TIMER:ON\n".encode())
    ser.write("TIMER:HOUR {hour}\n".format(hour = hour).encode())
    ser.write("TIMER:MIN {minute}\n".format(minute = minute).encode())
    ser.write("TIMER:SEC {sec}\n".format(sec = sec).encode())
    ser.write("OUT ON\n".encode())

def set_limits(lim_volt, lim_curr, ser):
    ser.write("OUT:LIM:VOLT 23\n".encode())
    ser.write("OUT:LIM:CURR 0.300\n".encode())

def memory_rec(mem_slot, m_volt, m_curr, ser):
    ser.write("MEM 0\n".encode())
    ser.write("MEM:VSET 10.000\n".encode())
    ser.write("MEM:ISET 0.200\n".encode())
    ser.write("MEM:SAV\n".encode())
    
def data_collect(run_time,file_name, bucket, path, ser):
    current = []
    voltage = []
    seconds = []
    
    for i in range (run_time):
        ser.write("MEAS:CURR?\n".encode())
        current.append(ser.readline().decode("utf-8").strip())
        ser.write("MEAS:VOLT?\n".encode())
        voltage.append(str(ser.readline().decode("utf-8").strip()))
        seconds.append(i+1)
        print(str(i + 1) + ' sec')
        time.sleep(1)
    
        if i % 300 == 0 and i != 0:
            data = {'current' : current, 'voltage' : voltage, 'time' : seconds}
            df = pd.DataFrame(data)
            df.to_csv('/home/pi/power_supply/for_S3/' + file_name)
            print("Data was added to csv file")

    print('Experiment was compleated')
    ser.close()
    
    return current, voltage, time
    
def visualisation(path, file_name, current, voltage, time):

    read_csv = pd.read_csv(path + file_name)
    read_csv = read_csv[(read_csv != 0).all(1)]   
    
    fig, ax = plt.subplots()
    ax.plot(read_csv['time'], read_csv['voltage'], linewidth=1.0)
    ax.set_xlabel('Time, sec')
    ax.set_ylabel('Voltage, V')
    ax.set(ylim=((min(read_csv['voltage']-1)), (max(read_csv['voltage'])+1)), xlim=(0, (max(read_csv['time']))-1000))
    ax.grid(True)
    plt.title(file_name)
    
    jpg_file_name = file_name.split('.')[0] + '.jpg'
    plt.savefig(path + jpg_file_name)
    
    return jpg_file_name

def put_file_to_s3(jpg_file_name, bucket, path):

    s3 = boto3.resource('s3')
    response = s3.meta.client.upload_file(Filename = path + jpg_file_name,
                                      Bucket = bucket,
                                      Key = jpg_file_name)
