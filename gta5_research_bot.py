import subprocess

def install_libraries(libraries):
    for library in libraries:
        try:
            __import__(library)
        except ImportError:
            print(f"{library} is not installed. Installing now...")
            subprocess.check_call(["pip", "install", library])
required_libraries = ["pyautogui", "mysql.connector", "tqdm", "colorama"]
install_libraries(required_libraries)


from pyautogui import *
import pyautogui
import mysql.connector
from tqdm import tqdm
from datetime import datetime
import time
import keyboard
import win32api, win32con
import mouse
import math
import os
import uuid
from dateutil.relativedelta import relativedelta
import colorama
from colorama import Fore, Back, Style

print(Fore.YELLOW +'''
  /$$$$$$  /$$$$$$$$ /$$$$$$        /$$    /$$       /$$                           /$$                
 /$$__  $$|__  $$__//$$__  $$      | $$   | $$      | $$                          | $$                
| $$  \__/   | $$  | $$  \ $$      | $$   | $$      | $$$$$$$  /$$   /$$ /$$$$$$$ | $$   /$$ /$$   /$$
| $$ /$$$$   | $$  | $$$$$$$$      |  $$ / $$/      | $$__  $$| $$  | $$| $$__  $$| $$  /$$/| $$  | $$
| $$|_  $$   | $$  | $$__  $$       \  $$ $$/       | $$  \ $$| $$  | $$| $$  \ $$| $$$$$$/ | $$  | $$
| $$  \ $$   | $$  | $$  | $$        \  $$$/        | $$  | $$| $$  | $$| $$  | $$| $$_  $$ | $$  | $$
|  $$$$$$/   | $$  | $$  | $$         \  $/         | $$$$$$$/|  $$$$$$/| $$  | $$| $$ \  $$|  $$$$$$$
 \______/    |__/  |__/  |__/          \_/          |_______/  \______/ |__/  |__/|__/  \__/ \____  $$
                                                                                             /$$  | $$
                                                                                            |  $$$$$$/
                                                                                             \______/ 
                                                                                             
                                                                                                
                                                                                            GTAV Automatic Bunker Research bot by arkis0
      
'''+ Style.RESET_ALL)

mydb = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
    )
mycursor = mydb.cursor()

mac_address = uuid.UUID(int=uuid.getnode()).hex[-12:]

now = datetime.now()
current_date_str = now.strftime('%Y-%m-%d %H:%M:%S')
current_date = datetime.strptime(current_date_str, '%Y-%m-%d %H:%M:%S')

sql = "SELECT * FROM license_keys WHERE mac_address = %s AND valid = 1"
mycursor.execute(sql, (mac_address,))

# Get info if license key is valid
myresult = mycursor.fetchone()

if myresult is not None:
    if myresult[2] != '':
        if myresult[4] > current_date:
            print("License key is valid!")
        else:
            print("License key has expired.")
            validation_update_sql = "UPDATE license_keys SET valid = 0 WHERE mac_address = %s"
            mycursor.execute(validation_update_sql, (mac_address,))
            mydb.commit()
            exit()
    else:
        print("License key is empty.")
else:
    print("No valid license key found for this device.")
    print("Do you have a license key? (y/n)")
    answer = input()
    if answer == 'y' or answer == 'Y':
        print("Enter license key:")
        license_key = input()
        key_sql = "SELECT * FROM license_keys WHERE license_key = %s AND valid = 1"
        mycursor.execute(key_sql, (license_key,))

        # Get info if license key is valid
        myresult_key = mycursor.fetchone()
        if myresult_key is None:
            print("License key is not valid.")
            exit()
        elif myresult_key[1] is not None:
            print("License key is already assigned to another device.")
            exit()
        if myresult_key[6] != 0:
            expiration_date = current_date + relativedelta(months=myresult_key[6])
        elif myresult_key[6] == 0:
            expiration_date = datetime.strptime('9999-12-31 23:59:59', '%Y-%m-%d %H:%M:%S')
        
        
        sql = "UPDATE license_keys SET mac_address = %s, registration_date = %s, expiration_date = %s WHERE license_key = %s"
        
        mycursor.execute(sql, (mac_address, current_date, expiration_date, license_key))
        mydb.commit()
        print("License key was assigned to your device! Your key will expire on:", expiration_date)
    if answer == 'n' or answer == 'N':
        print("You can buy license key from owner by contacting him on discord: .arkis / arkis#0001")
        exit()





begin_position = False



def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    

