import serial
import time
import pandas as pd

current = []
voltage = []

#set the duration of the electrochemical experiment
hour = 1
minute = 0
sec = 0

#indicate the port number on the raspberry to which the power supply is connected
comNum = '/dev/ttyUSB0'
ser = serial.Serial(comNum, 57600)
ser.flush()
ser.write("*idn?\n".encode())
print(ser.readline())

#this command disables audio signals from the power supply
ser.write("SYS:BEEP OFF\n".encode())

#set the timer according to the above data
ser.write("TIMER:ON\n".encode())
ser.write("TIMER:HOUR {hour}\n".format(hour = hour).encode())
ser.write("TIMER:MIN {minute}\n".format(minute = minute).encode())
ser.write("TIMER:SEC {sec}\n".format(sec = sec).encode())

#set the maximum allowable current and voltage values
ser.write("OUT ON\n".encode())
ser.write("OUT:LIM:VOLT 23\n".encode())
ser.write("OUT:LIM:CURR 0.300\n".encode())

#set the current and voltage values and store them in the power supply memory in lot 0
ser.write("MEM 0\n".encode())
ser.write("MEM:VSET 10.000\n".encode())
ser.write("MEM:ISET 0.200\n".encode())
ser.write("MEM:SAV\n".encode())

#record current and voltage measurement data throughout the experiment
time = hour*3600 + minute*60 + sec
for i in range (time):
    ser.write("MEAS:CURR?\n".encode())
    current.append(ser.readline().strip())
    ser.write("MEAS:VOLT?\n".encode())
    voltage.append(str(ser.readline().strip()))
    time.sleep(1)

print('Electrochemical experiment was compleated')

#save data in csv file
data = {'current' : current, 'voltage' : voltage}
df = pd.DataFrame(data)
df.to_csv('/home/pi/test.csv')
ser.close()