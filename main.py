import app_functions as app

'''These functions run app and get input from user'''
win = app.set_conn()
ent_file_name, ent_path, ent_bucket, ent_hour, ent_mins, ent_sec, ent_volt, ent_curr, ent_comNum = app.interface(win)
app.buttons(win)

'''These functions connect to power supply, start experiment and sent output to S3'''
ser = app.port_connection(comNum)
app.set_curr_and_volt(curr, volt, ser)
app.set_timer(hour, minute, sec, ser)
current, voltage, time = app.data_collect(run_time,file_name, bucket, path, ser)
jpg_file_name = app.visualisation(path, file_name, current, voltage, time)
app.put_file_to_s3(jpg_file_name, bucket, path)
