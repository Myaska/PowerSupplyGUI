import serial
import time
import pandas as pd
import boto3

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
            df.to_csv('/home/pi/' + file_name)
            print("Data was added to csv file")
    
        if i % 1800 == 0 and i != 0:
            s3 = boto3.resource('s3')
            response = s3.meta.client.upload_file(Filename = path + file_name,
                                      Bucket = bucket,
                                      Key = file_name)
            print("Data was senе to s3 bucket")

    print('Experiment was compleated')
    ser.close()
