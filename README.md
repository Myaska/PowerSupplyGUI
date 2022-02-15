### Power supply 9183B (BKPrecision)

    In the file "user_data.py" you must specify all the data for the experiment, such as current, voltage, time, etc., 
    as well as add/remove functions from the "power_supply_functions.py" file that you need for your experiment. 
    
    def data_collect() saves the data in a сsv file and sends it to amazon S3 bucket every 30 minutes. 
    This "put object" operation will trigger Lambda that will create the plots and send them to my email.
