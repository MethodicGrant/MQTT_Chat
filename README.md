General Instructions: 

Flash SD Card with 64bit RasPI OS lite using the RPI flash tool
MAKE SURE YOU SETUP YOUR WIFI DURING THE FLASHING PROCESS IF YOU ARE DOING A HEADLESS SETUP
When flashing select the allow SSH option unless you have keyboard/mouse/display for the PI zero
Make sure you remember the username and password for the PI 
After flashing your SD Card make sure you install it into the PI and connect power


FOR HEADLESS SETUP:

On your computer open a CMD/Terminal
use the following command to connect ssh PIUSERNAME@raspberrypi.local #you can have a differnt host name if you changed it during flashing. this is for the default hostname. replace "PIUSERNAME" with the username you setup
CMD will prompt you for a Yes/No select Yes
Upon connction it will ask for a password. This is the password you set during the setup in the flash tool. Key in your password and press enter. The terminal line will appear blank and the cursor will not move this is normal.
You should get a username@hostname.local in green upon connection.

FOR KEYBOARD/MOUSE/DISPLAY SETUP SKIP TO NEXT SECTION:

UPON CONNECTION
Once connected run the collowing commands:

sudo apt update
sudo apt install python3 python3-pip -y
sudo apt install python3-paho-mqtt -y
sudo apt install git

Now CD into your desired directory
If you do not care just run the following command from your root directory

sudo git clone https://github.com/MethodicGrant/MQTT_Chat

TO EDIT THE SCRIPT 
use nano or your preffered text editor. I use nano so my commands will be taking that into consideration

Use the following command to open the python file
IF YOU DO NOT RUN THE COMMAND AS SUDO YOU WILL NOT BE ABLE TO EDIT THIS FILE
sudo nano Mqtt_Chat.py

once open follow the instructions listed as comments 

MY CODE ASSUMES YOU ARE USING A HIVEMQ CLOUD BROKER CHANGES WILL NEED TO BE MADE IF YOU ARE USING ANOTHER BROKER

you should only need to change the following:
BROKER
USERNAME
PASSWORD
MY_NAME
PEER_NAME

once edited press ctrl+o then enter

Now run the script with the following command
python3 Mqtt_Chat.py

