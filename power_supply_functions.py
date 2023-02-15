import serial
import time

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
    
def data_collect(run_time, path, file_name, ser):
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
    
        with open(file_name, 'a') as file:
            data = f'{seconds}, {voltage}'
            file.wrte(data+'\n')

    ser.close()
    
    return current, voltage, time

def set_voltage_lim(ser, volt_max):
    ser.write("OUT ON\n".encode())
    for i in range(3600):
        ser.write("MEAS:VOLT?\n".encode())
        a = ser.readline().decode("utf-8").strip()
        print(a)
        if float(a) > volt_max:
            ser.write("SYS:BEEP ON\n".encode())
            ser.write("OUT OFF\n".encode())         
            break
        else:
            time.sleep(1)
                
def set_program(ser):
    #ser.write("*idn?\n".encode())
    ser.write("PROG 1\n".encode())
    ser.write("PROG:CLE\n".encode())
    ser.write("PROG:REP 5\n".encode())
    ser.write("PROG:TOTA 2\n".encode())
    
    ser.write("PROG:STEP 1\n".encode())
    ser.write("PROG:STEP:CURR 0.3\n".encode())
    ser.write("PROG:STEP:VOLT 5\n".encode())
    ser.write("PROG:STEP:ONT 3\n".encode())
    
    ser.write("PROG:STEP 2\n".encode())
    ser.write("PROG:STEP:CURR 0.35\n".encode())
    ser.write("PROG:STEP:VOLT 7\n".encode())
    ser.write("PROG:STEP:ONT 3\n".encode())
    
    ser.write("PROG:NEXT 0\n".encode())
    ser.write("PROG:SAVE\n".encode())
    
    ser.write("PROG:RUN ON\n".encode())
    
def program_on(ser):
    ser.write("PROG 1\n".encode())
    ser.write("PROG:RUN ON\n".encode())
    
def program_off(ser):
    ser.write("PROG 1\n".encode())
    ser.write("PROG:RUN OFF\n".encode())    