def buy_resources():
    time.sleep(2)
    click(458, 494) #zakładka odnawiania
    time.sleep(2)
    click(967, 791) #przycisk kup zasoby
    time.sleep(2)
    click(1070, 620) #potwierdź zakup
    time.sleep(2)
    keyboard.press_and_release('esc') #powrót na home screen
    keyboard.press_and_release('esc') #swobodny widok
    print("Resources were ordered!")


def check_progress_of_research():
    
    print("Checking progress of research...")
    mydb = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
    )
    mycursor = mydb.cursor()

    x = 993
    y = 329
    matching_pixels_research = 0
    total_pixels = 597
    step_size = 4
    
    for i in tqdm(range(0, total_pixels, step_size)):
        if pyautogui.pixelMatchesColor(x + i, y, (46,135,46)):
            matching_pixels_research += 4
            
    research_level = math.ceil((matching_pixels_research / total_pixels) * 100)

    print("You have around", research_level, "% of completion on research")

    sql = "INSERT INTO research (research_level) VALUES (%s)"
    mycursor.execute(sql, (research_level,))

    mydb.commit()




def screenshot_of_current_project():
    mydb = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
    )
    mycursor = mydb.cursor()
    #? Usuń ostatni rekord z bazy danych
    sql = "DELETE FROM research_screenshots ORDER BY id DESC LIMIT 1"
    mycursor.execute(sql)
    mydb.commit()

    print("Taking screenshot of current project...")
    click(468, 559)
    sleep(1)
    screenshot = pyautogui.screenshot(region=(1233, 468, 360, 360))
    screenshot.save("screenshot.png")
    print("Sending image to database...")

    command = 'curl -X POST -F "image=@screenshot.png" https://r-dev.pl/save_screenshot.php'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if os.path.exists("screenshot.png"):
        os.remove("screenshot.png")
    

    if result.returncode == 0:
        print("Screenshot was saved to database")
    else:
        print("Error saving screenshot to database")
    keyboard.press_and_release('esc') #powrót na home screen



def check_amount_of_resources():
    print("Checking amount of resources...")
    mydb = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
    )
    mycursor = mydb.cursor()
    x = 993
    y = 380
    matching_pixels_resources = 0
    total_pixels = 597

    step_size = 4
    for i in tqdm(range(0, total_pixels, step_size)):
        if pyautogui.pixelMatchesColor(x + i, y, (179, 57, 9)):
            matching_pixels_resources += 4

    resource_amount = math.ceil((matching_pixels_resources / total_pixels) * 100)

    print("You have around", resource_amount, "% of resources")
    if(resource_amount <= 30):
        print("You need to order more resources")
        buy_resources()
    else:
        print("You have sufficient amount of resources")
        keyboard.press_and_release('esc')

    sql = "INSERT INTO resources (resources_amount) VALUES (%s)"
    mycursor.execute(sql, (resource_amount,))
    mydb.commit()

time.sleep(2)

starting_setup = False
last_buy_time = 0
print("Bot won't start until you enter laptop home screen!")
while keyboard.is_pressed('q') == False:
    while starting_setup == False:
        if pyautogui.locateOnScreen('laptop_home_screen_logo.png', region=(0, 0, 1919, 1079), grayscale=True, confidence=0.8) != None:
            print("Laptop home screen detected! Bot is starting")
            starting_setup = True
            time.sleep(0.5)
            click(941, 645)
            
    check_progress_of_research()
    screenshot_of_current_project()
    check_amount_of_resources()
    time_of_check = time.time()
    print("Anti-kick started working! Next resource check in 15 minutes. Message from: ", time.ctime())
    while time.time() - time_of_check <= 900:
        if pyautogui.locateOnScreen('kick_time.png', region=(0, 0, 820, 1079), grayscale=True, confidence=0.8) != None:
            print("Kick message detected. Proceeding with activity")
            mouse.drag(0, 630, 1919, 630, absolute=True, duration=2)
            mouse.drag(1919, 630, 0, 630, absolute=True, duration=2)
            activity_detected = False
            while activity_detected == False:
                if pyautogui.locateOnScreen('kick_time.png', region=(0, 0, 820, 1079), grayscale=True, confidence=0.8) == None:
                    print("Activity was detected by game")
                    activity_detected = True
                    
                else:
                    print("Activity was not detected by game! Retrying")
                    mouse.drag(0, 630, 1919, 630, absolute=True, duration=2)
                    mouse.drag(1919, 630, 0, 630, absolute=True, duration=2)
    keyboard.press_and_release('enter')
    time.sleep(3)
    if pyautogui.locateOnScreen('laptop_home_screen_logo.png', region=(0, 0, 1919, 1079), grayscale=True, confidence=0.8) != None:
            print("Laptop home screen detected!")
            time.sleep(0.5)
            click(941, 645)
