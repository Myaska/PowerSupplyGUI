import power_supply_functions as psf

"""Set parameters for your electrochemical experiment"""

"""1. Enter the name for csv file, where all data will be saved"""
file_name = '05_27_Cr(VI)_23V_0.3A' + '.csv'
path = '/home/pi/power_supply/for_S3/'
bucket = 'data-from-power-supply'

"""2. Set duration of experiment"""
hour = 24
minute = 0
sec = 0
run_time = hour*3600 + minute*60 + sec

"""3. Set voltage and current"""
volt = 23
curr = 0.3

"""4. Indicate port name power supply connected to"""
comNum = '/dev/ttyUSB0'

#this function connect power supply to port
ser = psf.port_connection(comNum)

#this function set current and voltage we need for experiment
psf.set_curr_and_volt(curr, volt, ser)

#this function set timer
psf.set_timer(hour, minute, sec, ser)

#this function save data to csv file every 5 min
current, voltage, time = psf.data_collect(run_time,file_name, bucket, path, ser)

#this functean create plot
jpg_file_name = psf.visualisation(path, file_name, current, voltage, time)

#this function sent .jpg to s3 bucket
psf.put_file_to_s3(jpg_file_name, bucket, path)
