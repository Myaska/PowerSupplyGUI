### Power supply 9183B (BKPrecision)

#### Raspberry Pi preparation
You need to set up a WiFi connection on your Raspberry Pi. Run in your CLI the foolowing command:
sh raspberry_setup.sh 
Connect your power supply to Raspberry Pi and run .py files from it. You can use CLI to get access to your Raspberry Pi or Remote Desctop. 

#### AWS CLI installation
Here you can find information how to set up AWS on your Raspberry Pi: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

#### Application
This app make it able to run Power supply 9183B from Raspberry Pi. When you atart to run main.py, grafical interface allow you to set parameters for your experiment. When you press the botton "Set parameters" and "Quit" the electrochemical experiment will be started. After the end of the experiment, based on the collected data, a plot will be made and saved as a .jpg file, which will be uploaded to your AWS S3 bucket.
<img width="518" alt="Screen Shot 2022-07-13 at 12 15 39 PM" src="https://user-images.githubusercontent.com/72933965/178792379-7bc1a8df-d35a-4cac-84f5-08270b130af1.png">
