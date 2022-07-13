import serial
import time
import pandas as pd
import boto3
import matplotlib.pyplot as plt
from tkinter import *

def set_conn():
    win = Tk()
    return win 

def show_data():
    global file_name, path, bucket, run_time, volt, curr, comNum
    
    file_name = ent_file_name.get()
    path = ent_path.get()
    bucket = ent_bucket.get()
    run_time = int(ent_hour.get())*3600 + int(ent_mins.get())*60 + int(ent_sec.get())
    volt = ent_volt.get()
    curr = ent_curr.get()    
    comNum = ent_comNum.get()
    
def interface(win):
    
    Label(win, text='Enter file name:').grid(row=0)
    Label(win, text='Enter path for output files:').grid(row=1)
    Label(win, text='Enter S3 bucket name:').grid(row=2)
    Label(win, text='Enter the duration of the experiment:').grid(row=3)
    Label(win, text='hours').grid(row=4)
    Label(win, text='min').grid(row=5)
    Label(win, text='sec').grid(row=6)
    Label(win, text='Set current value in A:').grid(row=8)
    Label(win, text='Set voltage value in V:').grid(row=9)
    Label(win, text='Set port nuber (try /dev/ttyUSB0 if you are not sure):').grid(row=10)
    
    ent_file_name = Entry(win)
    ent_path = Entry(win)
    ent_bucket = Entry(win)
    ent_hour = Entry(win)
    ent_mins = Entry(win)
    ent_sec = Entry(win)
    ent_volt = Entry(win)
    ent_curr = Entry(win)
    ent_comNum = Entry(win)
    
    ent_file_name.grid(row=0, column=1)
    ent_path.grid(row=1, column=1)
    ent_bucket.grid(row=2, column=1)
    ent_hour.grid(row=4, column=1)
    ent_mins.grid(row=5, column=1)
    ent_sec.grid(row=6, column=1)
    ent_volt.grid(row=8, column=1)
    ent_curr.grid(row=9, column=1)
    ent_comNum.grid(row=10, column=1)
    
    return ent_file_name, ent_path, ent_bucket, ent_hour, ent_mins, ent_sec, ent_volt, ent_curr, ent_comNum

def buttons(win):
    Button(win, text='Exit', command=win.quit).grid( row=12, column=1, sticky=W, pady=4)
    Button(win, text='Set parameters', command=show_data).grid( row=11, column=1, sticky=W, pady=4 )
    mainloop()
   
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
