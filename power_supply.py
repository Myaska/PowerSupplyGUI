import serial
import time
import pandas as pd

current = []
voltage = []

hour = 1
minute = 0
sec = 0

comNum = '/dev/ttyUSB0'
ser = serial.Serial(comNum, 57600)
ser.flush()

ser.write("*idn?\n".encode())
print(ser.readline())

ser.write("SYS:BEEP OFF\n".encode())

ser.write("TIMER:ON\n".encode())
ser.write("TIMER:HOUR {hour}\n".format(hour = hour).encode())
ser.write("TIMER:MIN {minute}\n".format(minute = minute).encode())
ser.write("TIMER:SEC {sec}\n".format(sec = sec).encode())

ser.write("OUT ON\n".encode())
#ser.write("OUT:LIM:VOLT 23\n".encode())
#ser.write("OUT:LIM:CURR 0.300\n".encode())

#ser.write("MEM 0\n".encode())
#ser.write("MEM:VSET 10.000\n".encode())
#ser.write("MEM:ISET 0.200\n".encode())
#ser.write("MEM:SAV\n".encode())


for i in range (hour*3600):
    ser.write("MEAS:CURR?\n".encode())
    current.append(ser.readline().strip())
    ser.write("MEAS:VOLT?\n".encode())
    voltage.append(str(ser.readline().strip()))
    time.sleep(0.8)
print('Experiment was compleated')

data = {'current' : current, 'voltage' : voltage}
df = pd.DataFrame(data)
df.to_csv('/home/pi/test.csv')
#ser.write("OUT OFF\n".encode())
ser.close()