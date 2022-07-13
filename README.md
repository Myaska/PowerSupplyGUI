### Power supply 9183B (BKPrecision)

#### Raspberry Pi preparation
You need to set up a Wi-Fi connection on your Raspberry Pi. Run the following command from the CLI: sh raspberry_setup.sh Connect the power supply to your Raspberry Pi and run the main.py files from it. You can use the CLI to access your Raspberry Pi or remote desktop.

#### AWS CLI installation
Here you can find information how to set up AWS on your Raspberry Pi: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

#### Application
This application allows you to run the 9183B power supply from Raspberry Pi. When you start running main.py, the GUI will let you set the parameters for your experiment. By pressing the "Set parameters" and "Exit" buttons, the electrochemical experiment will be launched. After the experiment is completed, the collected data will be graphed and saved as a .jpg file, which will be uploaded to your AWS S3 bucket.


<img width="548" alt="Screen Shot 2022-07-13 at 12 20 43 PM" src="https://user-images.githubusercontent.com/72933965/178793310-f992e921-8e63-46c7-aa9d-800df19dcced.png">
